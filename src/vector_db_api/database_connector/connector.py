"""MySQL database connector for vector database dataset builder."""

from os import environ
import mysql.connector


class DbConnector:
    """Connector to the MYSQL database."""

    connection: mysql.connector.connection_cext.CMySQLConnection

    DB_IP: str = environ.get("MYSQL_HOST", default="100.77.88.30")
    USER: str = environ.get("MYSQL_USER")
    DATABASE: str = environ.get("MYSQL_DATABASE")
    PASSWORD: str = environ.get("MYSQL_PASSWORD")

    def __init__(self):
        """Constructor."""
        self.connection = mysql.connector.connect(
            host=self.DB_IP, database=self.DATABASE, user=self.USER, password=self.PASSWORD
        )

    @property
    def connection_status(self):
        """SQL server connection status."""
        return self.connection.is_connected()

    def fetch_ioc_mappings(self) -> list:
        """Fetch all IoC mapped to APTs and retrieve them in a defined format."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM ioc_table")

        fetched_results = cursor.fetchall()

        return self._construct_format(fetched_results)

    @staticmethod
    def _construct_format(fetched_results: list) -> list:
        """Construct a formatted list of IoC and APT pairs.

        Args:
            fetched_results: Result fetched in form of a list of tuples.

        Returns:
            Format [{"indicator": "<IOC>",
                     "type": "<IOC_TYPE>",
                     "apt": "<APT_GROUP_NAME"
                    }]
        """
        overview_list = []
        for element in fetched_results:
            if isinstance(element, tuple) and len(element) > 2:
                overview_list.append({"indicator": element[0], "type": element[1], "apt": element[2]})

        return overview_list

    def retrieve_specific_ioc(self, ioc: str) -> list:
        """Retrieve the information for a given IOC if it can be found in the database.

        Args:
            ioc: Specified IoC.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM ioc_table where IoC = '{ioc}'")

        fetched_results = cursor.fetchall()

        return fetched_results
