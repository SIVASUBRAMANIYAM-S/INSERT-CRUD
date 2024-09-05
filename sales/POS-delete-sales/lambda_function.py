import logging
from DB_manager import DatabaseManager
import pymysql
import json

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
                sales_id = event['queryStringParameters']['salesId']
                
                update_sales_query = '''UPDATE SALES 
                                        SET isActive = 0 
                                        WHERE salesId = %s'''
                
                with conn.cursor() as cur:
                    cur.execute(update_sales_query, (sales_id,))
                    conn.commit()
                
                response_body['response'] = "Deleted Successfully"
                
            elif action == "getSalesDetails":
                sales_details = []
                
                with conn.cursor(pymysql.cursors.DictCursor) as cur:
                    cur.callproc('SP_GET_SALES_DETAILS')
                    sales_details = cur.fetchall()
                
                response_body['response'] = sales_details
            
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
