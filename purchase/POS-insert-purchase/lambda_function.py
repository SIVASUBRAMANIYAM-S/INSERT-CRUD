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
            purchase_detail = json.loads(event['body'])

            insert_purchase_query = '''INSERT INTO PURCHASE 
                (shopId, purchaseDate, purchaseCode, purchasePaymentId, paymentStatus, supplierId, purchaseStatus, 
                purchaseTotal, purchasePaymentDue, paidAmount, discount, otherCharges, referenceNo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                
            purchase_data = [
                purchase_detail['shopId'], 
                purchase_detail['purchaseDate'], 
                purchase_detail['purchaseCode'], 
                purchase_detail['purchasePaymentId'], 
                purchase_detail['paymentStatus'], 
                purchase_detail['supplierId'], 
                purchase_detail['purchaseStatus'], 
                purchase_detail['purchaseTotal'], 
                purchase_detail['purchasePaymentDue'], 
                purchase_detail['paidAmount'], 
                purchase_detail['discount'], 
                purchase_detail['otherCharges'], 
                purchase_detail['referenceNo']
            ]

            with conn.cursor() as cur:
                cur.execute(insert_purchase_query, purchase_data)
                purchase_id = conn.insert_id()
                conn.commit()

                for detail in purchase_detail['purchaseDetails']:
                    insert_purchase_details_query = '''INSERT INTO PURCHASE_DETAILS 
                        (purchaseId, itemName, itemDiscount, quantity, tax, purchasePrice, unitId, unitPrice) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                    purchase_details_data = [
                        purchase_id,
                        detail['itemName'],
                        detail['itemDiscount'],
                        detail['quantity'],
                        detail['tax'],
                        detail['purchasePrice'],
                        detail['unitId'],
                        detail['unitPrice']
                    ]
                    cur.execute(insert_purchase_details_query, purchase_details_data)
                
                insert_purchase_payment_query = '''INSERT INTO PURCHASE_PAYMENT 
                    (purchaseId, paymentDate, paymentMethod, paymentStatus, amountPaid, transactionId, paymentNote) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                purchase_payment_data = [
                    purchase_id,
                    purchase_detail['paymentDate'],
                    purchase_detail['paymentMethod'],
                    purchase_detail['paymentStatus'],
                    purchase_detail['amountPaid'],
                    purchase_detail['transactionId'],
                    purchase_detail['paymentNote']
                ]
                cur.execute(insert_purchase_payment_query, purchase_payment_data)

                conn.commit()

                purchase_detail['purchaseId'] = purchase_id
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
                        "response" : purchase_detail
                    }, default=str)
                }
                
        except Exception as ex: 
            logger.error("Error: %s", str(ex))
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
        logger.error("Connection Error: %s", str(ex))
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

if __name__ == "__main__":
    events = {
        "body": json.dumps({
            "shopId": 1,
            "purchaseDate": "2024-08-28",
            "purchaseCode": "PRC123",
            "purchasePaymentId": 2,
            "paymentStatus": "paid",
            "supplierId": 105,
            "purchaseStatus": "received",
            "purchaseTotal": 1000.00,
            "purchasePaymentDue": 200.00,
            "paidAmount": 800.00,
            "discount": "10%",
            "otherCharges": 50.00,
            "referenceNo": 12345,
            "purchaseDetails": [
                {
                    "itemName": "jeans",
                    "itemDiscount": "5%",
                    "quantity": 10,
                    "tax": "5%",
                    "purchasePrice": 100.00,
                    "unitId": 1,
                    "unitPrice": 10.00
                },
                {
                    "itemName": "shirt",
                    "itemDiscount": "10%",
                    "quantity": 5,
                    "tax": "10%",
                    "purchasePrice": 200.00,
                    "unitId": 2,
                    "unitPrice": 20.00
                }
            ],
            "paymentDate": "2024-08-28 10:00:00",
            "paymentMethod": "Cash",
            "paymentStatus": "paid",
            "amountPaid": 800.00,
            "transactionId": "TXN12345",
            "paymentNote": "Payment successful"
        })
    }

    lambda_handler(events, None)