# pylint: skip-file
"""
Migrations for alter(drop_not_null) the fields of tasks tables
"""
# pylint: disable=superfluous-parens
# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=broad-except
# pylint: disable=undefined-loop-variable

import os
from pathlib import Path

from databases import Databases
from dotenv import load_dotenv
from playhouse.migrate import MySQLDatabase, MySQLMigrator, migrate

databases = Databases()
database_names = databases.get_names()

ENV_PATH = Path('/var/www/qyapp') / '.env_core'
load_dotenv(dotenv_path=ENV_PATH, verbose=True)

MIGRATIONS = {
    'tasks': [
        {
            'column': 'plan',
        },
        {
            'column': 'account',
        },
        {
            'column': 'title',
        },
        {
            'column': 'description',
        },
        {
            'column': 'action',
        },
        {
            'column': 'due',
        },
        {
            'column': 'status',
        },
        {
            'column': 'end',
        },
        {
            'column': 'allday',
        },
        {
            'column': 'contact_id',
        },
    ]
}


def do_migrations():
    """
    Execute migrations.
    :return:
    Null
    """

    for db_name in database_names:
        database = MySQLDatabase(
            db_name,
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
            for table, migration in MIGRATIONS.items():
                try:
                    for columns_name in migration:
                        migrate(
                            migrator.drop_not_null(table, columns_name['column']),
                        )
                    print(
                        "Alter column {} in table {}.{}".format(
                            columns_name['column'],
                            db_name,
                            table
                        )
                    )
                except Exception as exp:
                    print(db_name)
                    print(exp)

        except Exception as exp:
            print(exp)
