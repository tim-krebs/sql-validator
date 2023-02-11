import sqlparse
import mysql.connector
import cx_Oracle

# Oracle DB
# Virtual-Machine-Name: Oracle-DB
# username: azureuser
# password: Azure123456789

# This function that takes a SQL query string as an argument and 
# returns a message indicating whether the query is valid or not for both Oracle and MySQL databases:
def check_sql_syntax(query):
    """
    Check if SQL query is valid for Oracle and MySQL databases.

    :param query: SQL query to check syntax for
    
    You'll need to replace username, password, oracle_sid, hostname, 
    and database with the appropriate values for your Oracle and MySQL 
    databases.
    """
    is_oracle_valid = False
    is_mysql_valid = False
    
    try:
        # Connect to Oracle database and check syntax
        conn = cx_Oracle.connect("username", "password", "oracle_sid")
        cursor = conn.cursor()
        cursor.execute(query)
        is_oracle_valid = True
    except cx_Oracle.DatabaseError as e:
        print("Oracle Error:", e)
        
    try:
        # Connect to MySQL database and check syntax
        conn = mysql.connector.connect(user='username', password='password', host='hostname', database='database')
        cursor = conn.cursor()
        cursor.execute(query)
        is_mysql_valid = True
    except mysql.connector.Error as e:
        print("MySQL Error:", e)
        
    if is_oracle_valid and is_mysql_valid:
        return "Query is valid for both Oracle and MySQL databases."
    elif is_oracle_valid:
        return "Query is only valid for Oracle database."
    elif is_mysql_valid:
        return "Query is only valid for MySQL database."
    else:
        return "Query is not valid for either Oracle or MySQL databases."



#   sql: The SQL statement to be parsed.
#   db_type: The type of database, either oracle or mysql.
#   host, port, user, password, and database: Connection details for the database.

#   The function establishes a connection to the database, creates a cursor, and executes the SQL statement. 
#   If the statement is parsed successfully, it prints a message indicating success. If an error occurs while 
#   parsing the statement, it raises an exception and prints an error message. The function also includes a 
#   finally block to close the cursor and the connection, regardless of whether an exception was raised or not.
def parse_sql(sql, db_type, host, port, user, password, database):
    """
    Parse SQL statement and return results.

    :param sql: SQL statement to parse
    :param db_type: Database type. Only 'oracle' and 'mysql' are supported.
    :param host: Database host
    :param port: Database port
    :param user: Database user
    :param password: Database password
    :param database: Database name
    """
    try:
        if db_type == "oracle":
            connection = cx_Oracle.connect(f"{user}/{password}@{host}:{port}/{database}")
            cursor = connection.cursor()
            cursor.execute(sql)
            print("SQL statement parsed successfully")
        elif db_type == "mysql":
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            cursor = connection.cursor()
            cursor.execute(sql)
            print("SQL statement parsed successfully")
        else:
            raise ValueError(f"Invalid database type: {db_type}. Only 'oracle' and 'mysql' are supported.")
    except cx_Oracle.DatabaseError as e:
        print(f"An error occurred while parsing the SQL statement: {e}")
    except mysql.connector.Error as e:
        print(f"An error occurred while parsing the SQL statement: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def validate_sql(sql_string):
    """
    Validate SQL statement.

    :param sql_string: SQL statement to validate
    """
    try:
        parsed = sqlparse.parse(sql_string)[0]
        return True
    except sqlparse.exceptions.SQLParseError:
        return False



