import importlib
import os
# import sys
import time
from stat import S_ISREG, ST_CTIME, ST_MODE

# Relative or absolute path to the directory
# DIR_PATH = sys.argv[1] if len(sys.argv) == 2 else r'.'

DIR_PATH = '/var/www/qyapp/api/schema_migrations'

# all entries in the directory w/ stats
data = (os.path.join(DIR_PATH, fn) for fn in os.listdir(DIR_PATH))
data = ((os.stat(path), path) for path in data)

# regular files, insert creation date
data = ((stat[ST_CTIME], path)
        for stat, path in data if S_ISREG(stat[ST_MODE]))

for cdate, path in sorted(data):
    if '__init__' in path or 'make_migrations' in path or 'databases' in path:
        continue

    # migration_file = path.split('.')[1][1:]
    migration_file = os.path.basename(path).split('.')[0]

    print("\n")
    print(migration_file)

    print('Running migration ... ' + time.ctime(cdate), os.path.basename(path))

    migration = importlib.import_module(migration_file)

    migration.do_migrations()
