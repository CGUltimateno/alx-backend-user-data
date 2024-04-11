#!/usr/bin/env python3
"""
 a function that returns the log message obfuscated
"""
import os
import re
from typing import List, Tuple
import logging
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum
        """
        record.msg = filter_datum(self._fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
        returns the log message obfuscated
        """
    for field in fields:
        message = re.sub(f"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}",
                         message)
    return message


PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
        returns a logging.Logger object
        """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> List[Tuple[str, str, str]]:
    """
        returns a list of tuples
        """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = os.getenv("PERSONAL_DATA_DB_NAME")

    return (mysql.connector.connect(
        host=host,
        database=db,
        user=username,
        password=password)
    )


def main():
    """
        obtain a database connection using get_db
        and retrieve all rows in the users table
        """
    columns = ["name", "email", "phone", "ssn",
               "password", "ip", "last_login", "user_agent"]
    logger = get_logger()

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users;")
        for row in cursor:
            ___msg = ""
            ___col_index = 0
            for col in row:
                ___msg += f"{columns[___col_index]}={col}; "
                ___col_index += 1
            __msg = ___msg.strip()
            logger.info(___msg)
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
