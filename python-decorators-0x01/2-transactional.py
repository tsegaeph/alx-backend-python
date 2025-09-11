# 2-transactional.py

import psycopg2
import functools

#### Decorator to handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname="users_db",
            user="postgres",
            password="findit",
            host="127.0.0.1",
            port="5432"
        )
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


#### Decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()   # commit if no error
            return result
        except Exception as e:
            conn.rollback() # rollback if error
            raise e
    return wrapper


#### Function to update user email
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))


#### Run update with automatic transaction handling
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print("User email updated successfully ✅")
