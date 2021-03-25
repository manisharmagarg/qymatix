from django.contrib.auth.models import User

from core.views.config_user import ConfigUser

user1 = {
    'email': 'Bernhard.Festner@hartl-online.de',
    'password': 'demo',
    'first_name': "Bernhard",
    'last_name': "Festner",
}


email = user1['email']
password = user1['password']
first_name = user1['first_name']
last_name = user1['last_name']

username = email.replace("@", "__")
username = username.replace(".", "_").replace("-", "___")

user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)

if created:
    user.set_password(password)
    user.save()
    print("User {} saved.".format(email))
else:
    print("User {} already exists.".format(email))

config_user = ConfigUser(user)

config_user.generate_token(password)
config_user.create_group()
config_user.user_plan_and_account(plan='advanced', account_type='admin')

config_user.create_databases()
config_user.create_tables()

print("User {} configured.".format(email))

