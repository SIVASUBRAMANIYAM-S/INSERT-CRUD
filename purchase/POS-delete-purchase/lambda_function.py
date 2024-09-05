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
        response_body = {"statusCode": 200, "responseMessage": "SUCCESS"}
        
        logger.info(f"Received event: {event}")

        try:
            action = event.get('queryStringParameters', {}).get('action')
            
            if action == "delete":
                purchase_id = event['queryStringParameters']['purchaseId']
                
                update_purchase_query = '''UPDATE PURCHASE 
                                           SET isActive = 0 
                                           WHERE purchaseId = %s'''
                
                with conn.cursor() as cur:
                    cur.execute(update_purchase_query, (purchase_id,))
                    conn.commit()
                
                response_body['response'] = "Deleted Successfully"
                
            elif action == "getPurchaseDetails":
                purchase_details = []
                
                with conn.cursor(pymysql.cursors.DictCursor) as cur:
                    cur.callproc('SP_GET_PURCHASE_DETAILS')
                    purchase_details = cur.fetchall()
                
                response_body['response'] = purchase_details
            
            else:
                response_body['statusCode'] = 400
                response_body['responseMessage'] = "FAILURE"
                response_body['response'] = "Invalid action specified"
            
        except Exception as ex:
            logger.error(f"Error occurred: {ex}")
            response_body['statusCode'] = 502
            response_body['responseMessage'] = "FAILURE"
            response_body['response'] = str(ex)
        
        finally:
            if conn:
                conn.close()
        
        return {
            "statusCode": response_body['statusCode'],
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            "body": json.dumps(response_body, default=str)
        }

    except Exception as ex:
        logger.error(f"Error occurred outside DB operations: {ex}")
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
                "responseMessage": "FAILURE",
                "response": str(ex)
            }, default=str)
        }
