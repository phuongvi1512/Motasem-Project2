from flask import Flask, jsonify
from flask_mysqldb import MySQL
from pymongo import MongoClient
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from bson.decimal128 import Decimal128

load_dotenv()
app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

schema = {
    "num_reports": "int",
    "max_size": "float",
    "avg_size": "float",
    "timestamp": "datetime"
}

@app.route('/analyze-report', methods=['GET', 'POST'])
def retrieve_mysql_and_update_mongodb():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT count(*) FROM reports")
        num_reports = cur.fetchone()[0]

        cur.execute("SELECT max(file_size) FROM reports")
        max_size = cur.fetchone()[0]

        cur.execute("SELECT avg(file_size) FROM reports")
        avg_size = cur.fetchone()[0]

        client = MongoClient(                
            host=os.getenv('MONGODB_HOST'),
            port=int(os.getenv('MONGODB_PORT')))
      
        
        db = client['analyticdb']
        collection = db['analytic']
            # Convert Decimal to Decimal128
        max_size_mongo = Decimal128(str(max_size))
        avg_size_mongo = Decimal128(str(avg_size))
        
        collection.insert_one({
            "num_reports": num_reports,
            "max_size": max_size_mongo,
            "avg_size": avg_size_mongo,
            "timestamp": datetime.now()
        })
        return jsonify({"message": "Report has been created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)