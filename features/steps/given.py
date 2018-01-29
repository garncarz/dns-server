from behave import given
from constance import config
from constance.test import override_config
from django.contrib.auth.models import User


@given('the root domain is "{root_domain}"')
def step_impl(context, root_domain):
    override_config(DOMAIN=root_domain)


@given('there\'s {role} "{login}" with password "{password}"')
def step_impl(context, role, login, password):
    if role == 'admin':
        email = f'{login}@{config.DOMAIN}'
        User.objects.create_superuser(username=login,
                                      email=email,
                                      password=password)
    elif role == 'user':
        User.objects.create_user(username=login,
                                 password=password)
    else:
        raise NotImplementedError(f'Unknown role: {role}')


@given('we\'re logged in as "{login}" with password "{password}"')
def step_impl(context, login, password):
    context.test.client.login(username=login, password=password)
