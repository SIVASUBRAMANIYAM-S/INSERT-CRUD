import logging
from DB_manager import DatabaseManager
import pymysql
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try: 
        conn = DatabaseManager.get_db_connection()   
        try:
            print(event)
            sales_detail = json.loads(event['body'])
            
            insert_sales_query = '''INSERT INTO SALES (shopId, salesCode, salesPaymentId, salesDate, salesStatus, 
                                    customerId, customerName, quantity, salesTotal, salesPaymentDue, paymentStatus, 
                                    paidAmount, discount, otherCharges, referenceNo) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            
            with conn.cursor() as cur:
                sales_data = [
                    sales_detail['shopId'],
                    sales_detail['salesCode'],
                    sales_detail['salesPaymentId'],
                    datetime.strptime(sales_detail['salesDate'], '%Y-%m-%d %H:%M:%S'),
                    sales_detail['salesStatus'],
                    sales_detail['customerId'],
                    sales_detail['customerName'],
                    sales_detail['quantity'],
                    sales_detail['salesTotal'],
                    sales_detail['salesPaymentDue'],
                    sales_detail['paymentStatus'],
                    sales_detail['paidAmount'],
                    sales_detail['discount'],
                    sales_detail['otherCharges'],
                    sales_detail['referenceNo']
                ]
                
                cur.execute(insert_sales_query, sales_data)
                sales_data_id = conn.insert_id()
                conn.commit()
                sales_detail['salesId'] = sales_data_id

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
                                    "response" : sales_detail },default=str)
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

if __name__  == "__main__":
    events = {
        "body": json.dumps({
            "shopId": 1,
            "salesCode": "S12345",
            "salesPaymentId": 1,
            "salesDate": "2024-09-01 10:00:00",
            "salesStatus": "Final",
            "customerId": 1,
            "customerName": "siva",
            "quantity": 10,
            "salesTotal": 990.00,
            "salesPaymentDue": 0.00,
            "paymentStatus": "paid",
            "paidAmount": 0.00,
            "discount": "5%",
            "otherCharges": 0.00,
            "referenceNo": 1234
        })
    }

    lambda_handler(events, None)
