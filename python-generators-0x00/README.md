# Python Generators - Task 0: Getting Started with Generators

## 📖 Project Overview
This project introduces the use of Python to interact with a PostgreSQL database and prepare it for generator-based data streaming.  
We focus on setting up a database, creating a table, inserting records from a CSV file, and preparing queries that will later be consumed by generators.

The goal is to **simulate handling large datasets efficiently** by streaming data row by row instead of loading everything into memory.

---

## 🎯 Objectives
- Connect to PostgreSQL using Python (`psycopg2`).
- Create a new database (`ALX_prodev`) if it does not already exist.
- Create a table `user_data` with the following fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Seed the database with values from `user_data.csv`.
- Test the setup by selecting and printing sample rows.

---

## 📂 Files in this Task
- **`seed.py`** → Contains helper functions to:
  - Connect to PostgreSQL
  - Create the database and table
  - Insert data from CSV
- **`0-main.py`** → Driver script to run the database setup.
- **`user_data.csv`** → Sample dataset used for seeding.
- **`README.md`** → This documentation.

---

## ⚙️ Requirements
- Python 3.x  
- PostgreSQL installed and running  
- Python library: [`psycopg2`](https://pypi.org/project/psycopg2/)  

Install psycopg2:
```bash
pip install psycopg2
