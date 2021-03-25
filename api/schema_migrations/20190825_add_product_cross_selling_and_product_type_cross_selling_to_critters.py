# pylint: skip-file
import os
from pathlib import Path

from databases import Databases
from dotenv import load_dotenv
from playhouse.migrate import *

env_path = Path('/var/www/qyapp') / '.env_core'
load_dotenv(dotenv_path=env_path, verbose=True)

databases = Databases()
database_names = databases.get_names()

migrations = {
    'critters': [
        {
            'column': 'product_cross_selling',
            'field': TextField(default=''),
        },
        {
            'column': 'product_type_cross_selling',
            'field': TextField(default=''),
        },
    ]
}


def do_migrations():
    """
    Execute migrations.
    :return:
    Null
    """
    for d in database_names:
        database = MySQLDatabase(
            d,
            **{
                'charset': 'utf8',
                'use_unicode': True,
                'host': os.getenv('MYSQL_HOST'),
                'user': os.getenv('MYSQL_USER'),
                'password': os.getenv('MYSQL_PASSWORD')
            }
        )

        migrator = MySQLMigrator(database)

        # Create your field instances. For non-null fields you must specify a
        # default value.

        # Run the migration, specifying the database table, field name and field.
        try:
            for table, migration in migrations.items():
                try:
                    for m in migration:
                        migrate(
                            migrator.add_column(table, m['column'], m['field']),
                        )
                    print("Added column {} in table {}.{}".format(m['column'], d, table))
                except Exception as e:
                    print(d)
                    print(e)

        except Exception as e:
            print(e)
