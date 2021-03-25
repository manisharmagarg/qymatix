from django.contrib.auth.models import User

from core.views.config_user import ConfigUser

user1 = {
    'email': 'test@clarus-films.com',
    'password': 'demo',
    'first_name': "Clarus",
    'last_name': "Films GmbH",
}



email = user1['email']
password = user1['password']
first_name = user1['first_name']
last_name = user1['last_name']

username = email.replace("@", "__")
username = username.replace(".", "_").replace("-", "___")

# user = User.objects.get(username=username)
# print(user)
# user, created = User.objects.get(pk=3)
users = User.objects.all()

for user in users:
    if user.username != 'admin' and user.is_active:
        print(user.username)
        config_user = ConfigUser(user)
        config_user.generate_token(password)

