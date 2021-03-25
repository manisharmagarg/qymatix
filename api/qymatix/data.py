# import datetime

from api.qymatix import addtables
from . import config
from . import upload
from .analysis import results


def createDataDatabases(dbname, local=False):
    '''
    '''
    config.dropDatabase(dbname='data_' + dbname, local=local)
    config.dropDatabase(dbname='results_' + dbname, local=local)
    config.createDatabase(dbname='data_' + dbname, local=local)
    config.createDatabase(dbname='results_' + dbname, local=local)


def createDataTables(dbname, local=False):
    '''
    '''
    addtables.createCustomersTable(dbname)
    addtables.createContactsTable(dbname)
    addtables.createProductTables(dbname)
    addtables.createSalesTable(dbname)


def createTasksDatabases(dbname, local=False):
    '''
    '''
    config.dropDatabase(dbname='data_' + dbname, local=local)
    config.createDatabase(dbname='data_' + dbname, local=local)


def createTasksTables(dbname, username, name="", local=False):
    '''
    '''
    config.createTasksTables(dbname, username, name)


def upload_data(data, dbname, from_line=None, to_line=None, local=False, append=False):
    '''
    '''
    if not append:
        print("Initializing databases...")
        createDataDatabases(dbname, local=local)
        createDataTables(dbname, local=local)
        print("Initializing databases...Done")

    print("Uploading data...")
    upload.xls2mysql(data=data, dbname=dbname, from_line=from_line, to_line=to_line, local=local)
    print("Running analysis...")
    # run_analysis(dbname)
    results(dbname)


if __name__ == "__main__":
    # dbname = 'ftest'
    # username = 'ftest'
    dbname = 'martinmasip_data_test_2015_2016_copy_super_reduced_xlsx'
    username = 'martinmasip'
    username = 'martin_masip'
    username = 'sapo_pepe'
    dbname = 'martinmasip'
    dbname = 'martin_masip'
    dbname = 'qymatix_best'
    local = True
    local = False

    dbname = 'coldjet_qy'
    username = 'robert_gruen'
    username = 'chancho_babe'
    dbname = 'qymatix_best'

    username = 'bob'
    username = 'alice'
    dbname = 'qy-test.com'.replace("-", "___").replace(".", "_")
    dbname = 'qymatix-solutions.com'.replace("-", "___").replace("@", "__").replace(".", "_")
    # dbname = 'qymatix_best'
    dbname = 'orbusneich_com'
    dbname = 'qymatix_best'
    # dbname = 'qy___test_com'
    # username = 'ep__mtm___ne_de'
    # dbname = 'mtm___ne_de'
    name = "Enrico Palma"

    createDataDatabases(dbname)
    createDataTables(dbname)

    createTasksDatabases(dbname)
    createTasksTables(dbname, username, name=name)

    # addtables.createUserGroupTable(dbname)
    # config.clear_table('data_' + dbname + '.sales')

    data = '/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017_reduced.xlsx'
    data = '/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017.xlsx'
    data = '/home/webuser/users/qymatix_best/data/201701-08_Sales_Analytics_OrbusNeich_adapted.xlsx'
    data = '/home/webuser/users/qymatix_best/data/201701-08_Sales_Analytics_OrbusNeich_with_Costs.xlsx'
    # data = '/home/webuser/users/qymatix___solutions_com/data/201701-08_Sales_Analytics_OrbusNeich_with_Costs_ordered.xlsx'
    data = '/home/webuser/users/qy___test_com/data/data_test_2016_17_groups_lp.xlsx'

    # upload_data(data, dbname, from_line=None, to_line=None, append=False)
    # upload_data(data, dbname, from_line=8940, to_line=8950, append=False)
    # upload_data(data, dbname, from_line=0, to_line=87, append=False)
