import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

# 1. Initialize the Flask Engine Architecture
app = Flask(__name__)

# 2. Establish the MongoDB Sandbox Connection Pipeline
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# 3. Bind the Database Schema and Collection Maps
db = client['academic_lab_db']
records_collection = db['student_placement_records']

# --- ROUTING ENDPOINTS ---

# GET Route: Home Verification Status
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Online",
        "framework": "Flask + PyMongo Core Engine",
        "message": "Welcome to Usha's Integrated Database API Server! 🚀"
    })

# POST Route: Insert Operation (Syllabus Target)
@app.route('/api/records/insert', methods=['POST'])
def insert_student_record():
    try:
        data = request.get_json()
        student_name = data.get('name')
        leetcode_streak = data.get('streak', 0)
        domain_skill = data.get('skill', 'Full-Stack Development')
        
        if not student_name:
            return jsonify({"success": False, "error": "Missing parameter: name"}), 400
            
        new_document = {
            "name": student_name,
            "streak": int(leetcode_streak),
            "skill": domain_skill
        }
        
        result = records_collection.insert_one(new_document)
        return jsonify({
            "success": True,
            "message": f"Successfully inserted database log for {student_name}!",
            "inserted_id": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# GET Route: Retrieve/Query Operation (Syllabus Target)
@app.route('/api/records/retrieve', methods=['GET'])
def retrieve_all_records():
    try:
        cursor = records_collection.find({}, {"_id": 0})
        records_list = list(cursor)
        return jsonify({
            "success": True,
            "total_documents": len(records_list),
            "data": records_list
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)