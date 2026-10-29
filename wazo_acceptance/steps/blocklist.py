from behave import given
from hamcrest import assert_that, has_entries


@given('the user "{firstname} {lastname}" has a blocklist with:')
def given_user_has_blocklist_with(context, firstname, lastname):
    context.table.require_columns(['label', 'number'])
    tracking_id = f"{firstname} {lastname}".strip()
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.confd_client, token):
        for row in context.table:
            body = {'number': row['number'], 'label': row['label']}
            context.confd_client.users.my_blocklist.numbers.create(body)


@given('tenant country is "{country}"')
def given_tenant_country_is(context, country):
    tenant_uuid = context.default_auth_tenant['uuid']
    body = {'country': country}
    context.confd_client.localization.update(body, wazo_tenant=tenant_uuid)
    tenant_info = context.confd_client.localization.get(wazo_tenant=tenant_uuid)
    assert_that(tenant_info, has_entries(country=country))
