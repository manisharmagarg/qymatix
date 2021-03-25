import requests
from ast import literal_eval


def basic_call(function, data='', local=True):
    '''
    '''
    if local:
        token = '88:4ex-b4b2933da912f71314c5'
        server = '192.168.56.102'
    else:
        token = '88:4ew-38d1221bab855964163c'
        server = 'www.qymatix.com'

    url = 'https://{}/api-v0.1.0/{}/{}'.format(server, token, function)

    if data != '':
        url = url + '/' + str(data)

    ans = requests.get(url, verify=False)
    try:
        return ans.json()
    except:
        return ans.text


def basic_post(function, data='', local=True):
    '''
    '''
    if local:
        token = '88:4ex-b4b2933da912f71314c5'
        server = '192.168.56.102'
    else:
        token = '88:4ew-38d1221bab855964163c'
        server = 'www.qymatix.com'

    url = 'https://{}/api-v0.1.0/{}/{}'.format(server, token, function)

    if data != '':
        url = url + '/' + str(data)

    ans = requests.post(url, verify=False)
    try:
        return ans.json()
    except:
        return ans.text


def test_getActions(customer=''):
    '''
    '''
    func = 'getactions'
    ans = basic_call(func, data=customer)
    return ans


def test_setAction(data=''):
    '''
    '''
    func = 'setAction'
    ans = basic_post(func, data=data)
    return ans


def test_deleteAction(data=''):
    '''
    '''
    func = 'deleteAction'
    ans = basic_post(func, data=data)
    return ans


def test_getPlans(customer=''):
    '''
    '''
    func = 'getplans'
    ans = basic_call(func, data=customer, local=True)
    return ans


def test_modifyCustomer(data=''):
    '''
    '''
    func = 'modifyCustomer'
    ans = basic_post(func, data=data)
    return ans


def test_getCustomers(customer=''):
    '''
    '''
    func = 'getcustomers'
    ans = basic_call(func, data=customer)
    return ans


def test_getKam(kam=''):
    '''
    '''
    func = 'getKam'
    ans = basic_call(func, data=kam)
    return ans


def modifyCustomer():
    '''
    '''
    kams = test_getKam()

    customer = "Metro"
    metro = {}
    metro['data'] = test_getCustomers(customer)
    metro['actions']= test_getActions(customer)

    print(metro['data']['kam'])
    print(metro['data']['industry'])
    #print(kams)

    data = {'id':756, 'kam_id':680}
    data = {'id':756, 'kam_id':31}
    data = {'id':756, 'industry':31}
    data = {'id':756, 'industry':'Retail'}
    data = {
        "id":756,
        "address":"",
        "city":"Trier",
        "country":"Germany",
        "kam_id":13,
        "postcode": 11111,
        "revenue": 1000,
        "employees": 100,
        "industry": "Energy",
        "classification": "Seller",
        "website": "website.com",
        "comment": "comment",
        "favorite": 0
    }
    data = {'id':756, 'kam_id':13}
    ans = test_modifyCustomer(data)
    metro['data'] = test_getCustomers(customer)

    print(ans)
    #print(ans[9000:12000])
    print(">>>>")
    print(metro['data']['kam'])
    print(metro['data']['industry'])


def deleteAction():
    '''
    '''
    actions = test_getActions('Metro')
    print(actions.keys())
    print(actions['Metro'])
    test_deleteAction(38)
    actions = test_getActions('Metro')
    print(actions.keys())
    print(actions['Metro'])


def test_unlinkPlanFromAction(data=''):
    '''
    '''
    func = 'unlinkPlanFromAction'
    ans = basic_post(func, data=data)
    return ans

def test_linkPlanToAction(data=''):
    '''
    '''
    func = 'linkPlanToAction'
    ans = basic_post(func, data=data)
    return ans



if __name__ == "__main__":

    plans = test_getPlans()
    #print(plans[8000:10000])
    print(plans)
    #print(plans.keys())
    
    #data = [6, 23]
    #data = [2, 18]
    #data = [4, 16]
    #ans = test_unlinkPlanFromAction(data)
    #test_linkPlanToAction(data)

    #modifyCustomer()



