import logging, sys
from connect import create_connection
from insert import insert_author
from import_author import import_author_from_csv
from bulk import bulk_copy_customers

# config logging to console
logging.basicConfig(
    stream=sys.stdout, 
    encoding='utf-8', 
    format='%(levelname)s:%(message)s',
    level=logging.DEBUG
)

# Create Authors table if it does not exist
create_table_query = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Authors' AND xtype='U')
CREATE TABLE Authors (
    AuthorID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    BirthDate DATE
);
"""

connection = create_connection()
if connection is None:
    logging.error("Failed to create a database connection.")
    sys.exit(1)
cursor = connection.cursor()

try:
    cursor.execute(create_table_query)
    connection.commit()
    logging.info("Authors table checked/created successfully.")
except Exception as e:
    logging.error(f"Error occurred while creating Authors table: {e}")
    connection.rollback()
finally:
    cursor.close()
connection.close()

# # insert a new author manually
# id = insert_author('Alice', 'Johnson', '1978-05-14');
# if id is not None:
#     logging.info(f'Author ID: {id}')

# import from csv
import_author_from_csv('./data/authors.csv')

# bulk import from bulk
# bulk_copy_customers('./data/customers.csv')
