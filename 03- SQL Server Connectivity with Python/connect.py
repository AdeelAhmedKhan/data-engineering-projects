import os, logging
from pymssql import connect, Connection
from dotenv import load_dotenv


def create_connection() -> Connection | None:
    # read data from .env file
    load_dotenv()
    db_server   = "localhost"
    db_user     = "sa"
    db_password = "admin12345"
    db_name     = "new"

    # connect to the SQL Server
    try:
        conn = connect(server=db_server, user=db_user, password=db_password, database=db_name)
        return conn
    except Exception as e:
        logging.error(f'Error connecting to the SQL Server database: {e}')
        return None