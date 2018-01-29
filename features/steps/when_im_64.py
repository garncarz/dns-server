from behave import when


@when('we add IP "{ip}" as "{name}"')
def step_impl(context, ip, name):
    context.response = context.test.client.post(
        '/api/record/',
        {'ip': ip, 'name': name},
    )
