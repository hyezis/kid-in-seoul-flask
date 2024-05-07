from flask import Flask, request, jsonify
import pymysql
import config

app = Flask(__name__)

def get_user_region(member_id):
    conn = pymysql.connect(
        host=config.DB_CONFIG['host'], 
        port=3306, 
        user=config.DB_CONFIG['user'], 
        passwd=config.DB_CONFIG['passwd'], 
        db=config.DB_CONFIG['db'], 
        charset='utf8'
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT region_id FROM member WHERE member_id = %s", (member_id,))
    user_region_id = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user_region_id:
        return user_region_id[0]
    else:
        return None

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_id = data.get('member_id')

    if user_id is None:
        return jsonify({"error": "Member ID is required."}), 400

    user_region_id = get_user_region(user_id)
    if user_region_id is None:
        return jsonify({"error": "Region is required for the specified member."}), 400
    
    conn = pymysql.connect(
        host=config.DB_CONFIG['host'], 
        port=3306, 
        user=config.DB_CONFIG['user'], 
        passwd=config.DB_CONFIG['passwd'], 
        db=config.DB_CONFIG['db'], 
        charset='utf8'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT facility_id, facility_type FROM facility WHERE region_id = %s ORDER BY like_count DESC LIMIT 20", (user_region_id,))
    recommends = cursor.fetchall()

    cursor.close()
    conn.close()

    if not recommends:
        return jsonify({"message": "No facilities found in the specified region."}), 404

    result = [{"facility_id": rec[0], "facility_type": rec[1]} for rec in recommends]
    return jsonify({"recommendations": result}), 200

if __name__ == '__main__':
    app.run(prot=8070,debug=False)
