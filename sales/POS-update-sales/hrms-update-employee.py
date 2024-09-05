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
            update_employee_query = f'''UPDATE EMPLOYEE SET 
                                firstName='{employee_detail['firstName']}',
                                middleName='{employee_detail['middleName']}',
                                lastName='{employee_detail['lastName']}',
                                birthDate='{employee_detail['birthDate']}',
                                genderID='{employee_detail['genderID']}',
                                currentAddress='{employee_detail['currentAddress']}',
                                permanentAddress='{employee_detail['permanentAddress']}',
                                officialAddress='{employee_detail['officialAddress']}',
                                mobile='{employee_detail['mobile']}',
                                personalMailId='{employee_detail['personalMailId']}',
                                officialMailId='{employee_detail['officialMailId']}',
                                aadharNumber='{employee_detail['aadharNumber']}',
                                maritalStatusId='{employee_detail['maritalStatusId']}',
                                positionId='{employee_detail['positionId']}',
                                roleId='{employee_detail['roleId']}',
                                statusId='{employee_detail['statusId']}',
                                loginTypeId='{employee_detail['loginTypeId']}',
                                joiningDate='{employee_detail['joiningDate']}',
                                leaveDate='{employee_detail['leaveDate']}',
                                lastLogin='{employee_detail['lastLogin']}',
                                lastLogout='{employee_detail['lastLogout']}',
                                profilePhoto='{employee_detail['profilePhoto']}',
                                createdBy='{employee_detail['createdBy']}',
                                createdDate='{employee_detail['createdDate']}',
                                modifiedBy='{employee_detail['modifiedBy']}',
                                modifiedDate='{employee_detail['modifiedDate']}',
                                comments='{employee_detail['comments']}'
                            WHERE empId='{employee_detail['empId']}' '''
            
            with conn.cursor() as cur:
                cur.execute(update_employee_query)
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

