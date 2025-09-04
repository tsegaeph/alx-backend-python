#!/usr/bin/python3

import psycopg2
from psycopg2 import sql
import uuid
import csv


def connect_db():
    """Connect to PostgreSQL server (default 'postgres' database)."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",      
            password="findit"
        )
        connection.autocommit = True
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ALX_prodev';"
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE ALX_prodev;")
            print("Database ALX_prodev created successfully")
        else:
            print("Database ALX_prodev already exists")
        cursor.close()
    except Exception as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",  
            password="findit",
            database="ALX_prodev"
        )
        connection.autocommit = True
        return connection
    except Exception as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL NOT NULL
            );
        """)
        cursor.close()
        print("Table user_data created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Reads header automatically
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])  # cast to integer

                # Skip if email already exists
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s;", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))
        cursor.close()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
