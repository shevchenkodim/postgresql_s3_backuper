"""
Backup PostgreSQL database to DigitalOcean Storage, that has S3 compatible API.
"""
import os
from s3_spaces import s3_space
from utils import get_now_datetime_str
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_FILENAME


class DumpDatabase:
    def __init__(self, host, port, user, password, db_name, file_name):
        self.host = host
        self.port = port
        self.user = user
        self.db_name = db_name
        self.password = password
        self.file_name = file_name

    def dump(self, save_to_space=True):
        print("\U0001F4E6 Preparing database backup started")
        process_status = os.WEXITSTATUS(os.system(
            f"pg_dump -h {self.host} -p {self.port} -U {self.user} -w {self.password} -d {self.db_name} "
            f"--format=t --file='{self.file_name}'"
        ))
        if process_status != 0:
            exit(f"\U00002757 Dump database command exits with status {process_status}.")
        print("\U0001F510 DB dumped")
        if save_to_space:
            self.upload_dump_to_s3()

    def upload_dump_to_s3(self):
        print("\U0001F4C2 Starting upload to Storage")
        s3_space.upload_file(f'db-{get_now_datetime_str()}.tar', self.file_name)
        print("\U0001f680 Uploaded")


db_dump = DumpDatabase(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_FILENAME)
