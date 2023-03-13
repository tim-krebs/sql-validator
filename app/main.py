import os
import re
import csv
import openai
import logging
import platform
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def simplify_sql(sql_query):
    # Set up the OpenAI API client
    prompt = f"Simplify the following SQL query to visualize:\n\n{sql_query}\n\n"

    # Call the OpenAI API to generate the simplified query
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the simplified query from the API response
    simplified_query = response.choices[0].text.strip()

    return simplified_query


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def check_sql_syntax(sql_statement, completion_length=1024):
    """
    This function checks the syntax of the SQL statement using the Codex model.
    Parameters
    ----------
    sql_statement : str
        SQL statement.
    completion_length : int
        Number of tokens to generate.
    """

    ## Send the SQL statement to the Codex model
    #response = openai.Completion.create(
    #    engine="davinci-codex",
    #    prompt=f"Check the syntax of this SQL statement:\n{sql_statement}\n\n",
    #    max_tokens=1024,
    #    n=1,
    #    stop=None,
    #    temperature=0.5,
    #)

    try:
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Check the syntax of this SQL statement:\n{sql_statement}\n\n",
            max_tokens=completion_length,
            n=1,
        )
        # Check if the model generated any errors or warnings
        if "syntax error" in response.choices[0].text.lower():
            return f"Syntax Error: {sql_statement}"
        elif "warning" in response.choices[0].text.lower():
            return f"Warning: {sql_statement}"
        else:
            return True

    except openai.error.InvalidRequestError as e:
        if "parameter 'max_tokens' must be at most" in str(e):
            max_context_length = 4096 - completion_length
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=f"Check the syntax of this SQL statement:\n{sql_statement}\n\n"[-max_context_length:],
                max_tokens=completion_length,
                n=1,
                temperature=0.7,
            )
            # Check if the model generated any errors or warnings
            if "syntax error" in response.choices[0].text.lower():
                return f"Syntax Error: {sql_statement}"
            elif "warning" in response.choices[0].text.lower():
                return f"Warning: {sql_statement}"
            else:
                return True
        else:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Is the following SQL statement valid?\n\n{sql_statement}\n\nAnswer:",
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                answer = response.choices[0].text.strip()
                if answer.lower() == "yes":
                    return True
                else:
                    if "syntax error" in response.choices[0].text.lower():
                        return f"Syntax Error: {sql_statement}"
                    elif "warning" in response.choices[0].text.lower():
                        return f"Warning: {sql_statement}"

            except openai.error.InvalidRequestError as e:
                if "parameter 'max_tokens' must be at most" in str(e):
                    max_context_length = 4096 - completion_length
                    response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=f"Is the following SQL statement valid?\n\n{sql_statement}\n\nAnswer:"[-max_context_length:],
                        max_tokens=completion_length,
                        n=1,
                        temperature=0.7,
                    )
                    answer = response.choices[0].text.strip()
                    if answer.lower() == "yes":
                        return True
                    else:
                        if "syntax error" in response.choices[0].text.lower():
                            return f"Syntax Error: {sql_statement}"
                        elif "warning" in response.choices[0].text.lower():
                            return f"Warning: {sql_statement}"
                else:
                    return f"Error: {sql_statement}"

    ## Check if the model generated any errors or warnings
    #if "syntax error" in response.choices[0].text.lower():
    #    return f"Syntax Error: {sql_statement}"
    #elif "warning" in response.choices[0].text.lower():
    #    return f"Warning: {sql_statement}"
    #else:
    #    return True

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
    sql_statements = [item.replace('&quot', '') for item in sql_statements]
    sql_statements = [item.strip() for item in sql_statements]

    # Check the syntax of the SQL statements
        #logging.error(check_syntax(sql_statements))

    return sql_statements

def remove_comments(sql_statements):
    # Remove all comments starting with "/*" and ending with "*/"
    cleared_sql = []
    for item in sql_statements:
        sql = re.sub(r"/\*.*?\*/", "", item, flags=re.DOTALL)
        cleared_sql.append(sql)

    return cleared_sql

def file_writer(folder, filepath, sql_statements):
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
    with open(folder+"/"+filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for sql_statement in sql_statements:
            writer.writerow([sql_statement])


def main():
    # Load the environment variables
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    awrr_file = "data/awrrpt_1_285_286.html"

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Get the AWR report information
    db_name, db_id, hostname = get_awrr_info(awrr_file)
    sql_statements = pars_queries(awrr_file)

    # Simplify the SQL statements

    file_name = db_name + "_" + db_id + "_" + hostname + "_valid.csv"
    simplified_query = []
    for sql_statement in sql_statements:
        simplified_query.append(simplify_sql(sql_statement))
        simplified_query = [item.replace('&lt', '<') for item in simplified_query]
        simplified_query = [item.replace('&gt', '>') for item in simplified_query]
        simplified_query = [item.strip('# * \n`')    for item in simplified_query]

    sql_statements = remove_comments(sql_statements)
    #file_writer("simplified",file_name, simplified_query )
    #logging.warning("Simplified SQL statements written to file")

    # Classifies the SQL statements
    valid_statements = []
    for sql_statement in sql_statements:

        if check_sql_syntax(sql_statement):
            logging.warning(f"SQL statement is valid: {sql_statement}")
            valid_statements.append(sql_statement)

        else:
            logging.error(f"SQL statement is invalid: {sql_statement}")

    # Write the valid SQL statements to a CSV file
    file_name = db_name + "_" + db_id + "_" + hostname + "_valid.csv"
    file_writer("results", file_name, valid_statements)
    print("Valid SQL statements written to file")


if __name__ == '__main__':
    # Run the main function
    main()
