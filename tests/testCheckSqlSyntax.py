import unittest
import mysql.connector
import cx_Oracle

from helper.sqlvalidation import *


class TestCheckSQLSyntax(unittest.TestCase):
    def test_valid_query(self):
        query = "SELECT 1"
        result = check_sql_syntax(query)
        self.assertEqual(result, "Query is valid for both Oracle and MySQL databases.")

    def test_invalid_query(self):
        query = "INVALID SQL STATEMENT"
        result = check_sql_syntax(query)
        self.assertEqual(result, "Query is not valid for either Oracle or MySQL databases.")

    def test_oracle_valid_mysql_invalid(self):
        query = "SELECT * FROM DUAL"
        result = check_sql_syntax(query)
        self.assertEqual(result, "Query is only valid for Oracle database.")

    def test_mysql_valid_oracle_invalid(self):
        query = "SHOW TABLES"
        result = check_sql_syntax(query)
        self.assertEqual(result, "Query is only valid for MySQL database.")

if __name__ == '__main__':
    unittest.main()
