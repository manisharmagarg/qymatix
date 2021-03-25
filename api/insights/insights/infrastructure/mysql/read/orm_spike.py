# pylint: skip-file

import pandas as pd

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.customer_finder import CustomerFinder
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder

group_name = 'clarus___films_com'


def create_session(database_name):
    data_db = "data_{}".format(database_name)
    connection = MySqlConnection(data_db)
    return connection.session()


session = create_session(group_name)

customer_finder = CustomerFinder(session)

kam_finder = KamFinder(session)
# print(kam_finder.session)
# kam = kam_finder.get_kam_by_name('test__clarus___films_com')

# addr_vtr = {
#     'addr': ['SEPEC', 'BONG S.A.S  FR'],
#     'vtr': [1, 2]
# }

data = {
    251: [2, 4, 5, 6, 9, 10, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 61, 90],
    252: [2, 4, 5, 6, 9, 10, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 61, 90],
    253: [2, 4, 5, 6, 9, 10, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 61, 90],
    254: [2, 4, 5, 6, 9, 10, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 61, 90],
    255: [2, 4, 5, 6, 9, 10, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24, 61, 90],
    256: [3, 330, 530],
    257: [110, 112, 130],
    258: [80, 81, 82, 83, 85]
}

adrn_vtrn = pd.read_excel('/Users/martin/Downloads/VTR_Hart.xlsx')
adrn_vtrn = adrn_vtrn.dropna()
vtrn = adrn_vtrn['VTRN'].unique()
adrn = adrn_vtrn['ADRN'].unique()

adrn_vtrn['kam_id'] = adrn_vtrn['VTRN'].astype('int')

for kam_id, values in data.items():
    for vtrn_id in values:
        adrn_vtrn.loc[adrn_vtrn['kam_id'] == vtrn_id, 'kam_id'] = kam_id

for kam_id in data.keys():
    customers = adrn_vtrn[adrn_vtrn['kam_id'] == kam_id]['ADRN']
    kam = kam_finder.get_kam_by_id(kam_id)
    for customer_name in customers:
        customer = customer_finder.get_customer_by_name(customer_name)
        if customer is not None:
            kam.customers = kam.customers + [customer]

    session.add(kam)
    session.commit()

'''
c = customer_finder.get_customer_by_id(91067)

kam2 = kam_finder.get_kam_by_id(2)
print(kam2)

customers = kam2.customers
print(kam2.customers)
c = customer_finder.get_customer_by_id(91067)
print(c)
kam2.customers = kam2.customers + [c]
session.add(kam2)
session.commit()

customers = kam2.customers
print(customers)
'''

'''
group_finder = GroupFinder(session)
group1 = group_finder.get_group_by_name('Group 1')

groups = group_finder.get_group_by_owner(kam.id)

for group in groups:
    group.users = [kam2]
    session.add(group)
    session.commit()

print(groups)

print([c.id for c in kam.customers])
print(kam.groups)
print([user.id for user in group.users for group in groups])

kam_list = [kam]
customer_ids = [customer.id for k in kam_list for customer in k.customers]
# print(customers)
# customer_ids = [c.id for c in customers]
print(customer_ids)

# teams = Teams(kam)
# print(teams.get_teams())

# group = ReadGroups('clarus___films_com')


# print(group.get_groups([1]))
#
# print(group.get_groups('Group 2'))

'''
