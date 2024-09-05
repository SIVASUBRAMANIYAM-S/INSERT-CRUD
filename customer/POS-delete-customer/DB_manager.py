import os
import json
import pymysql
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DatabaseManager:
    
    @staticmethod
    def get_db_connection():
        try:
            connection = pymysql.connect(
                host='localhost',
                user='siva',
                passwd='S.siva@2002',
                db='POS',
                connect_timeout=5
            )
            logger.info("Successfully connected to the database RDS Proxy.")
            return connection
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            raise 
