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
            customer_detail = event['queryStringParameters']
            customer_id = customer_detail['customerId']
            
            update_customer_query = f'''
                UPDATE CUSTOMER 
                SET isActive = 0
                WHERE customerId = {customer_id}
            '''
            
            with conn.cursor() as cur:
                cur.execute(update_customer_query)
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
                        "response" : "Deleted Successfully"
                    }, default=str)
                }
                
        except Exception as ex: 
            logger.error(f"Error executing query: {str(ex)}")
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
                    "response" : str(ex)
                }, default=str)
            }
                
        finally:
            if conn:
                conn.close()
    
    except Exception as ex: 
        logger.error(f"Error connecting to the database: {str(ex)}")
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
                "response" : str(ex)
            }, default=str)
        }
