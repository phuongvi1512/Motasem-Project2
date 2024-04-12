import json
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz
from flask import Flask, jsonify, current_app
from flask_mysqldb import MySQL
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from apscheduler.schedulers.background import BackgroundScheduler

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

sched = BackgroundScheduler(daemon=True)
#specify timezone UTC
timezone = pytz.timezone('UTC')

#@app.route('/analyze-report', methods=['GET', 'POST'])
def retrieve_mysql_and_update_mongodb():
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT count(*) FROM reports")
            num_reports = cur.fetchone()[0]

            cur.execute("SELECT max(file_size) FROM reports")
            max_size = cur.fetchone()[0]

            cur.execute("SELECT avg(file_size) FROM reports")
            avg_size = cur.fetchone()[0]

            # client = MongoClient(                
            #     host=os.getenv('MONGODB_HOST'),
            #     port=27017) #int(os.getenv('MONGODB_PORT')))
        
            client = MongoClient('mongodb://mongodb:27017')
            
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
    
def init_scheduler():
    #create a scheduler
    sched = BackgroundScheduler(daemon=True)

    #specify timezone UTC
    timezone = pytz.timezone('UTC')

    # def scheduled_job():
    #     print("starting the scheduled job")
    #     with app.app_context():
    #         retrieve_mysql_and_update_mongodb(http_request=True)
    #add the scheduler to run the populate_stats every 5 seconds
    sched.add_job(retrieve_mysql_and_update_mongodb, 'interval', seconds=60, timezone=timezone)
    #start the scheduler
    sched.start()


if __name__ == '__main__':
    init_scheduler()
    app.run(host='0.0.0.0', port=5001)