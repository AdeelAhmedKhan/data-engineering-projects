from connect import create_connection
from utils import read_csv


def bulk_copy_customers(filename:str) -> bool:
    customers = read_csv(filename)
    if not customers:
        return False
    
    conn = create_connection()
    if conn is None:
        return False
    
    with conn:
        conn.bulk_copy('Customers',customers)
        conn.commit()

    return True   