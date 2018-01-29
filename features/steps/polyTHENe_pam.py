from behave import then

from dns import models


@then('status code is {code:d}')
def step_impl(context, code):
    context.test.assertEqual(context.response.status_code, code)


@then('there\'s {count:d} record for IP "{ip}" and name "{name}"')
def step_impl(context, count, ip, name):
    context.test.assertEqual(
        count,
        models.Record.objects.filter(ip=ip, name=name).count(),
    )
