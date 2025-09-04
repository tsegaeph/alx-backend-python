#!/usr/bin/python3

from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database at a given offset.
    Returns a list of dictionaries.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        {"user_id": row[0], "name": row[1], "email": row[2], "age": row[3]}
        for row in rows
    ]


def lazy_pagination(page_size):
    """
    Generator that lazily yields each page of users one by one.
    Uses only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
