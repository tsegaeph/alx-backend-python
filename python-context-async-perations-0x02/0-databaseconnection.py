import psycopg2

class DatabaseConnection:
    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open PostgreSQL connection
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        # Rollback on error, otherwise commit
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        # Always close connection
        self.cursor.close()
        self.conn.close()


# Usage example
if __name__ == "__main__":
    with DatabaseConnection(
        db_name="users_db",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    ) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
