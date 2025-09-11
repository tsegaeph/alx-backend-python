# 4-cache_query_postgres.py

import psycopg2
import functools
import os

# Simple cache dictionary
query_cache = {}


#### Decorator for DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "alxtravel"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "findit"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432"),
        )
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


#### Decorator to cache queries
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"⚡ Using cached result for query: {query}")
            return query_cache[query]
        print(f"🆕 Executing and caching query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


#### Function with caching
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### Run
if __name__ == "__main__":
    # First call executes query
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call uses cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
