import logging
import pymysql
import json
from DB_manager import DatabaseManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        conn = DatabaseManager.get_db_connection()
        try:
            purchase_detail = json.loads(event['body'])

            purchase_id = purchase_detail.get('purchaseId')
            if not purchase_id:
                raise ValueError("purchaseId is required")

            update_columns = []
            params = []

            if 'purchaseDate' in purchase_detail:
                update_columns.append("purchaseDate = %s")
                params.append(purchase_detail['purchaseDate'])
            if 'purchaseCode' in purchase_detail:
                update_columns.append("purchaseCode = %s")
                params.append(purchase_detail['purchaseCode'])
            if 'purchaseStatus' in purchase_detail:
                update_columns.append("purchaseStatus = %s")
                params.append(purchase_detail['purchaseStatus'])
            if 'referenceNo' in purchase_detail:
                update_columns.append("referenceNo = %s")
                params.append(purchase_detail['referenceNo'])
            if 'supplierName' in purchase_detail:
                update_columns.append("supplierName = %s")
                params.append(purchase_detail['supplierName'])
            if 'purchaseTotal' in purchase_detail:
                update_columns.append("purchaseTotal = %s")
                params.append(purchase_detail['purchaseTotal'])
            if 'amountPaid' in purchase_detail:
                update_columns.append("amountPaid = %s")
                params.append(purchase_detail['amountPaid'])
            if 'purchasePaymentDue' in purchase_detail:
                update_columns.append("purchasePaymentDue = %s")
                params.append(purchase_detail['purchasePaymentDue'])
            if 'paymentStatus' in purchase_detail:
                update_columns.append("paymentStatus = %s")
                params.append(purchase_detail['paymentStatus'])

            if not update_columns:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json",
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                        "statusCode": 400,
                        "responseMessage": "FAILURE",
                        "response": "No valid fields provided to update"
                    }, default=str)
                }

            update_query = f'''
                UPDATE PURCHASE p
                LEFT JOIN PURCHASE_PAYMENT pp ON p.purchaseId = pp.purchaseId
                SET {", ".join(update_columns)}
                WHERE p.purchaseId = %s
            '''
            params.append(purchase_id)

            with conn.cursor() as cur:
                cur.execute(update_query, params)
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
                        "responseMessage": "SUCCESS",
                        "response": purchase_detail
                    }, default=str)
                }

        except Exception as ex:
            logger.error(f"Error occurred: {str(ex)}")
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
        logger.error(f"Connection error occurred: {str(ex)}")
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
