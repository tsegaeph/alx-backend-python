#!/usr/bin/python3
"""
Generator function that streams rows from user_data table one by one.
"""

import psycopg2
from seed import connect_to_prodev

def stream_users():
    """
    Generator that yields each row from user_data as a dictionary.
    No more than one loop is used.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")

    for row in cursor:
        yield {
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3]
        }

    cursor.close()
    connection.close()
