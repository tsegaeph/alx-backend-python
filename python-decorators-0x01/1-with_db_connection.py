# 1-db_connection.py

import psycopg2
import functools

#### Decorator to handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a connection
        conn = psycopg2.connect(
            dbname="users_db", 
            user="postgres",     
            password="findit",   
            host="127.0.0.1",
            port="5432"
        )
        try:
            # Pass the connection to the function
            result = func(conn, *args, **kwargs)
        finally:
            # Close the connection
            conn.close()
        return result
    return wrapper

#### Function to fetch a user by ID
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
