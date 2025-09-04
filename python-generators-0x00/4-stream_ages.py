#!/usr/bin/python3

from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for row in cursor.fetchall():
        yield row[0]  # only yield the age
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates the average age using the generator without loading all data into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # first loop over generator
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
