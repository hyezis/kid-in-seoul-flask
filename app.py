import config
from flask import Flask, request, jsonify
import pymysql
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Okt

app = Flask(__name__)
okt = Okt()

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
    user_region_id = cursor.fetchone()[0]  # Changed to directly fetch the value

    if user_region_id:
        return user_region_id
    else:
        # Improved error handling
        raise ValueError("Region not found for the specified member.")

def get_user_likes(member_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT facility_id FROM member_preferred_facility WHERE member_id = %s", (member_id,))
    user_likes_id = [like[0] for like in cursor.fetchall()]
    cursor.execute("SELECT name FROM facility WHERE facility_id IN %s", (tuple(user_likes_id),))  # Modified SQL query to handle multiple facility IDs
    user_likes = [like[0] for like in cursor.fetchall()]

    return user_likes

def get_similar_facilities(user_region_id, user_likes):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM facility WHERE region_id = %s", (user_region_id,))
    all_facilities = cursor.fetchall()
    facility_list = [name[0] for name in all_facilities]
    user_likes_string = ' '.join(user_likes)

    user_likes_tokens = okt.morphs(user_likes_string)

    facility_tokens = [okt.morphs(name) for name in facility_list]
    facility_str = [' '.join(tokens) for tokens in facility_tokens]

    facility_str.append(' '.join(user_likes_tokens))

    vectorizer = CountVectorizer()
    facility_matrix = vectorizer.fit_transform(facility_str)

    similarity_matrix = cosine_similarity(facility_matrix, facility_matrix)

    num_facilities = len(facility_list)

    similar_indices = similarity_matrix[num_facilities - 1].argsort()[-6:-1][::-1]

    similar_facilities = [facility_list[i] for i in similar_indices]

    return similar_facilities

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

    try:
        user_region_id = get_user_region(user_id)
    except ValueError as e:
        conn = connect_to_database()
        cursor = conn.cursor()
        return jsonify({"error": str(e)}), 400
    
    user_likes = get_user_likes(user_id)

    if not user_likes:
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
        recommends = cursor.fetchall()
        result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]

        cursor.close()
        conn.close()
        
        return jsonify({"recommendations": result}), 200

    cursor.execute("SELECT name FROM facility WHERE region_id = %s", (user_region_id,))
    facilities = cursor.fetchall()

    if not facilities:
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
        recommends = cursor.fetchall()
        result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]
        
        cursor.close()
        conn.close()

        return jsonify({"recommendations": result}), 200

    user_liked_facilities = [facility[0] for facility in facilities if facility[0] in user_likes]
    similar_facilities = get_similar_facilities(user_region_id, user_liked_facilities)
    print("similar_facilities")
    print(similar_facilities)
    
    result = []
    for facility_name in similar_facilities:
        print(facility_name)
        cursor.execute("SELECT facility_id, facility_type FROM facility WHERE name IN %s", (tuple(facility_name),))
        facility_info = cursor.fetchall()
        print("faciliyt_info")
        print(facility_info)
        if facility_info:
            result.append({"facility_id": facility_info[0], "facility_type": facility_info[1]})
        print("result")
        print(result)

    cursor.close()
    conn.close()

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
