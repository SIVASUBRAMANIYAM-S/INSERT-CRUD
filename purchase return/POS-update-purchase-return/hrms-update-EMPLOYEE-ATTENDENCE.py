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
            department_detail = json.loads(event['body'])
            update_attendance_query = f'''UPDATE EMPLOYEE_ATTENDANCE SET 
                                loginTypeId='{attendance_detail['loginTypeId']}',
                                empId='{attendance_detail['empId']}',
                                workLocation='{attendance_detail['workLocation']}',
                                inTime='{attendance_detail['inTime']}',
                                inStatus='{attendance_detail['inStatus']}',
                                outTime='{attendance_detail['outTime']}',
                                outStatus='{attendance_detail['outStatus']}',
                                Notes='{attendance_detail['Notes']}'
                            WHERE attendanceId='{attendance_detail['attendanceId']}' '''

            
            with conn.cursor() as cur:
                cur.execute(update_attendance_query)
                conn.commit()
                
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
                                    "response" : department_detail},default=str)}
                
        except Exception as ex: 
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

