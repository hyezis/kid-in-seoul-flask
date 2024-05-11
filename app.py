import config
from flask import Flask, request, jsonify
import pymysql
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def connect_to_database():
    return pymysql.connect(
        host=config.DB_CONFIG['host'], 
        port=3306, 
        user=config.DB_CONFIG['user'], 
        passwd=config.DB_CONFIG['passwd'], 
        db=config.DB_CONFIG['db'], 
        charset='utf8'
    )

def get_user_region(member_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT region_id FROM member WHERE member_id = %s", (member_id,))
    user_region_id = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_region_id:
        return user_region_id[0]
    else:
        return None

def get_user_likes(member_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT facility_id FROM member_preferred_facility WHERE member_id = %s", (member_id,))
    user_likes = [like[0] for like in cursor.fetchall()]

    cursor.close()
    conn.close()

    return user_likes

def get_similar_users(user_likes):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT member_id FROM member_preferred_facility WHERE facility_id IN %s", (tuple(user_likes),))
    similar_users = set([like[0] for like in cursor.fetchall()])
    
    cursor.close()
    conn.close()

    return similar_users

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/recommend', methods=['POST'])
def recommend():
    conn = connect_to_database()
    cursor = conn.cursor()

    data = request.json
    user_id = data.get('member_id')

    if user_id is None:
        return jsonify({"error": "Member ID is required."}), 400

    user_region_id = get_user_region(user_id)
    if user_region_id is None:
        return jsonify({"error": "Region is required for the specified member."}), 400
    
    user_likes = get_user_likes(user_id)
    if not user_likes:
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
        recommends = cursor.fetchall()
        result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]

        cursor.close()
        conn.close()
        
        return jsonify({"recommendations": result}), 200
    
    similar_users = get_similar_users(user_likes)
    if not similar_users:
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
        recommends = cursor.fetchall()
        result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]
        
        cursor.close()
        conn.close()

        return jsonify({"recommendations": result}), 200

    cursor.execute("SELECT facility_id, like_count FROM facility WHERE region_id = %s", (user_region_id,))
    facilities = cursor.fetchall()

    cursor.close()
    conn.close()

    if not facilities:
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
        recommends = cursor.fetchall()
        result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]
        
        cursor.close()
        conn.close()

        return jsonify({"recommendations": result}), 200

    # Sort facilites based on Similarity with similar users' likes
    facility_scores = {}
    for facility in facilities:
        facility_id, facility_type, like_count = facility
        score = sum(like_count for like_count in user_likes if like_count in similar_users)
        facility_scores[facility_id] = {"facility_id": facility_id, "facility_type": facility_type, "score": score}
    
    sorted_facilities = sorted(facility_scores.values(), key=lambda x: x["score"], reverse=True)[:20]
    result = [{"facility_id": facility["facility_id"], "facility_type": facility["facility_type"]} for facility in sorted_facilities]
    return jsonify({"recommendations": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
