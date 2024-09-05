import logging
from DB_manager import DatabaseManager
import pymysql
import json
from datetime import datetime, timedelta, date



logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try: 
        conn = DatabaseManager.get_db_connection()   
        try:
            print(event)
            attendance_detail = json.loads(event['body'])
            create_on = datetime.utcnow().isoformat()
            insert_attendance_query = f'''INSERT INTO EMPLOYEE_ATTENDANCE (loginTypeId, empId, workLocation, inTime, inStatus, outTime, outStatus, Notes) 
                   VALUES ({attendance_detail.get('loginTypeId')}, {attendance_detail.get('empId')}, '{attendance_detail.get('workLocation')}', '{attendance_detail.get('inTime')}',
                     '{attendance_detail.get('inStatus')}', '{attendance_detail.get('outTime')}', '{attendance_detail.get('outStatus')}', '{attendance_detail.get('Notes')}') '''
            with conn.cursor() as cur:
               
                print(insert_attendance_query)
                cur.execute(insert_attendance_query)
                attendance_detail_id = conn.insert_id()
                conn.commit()
                attendance['empId'] = attendance_detail_id
                return {
                    "statusCode": 200,
                    "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                                    "statusCode": 200,
                                    "responseMessage" : "SUCCESS",
                                    "response" : user_detail },default=str)}
                
        except Exception as ex: 
            print(ex)
            return {
                    "statusCode": 502,
                    "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                                    "statusCode": 502,
                                    "responseMessage" : "FAILURE",
                                    "response" : str(ex) },default=str)
                }
        
        finally:
                if conn:
                    conn.close()
    
    except Exception as ex: 
            print(ex)
            return {
                    "statusCode": 502,
                    "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                                    "statusCode": 502,
                                    "responseMessage" : "FAILURE",
                                    "response" : str(ex) },default=str)
                }

if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "loginTypeId": "1",
            "empId": "123",
            "workLocation": "Office",
            "inTime": "2024-03-25 09:00:00",
            "inStatus": "Present",
            "outTime": "2024-03-25 18:00:00",
            "outStatus": "Present",
            "Notes": "Regular working hours"
        })
    }

    lambda_handler(event, None)
    lambda_handler(events, None)