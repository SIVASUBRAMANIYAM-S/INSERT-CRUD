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
            sales_detail = json.loads(event['body'])

            sales_id = sales_detail.get('salesId')
            if not sales_id:
                raise ValueError("salesId is required")

            update_columns = []
            params = []

            if 'salesDate' in sales_detail:
                update_columns.append("salesDate = %s")
                params.append(sales_detail['salesDate'])
            if 'salesCode' in sales_detail:
                update_columns.append("salesCode = %s")
                params.append(sales_detail['salesCode'])
            if 'salesStatus' in sales_detail:
                update_columns.append("salesStatus = %s")
                params.append(sales_detail['salesStatus'])
            if 'referenceNo' in sales_detail:
                update_columns.append("referenceNo = %s")
                params.append(sales_detail['referenceNo'])
            if 'customerName' in sales_detail:
                update_columns.append("customerName = %s")
                params.append(sales_detail['customerName'])
            if 'salesTotal' in sales_detail:
                update_columns.append("salesTotal = %s")
                params.append(sales_detail['salesTotal'])
            if 'amountPaid' in sales_detail:
                update_columns.append("amountPaid = %s")
                params.append(sales_detail['amountPaid'])
            if 'salesPaymentDue' in sales_detail:
                update_columns.append("salesPaymentDue = %s")
                params.append(sales_detail['salesPaymentDue'])
            if 'paymentStatus' in sales_detail:
                update_columns.append("paymentStatus = %s")
                params.append(sales_detail['paymentStatus'])

            # Check if there are columns to update
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
                UPDATE SALES s
                LEFT JOIN SALES_PAYMENT sp ON s.salesId = sp.salesId
                SET {", ".join(update_columns)}
                WHERE s.salesId = %s
            '''
            params.append(sales_id)

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
                        "response": sales_detail
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
