import logging
from DB_manager import DatabaseManager
import pymysql
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try: 
        conn = DatabaseManager.get_db_connection()
        
        try:
            logger.info("Received event: %s", event)
            
            get_sales_details_query = "CALL SP_GET_SALES_DETAILS();"
            
            with conn.cursor() as cur:
                cur.execute(get_sales_details_query)
                
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                
                json_data = [dict(zip(row_headers, result)) for result in rv]
                
                logger.info("Fetched sales details: %s", json_data)
                
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
                        "responseMessage": "SUCCESS",
                        "response": json_data
                    }, default=str)
                }
                
        except Exception as ex: 
            logger.error("Error during query execution: %s", ex)
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
            
        finally:
            if conn:
                conn.close()
    
    except Exception as ex: 
        logger.error("Error establishing DB connection: %s", ex)
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

if __name__ == "__main__":
    events = {
        "queryStringParameters": {"type": "salesDetails"}
    }
    lambda_handler(events, None)