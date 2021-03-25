from django.contrib.auth.models import User
from tokenapi.tokens import token_generator

#user = User.objects.get(username='Matthias_Binder__granzow_de')
#user.set_password('DoI$)20w8eh')

users = User.objects.all()

for user in users:
    if user.username != 'admin' and user.is_active:
        token = "{}:{}".format(user.pk, token_generator.make_token(user))
        user.configuration.token = token
        user.save()
