"""
Renew database on current server.
Script download last dump from S3 DigitalOcean Storage, load it after clear current database state.
"""
import os
from s3_spaces import s3_space
from utils import remove_temp_files
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_FILENAME


class RestoreDatabase:

    def __init__(self, host, port, user, password, db_name, file_name):
        self.host = host
        self.port = port
        self.user = user
        self.db_name = db_name
        self.password = password
        self.file_name = file_name

    def restore(self, load_from_space):
        if load_from_space:
            last_file = self.get_last_backup_filename()
            self.download_s3_file(last_file)
        self.load_database()

    def get_last_backup_filename(self):
        backup_files = s3_space.list_files()
        backup_file = backup_files[-1]
        print(f"\U000023F3 Last backup in S3 is {backup_file['Key']}, "
              f"{round(backup_file['Size'] / (1024*1024))} MB download it")
        return backup_file['Key']

    def download_s3_file(self, filename: str):
        remove_temp_files(filename)
        s3_space.download_file(filename, self.file_name)
        print(f"\U0001f680 Downloaded")

    def load_database(self):
        print(f"\U0001F4A4 Database load started")
        operation_status = os.WEXITSTATUS(os.system(
            f"""pg_restore --dbname=postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name} 
                --clean {self.file_name}"""
        ))
        if operation_status != 0:
            exit(f"\U00002757 Can not load database, status {operation_status}.")
        print(f"\U0001F916 Database loaded")


db_restore = RestoreDatabase(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_FILENAME)
