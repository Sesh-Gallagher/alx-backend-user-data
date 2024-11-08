#!/usr/bin/env python3
"""
Module for a  function called filter_datum
that returns the log message obfuscated
"""
import re
import logging
import os
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """
    Represents the redacting Formatter class module
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Module to redact the message of LogRecord instance
        Args:record (logging.LogRecord): LogRecord
        instance containing message
        Return: formatted string
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Module that returns an obfuscated log message
    Args: fields (list): list of strings indicating fields to obfuscate
          redaction (str): what the field will be obfuscated to
          message (str): the log line to obfuscate
          separator (str): the character separating the fields
    """
    for f in fields:
        message = re.sub(f+'=.*?'+separator,
                         f+'='+redaction+separator, message)
    return message


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Module that returns a connector to a MySQL database
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    cnxn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return cnxn


def get_logger() -> logging.Logger:
    """
    Module that returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def main():
    """
    Represents main entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names

    for row in cursor:
        message = "".join("{}={}; ".format(i, j) for i, j in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
