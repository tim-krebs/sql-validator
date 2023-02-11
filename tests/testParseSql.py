import unittest
import mysql.connector
import cx_Oracle

from helper.sqlvalidation import *

class TestParseSQL(unittest.TestCase):
    def test_oracle_connection(self):
        sql = "SELECT 1 FROM DUAL"
        db_type = "oracle"
        host = "localhost"
        port = 1521
        user = "test_user"
        password = "test_password"
        database = "orcl"
        result = parse_sql(sql, db_type, host, port, user, password, database)
        self.assertEqual(result, "SQL statement parsed successfully")

    def test_mysql_connection(self):
        sql = "SELECT 1"
        db_type = "mysql"
        host = "localhost"
        port = 3306
        user = "test_user"
        password = "test_password"
        database = "test_db"
        result = parse_sql(sql, db_type, host, port, user, password, database)
        self.assertEqual(result, "SQL statement parsed successfully")

    def test_invalid_database_type(self):
        sql = "SELECT 1"
        db_type = "invalid"
        host = "localhost"
        port = 3306
        user = "test_user"
        password = "test_password"
        database = "test_db"
        with self.assertRaises(ValueError) as context:
            parse_sql(sql, db_type, host, port, user, password, database)
        self.assertEqual(str(context.exception), "Invalid database type: invalid. Only 'oracle' and 'mysql' are supported.")

if __name__ == '__main__':
    unittest.main()
