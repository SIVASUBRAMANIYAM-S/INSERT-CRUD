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
            print(event)
            customer_detail = json.loads(event['body'])
            
            insert_customer_query = '''INSERT INTO CUSTOMER 
                                       (shopId, customerName, phoneNumber, email, address, city, state, country, postCode) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                                       
            with conn.cursor() as cur:
                customer_data = [customer_detail['shopId'], customer_detail['customerName'], customer_detail['phoneNumber'], 
                                 customer_detail['email'], customer_detail['address'], customer_detail['city'], 
                                 customer_detail['state'], customer_detail['country'], customer_detail['postCode']]
                                 
                cur.execute(insert_customer_query, customer_data)
                customer_data_id = conn.insert_id()
                conn.commit()
                
                customer_detail['customerId'] = customer_data_id
                
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
                        "response": customer_detail
                    }, default=str)
                }
        
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
                    "responseMessage": "FAILURE",
                    "response": str(ex)
                }, default=str)
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
                "responseMessage": "FAILURE",
                "response": str(ex)
            }, default=str)
        }

if __name__ == "__main__":
    events = {
        "body": json.dumps({
            "shopId": "1",
            "customerName": "siva",
            "phoneNumber": "8825722468",
            "email": "sivasaravanan492@gmail.com",
            "address": "29,KKG nagar",
            "city": "virudhachalam",
            "state": "tamil Nadu",
            "country": "India",
            "postCode": "606001"
        })
    }
    lambda_handler(events, None)
