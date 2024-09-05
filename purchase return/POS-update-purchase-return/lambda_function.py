import logging
from DB_manager import DatabaseManager
import pymysql
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    conn = None
    try:
        conn = DatabaseManager.get_db_connection()
        purchase_detail = json.loads(event['body'])

        allowed_fields = [
            'purchaseCode', 'purchaseStatus', 'referenceNo', 'supplilerName', 
            'total', 'paidAmount', 'due', 'paymentStatus', 'createdBy'
        ]

        update_fields = []
        update_values = []

        for field in allowed_fields:
            if field in purchase_detail:
                update_fields.append(f"{field} = %s")
                update_values.append(purchase_detail[field])

        if not update_fields:
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
                    "responseMessage": "No valid fields provided for update."
                }, default=str)
            }

        update_purchase_details_query = (
            f"UPDATE PURCHASE_DETAILS SET {', '.join(update_fields)} "
            f"WHERE purchaseDetailsId = %s"
        )
        update_values.append(purchase_detail['purchaseDetailsId'])

        with conn.cursor() as cur:
            cur.execute(update_purchase_details_query, tuple(update_values))
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
