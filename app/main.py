import os
import re
import csv
import openai
import logging
import cx_Oracle
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv



def check_sql_syntax(sql_statement):
    """
    This function checks the syntax of the SQL statement using the Codex model.

    Parameters
    ----------
    sql_statement : str
        SQL statement.

    """
    # Send the SQL statement to the Codex model
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Check the syntax of this SQL statement:\n{sql_statement}\n\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Check if the model generated any errors or warnings
    if "syntax error" in response.choices[0].text.lower():
        return False
    elif "warning" in response.choices[0].text.lower():
        return False
    else:
        return True

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
   
    # Check the syntax of the SQL statements
        #logging.error(check_syntax(sql_statements))

    return sql_statements

      
def file_writer(filepath, sql_statements):
    """
    This function writes the SQL statements to a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.
    sql_statements : list
        List of SQL statements.
    """
    # Write the SQL statements to a CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SQL Statement"])
        for sql_statement in sql_statements:
            writer.writerow([sql_statement])


def main():
    # Load the environment variables
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    awrr_file = "awrr/awrrpt_1_285_286.html"

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Initialize the Oracle client - not needed anymore
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_9")
    logging.warning(cx_Oracle.version)
    logging.warning(cx_Oracle.clientversion())

    # Get the AWR report information
    db_name, db_id, hostname = get_awrr_info(awrr_file)
    sql_statements = pars_queries(awrr_file)

    # Write the SQL statements to a CSV file
    file_name = db_name + "_" + db_id + "_" + hostname + ".csv"
    file_writer(file_name, sql_statements)

    # Classifies the SQL statements
    for sql_statement in sql_statements:
        logging.warning(check_sql_syntax(sql_statement))



if __name__ == '__main__':
    # Run the main function
    main()