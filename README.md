# SQL Validator
SQL Validator is a Python package that provides a simple and efficient way to validate SQL statements. The package uses the sqlparse module to parse SQL statements and check their validity against a given database schema.

## Features
Supports all major SQL dialects including PostgreSQL, MySQL, and SQLite
Validates SQL statements against a given database schema
Provides detailed error messages for easy debugging
Lightweight and easy to use
Installation
You can install SQL Validator using pip:

    shell
        Copy code
        pip install sql-validator
    
## Usage
To validate a SQL statement against a given database schema, simply create a Validator object and call its validate method:

    python
    Copy code
    from sql_validator import Validator
    
    validator = Validator(schema_path="path/to/schema.sql")
    is_valid = validator.validate("SELECT * FROM users;")
The schema_path parameter should point to a file containing the database schema in SQL format.

If the SQL statement is valid, validate will return True. Otherwise, it will raise a ValidationError with a detailed error message.

    python
    Copy code
    try:
        is_valid = validator.validate("SELECT name FROM users WHERE invalid_column = 42;")
    except ValidationError as e:
        print(e)
    Contributing
    Contributions to SQL Validator are welcome! If you would like to contribute, please open an issue or submit a pull request.

## License
SQL Validator is licensed under the MIT License. See LICENSE for more information.
