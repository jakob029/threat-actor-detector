import mysql.connector
import os
from getpass import getpass

DB_IP = input("Database server IP: ")
DATABASE = "ioc_apt_mapping"
USER = "remote_user"
PASSWORD = getpass()


class DbConnector:
    """Connector to the MYSQL database."""

    CURSOR = False

    def __init__(self, host, database, user, password):
        """Constructor

        Args:
            host: IP of the host system.
            database: Name of the database.
            user: SQL instance username.
            password: Password for the SQL user.
        """
        self.connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

    @property
    def connection_status(self):
        """SQL server connection status."""
        return self.connection.is_connected()

    def insert_apt(self, name: str, description: str, no_commit: bool = False):
        """Insert a new APT in the apt_table.

        name: Name of the APT.
        decription: Description of the APT.
        no_commit: Do not commit the selection instantly.
        """

        if not self.CURSOR:
            self.CURSOR = self.connection.cursor()

        self.CURSOR.execute(f'INSERT INTO apt_table (apt, description) VALUES ("{name}", "{description}");')
        if not no_commit:
            self.CURSOR.execute("COMMIT;")
            self.CURSOR.close()

    def multiple_insert_apts(self):
        """Gather APT:s from user cli input to insert."""
        apt = ""
        while True:
            print("--- Insert new APT ---")
            apt = input("APT name (q to quit): ")
            if apt == "q":
                break
            description = input("Description: ")
            self.insert_apt(apt, description)

        self.CURSOR.execute("COMMIT;")


i = DbConnector(DB_IP, DATABASE, USER, PASSWORD)
i.multiple_insert_apts()
