import psycopg2

class ExecuteQuery:
    def __init__(self, query, params=None, db_name="users_db", user="postgres", password="your_password", host="localhost", port="5432"):
        self.query = query
        self.params = params
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open connection
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        # Execute query immediately
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        # Rollback if exception, else commit
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        # Cleanup
        self.cursor.close()
        self.conn.close()


# Usage example
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(results)
