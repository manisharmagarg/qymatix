from core.views.config_user import ConfigUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User




user1 = {
    'email': 'lucas.pedretti@qymatix.com',
    'password': 'demo',
    'first_name': "Lucas",
    'last_name': "Pedretti",
}

email = user1['email']
password = user1['password']
first_name = user1['first_name']
last_name = user1['last_name']

username = email.replace("@", "__")
username = username.replace(".", "_").replace("-", "___")

user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
user.set_password(password)
user.save()
print("User {} saved.".format(email))

config_user = ConfigUser(user)
config_user.generate_token(password)
config_user.create_group()
config_user.user_plan_and_account(plan='basic', account_type='admin')
print("User {} configured.".format(email))




user2 = {
    'email': 'paul@qy-test.com',
    'password': 'demo',
    'first_name': "Paul",
    'last_name': "Dirac",
}

email = user2['email']
password = user2['password']
first_name = user2['first_name']
last_name = user2['last_name']

username = email.replace("@", "__")
username = username.replace(".", "_").replace("-", "___")

user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
user.set_password(password)
user.save()
print("User {} saved.".format(email))

config_user = ConfigUser(user)
config_user.generate_token(password)
config_user.create_group()
config_user.user_plan_and_account(plan='crm', account_type='admin')
print("User {} configured.".format(email))

