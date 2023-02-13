import os
import re
import logging
import cx_Oracle
from bs4 import BeautifulSoup
import sqlparse

import sqlparse

def validate_sql_syntax(sql_query):
    """
    it checks the type of statement and validates it further. For example, it checks if the 
    first token in the statement is 'SELECT' for a SELECT statement, 'UPDATE' for an UPDATE 
    statement, and so on. If the first token doesn't match the expected value, it raises an 
    exception.

    Parameters
    ----------
    sql_query : str
        SQL query to be validated.
    """
    try:
        parsed = sqlparse.parse(sql_query)
        #if len(parsed) > 1:
        #    raise Exception("Error: Multiple statements found in the query.")
        
        statement = parsed[0]
        if statement.get_type() not in ['SELECT', 'UPDATE', 'DELETE', 'INSERT', 'MERGE']:
            if statement.get_type() == 'BEGIN':
                return True
            else:
                raise Exception("Error: Unsupported statement type found.")
        
        if statement.get_type() == 'SELECT':
            if not statement.tokens or statement.tokens[0].value.upper() != 'SELECT':
                raise Exception("Error: Invalid SELECT statement.")
            
        elif statement.get_type() == 'UPDATE':
            if not statement.tokens or statement.tokens[0].value.upper() != 'UPDATE':
                raise Exception("Error: Invalid UPDATE statement.")
            
        elif statement.get_type() == 'DELETE':
            if not statement.tokens or statement.tokens[0].value.upper() != 'DELETE':
                raise Exception("Error: Invalid DELETE statement.")
            
        elif statement.get_type() == 'INSERT':
            if not statement.tokens or statement.tokens[0].value.upper() != 'INSERT':
                raise Exception("Error: Invalid INSERT statement.")
            
        elif statement.get_type() == 'MERGE':
            if not statement.tokens or statement.tokens[0].value.upper() != 'MERGE':
                raise Exception("Error: Invalid MERGE statement.")
        
        elif statement.get_type() == 'BEGIN':
            if not statement.tokens or statement.tokens[0].value.upper() != 'BEGIN':
                raise Exception("Error: Invalid BEGIN statement.")
        
        return True
    except Exception as e:
        print(f"{e}")
        return False



def get_awrr_info(filepath):
    """
    This function extracts the database name, database ID, and hostname from the HTML file.

    Parameters
    ----------
    filepath : str
        Path to the HTML file.
    """
    # Get the hostname of the machine
    with open(filepath, "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", attrs={"summary": "This table displays host information"})
    host_name = table.find("td", class_='awrnc').text

    # Read the HTML file
    with open(filepath, "r") as file:
        html = file.read()
        
    # Parse the HTML file
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find("table")

    # Iterate over the rows in the table
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells:
            db_name = cells[0].text
            db_id = cells[1].text
            print(f"DB Name: {db_name}, ID: {db_id}, HOSTNAME: {host_name}")
            
    return db_name, db_id, host_name

def pars_queries(filepath):
    """
    This function extracts the SQL statements from the HTML file and stores them in a list.

    Parameters
    ----------
    filepath : str
        Path to the HTML file.

    """
    # Open the HTML file
    with open(filepath, 'r') as file:
        content = file.read()

    # Find all instances of the SQL statements
    matches = re.findall(r'<pre_sqltext class="awr">(.*?)</pre_sqltext>', content, re.DOTALL)

    # Store the extracted SQL statements in a list
    sql_statements = []
    for sql_statement in matches:
        sql_statements.append(sql_statement)

    sql_statements = [item.replace('\n', '') for item in sql_statements]
    sql_statements = [item.replace('\t', '') for item in sql_statements]
    sql_statements = [item.strip() for item in sql_statements]

    for statement in sql_statements:
        print(validate_sql_syntax(statement))
    
    # Check the syntax of the SQL statements
        #logging.error(check_syntax(sql_statements))
      

def main():

    # Initialize the Oracle client
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_9")

    # Test to see if the cx_Oracle is recognized
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning(cx_Oracle.version)

    # This fails for me at this point but will succeed after the solution described below
    logging.warning(cx_Oracle.clientversion())

    # Get the AWR report information
    db_name, db_id, hostname = get_awrr_info("awrr/awrrpt_1_285_286.html")

    # Extract the SQL statements from the HTML file
    pars_queries("awrr/awrrpt_1_285_286.html")


if __name__ == '__main__':
    # Run the main function
    main()