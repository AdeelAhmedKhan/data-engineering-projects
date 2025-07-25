import logging
from connect import create_connection


def insert_author(first_name: str, last_name:str, birth_date:str) -> int | None:
    # Connect to the SQL Sever
    conn = create_connection()
    if conn is None:
        return None
    
    # Insert a new author
    with (conn, conn.cursor() as cursor):
        cursor.execute(
            "INSERT INTO Authors (FirstName, LastName, BirthDate) VALUES (%s, %s, %s)",
            (first_name, last_name, birth_date),
        )
        conn.commit()
        logging.info(f'Author: {first_name} {last_name} inserted successfully.')
        return cursor.lastrowid

