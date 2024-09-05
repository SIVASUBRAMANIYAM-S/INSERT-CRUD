import logging
import json
from DB_manager import DatabaseManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try: 
        conn = DatabaseManager.get_db_connection()   
        
        with conn.cursor() as cur:
            select_query = "SELECT * FROM CUSTOMER"  
            cur.execute(select_query)
            
            row_headers = [x[0] for x in cur.description]  
            records = cur.fetchall()  
            
            json_data = [dict(zip(row_headers, result)) for result in records]  
            
            response = {
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
            
            return response

    except Exception as ex:
        logger.error(f"Error: {str(ex)}")
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

if __name__ == "__main__":
    events = {
        "queryStringParameters": {"type": "customerDetails"}
    }
    lambda_handler(events, None)
