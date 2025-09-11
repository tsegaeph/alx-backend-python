from datetime import datetime
import psycopg2
import functools

#### Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the SQL query from args or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0]
        # Log the timestamp and query
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

#### Function to fetch all users
@log_queries
def fetch_all_users(query):
    conn = psycopg2.connect(
        dbname="users_db", 
        user="postgres",   
        password="findit",  
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
