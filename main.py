from backup import db_dump
from restore import db_restore


if __name__ == '__main__':
    db_dump.dump(False)
    db_restore.restore(False)
