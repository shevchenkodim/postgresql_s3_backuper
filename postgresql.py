import psycopg2
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME


class PostgreSQLServices:
    def __init__(self, host, port, user, password, db_name):
        self.connection = psycopg2.connect(f"dbname={db_name} "
                                           f"user={user} "
                                           f"password={password} "
                                           f"host='{host}' "
                                           f"port='{port}'")
        self.cursor = self.connection.cursor()


postgresql_services = PostgreSQLServices(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)
