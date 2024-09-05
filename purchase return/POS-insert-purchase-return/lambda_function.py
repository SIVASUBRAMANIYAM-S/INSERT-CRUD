import logging
from DB_manager import DatabaseManager
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        conn = DatabaseManager.get_db_connection()
        try:
            logger.info("Received event: %s", event)
            purchase_return_detail = json.loads(event['body'])
            
            if 'returnDate' not in purchase_return_detail or not purchase_return_detail['returnDate']:
                purchase_return_detail['returnDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            insert_purchase_return_query = '''
                INSERT INTO PURCHASE_RETURN 
                (purchaseId, supplierName, supplierId, status, returnDate, referenceNo, itemName) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            
            with conn.cursor() as cur:
                purchase_return_data = [
                    purchase_return_detail.get('purchaseId'), 
                    purchase_return_detail.get('supplierName'), 
                    purchase_return_detail.get('supplierId'), 
                    purchase_return_detail.get('status'), 
                    purchase_return_detail.get('returnDate'), 
                    purchase_return_detail.get('referenceNo'), 
                    purchase_return_detail.get('itemName')
                ]
                
                cur.execute(insert_purchase_return_query, purchase_return_data)
                purchase_return_id = conn.insert_id()
                conn.commit()
                
                purchase_return_detail['purchaseReturnId'] = purchase_return_id
                
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
                        "response": purchase_return_detail
                    }, default=str)
                }
                
        except Exception as ex:
            logger.error("Error during database operation: %s", str(ex))
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
        logger.error("Error establishing database connection: %s", str(ex))
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
        "body": json.dumps({
            "purchaseId": 1,
            "supplierName": "ABT Supplies",
            "supplierId": 123,
            "status": "return",
            # "returnDate": "2024-08-26", 
            "referenceNo": 54379,
            "itemName": "Item ABC"
        })
    }
    response = lambda_handler(events, None)
    print(response)
