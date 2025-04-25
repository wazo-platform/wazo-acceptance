from behave import given, step, then
from hamcrest import assert_that, contains_inanyorder, has_entries


# e.g. When the user "Charlie Unknown" adds number "+15555555555" with label "bad" to their blocklist
@step('the user "{firstname} {lastname}" adds number "{number}" with label "{label}" to their blocklist')
def step_user_adds_number_with_label_to_blocklist(context, firstname, lastname, number, label):
    tracking_id = f"{firstname} {lastname}".strip()
    # get user token
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.confd_client, token):
        context.confd_client.users.my_blocklist.numbers.create(dict(
            number=number,
            label=label,
        ))


@given('the user "{firstname} {lastname}" has a blocklist with')
def given_user_has_blocklist_with(context, firstname, lastname):
    context.table.require_columns(['label', 'number'])
    tracking_id = f"{firstname} {lastname}".strip()
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.confd_client, token):
        for row in context.table:
            context.confd_client.users.my_blocklist.numbers.create(dict(
                number=row['number'],
                label=row['label'],
            ))


@then('the user "{firstname} {lastname}" has a blocklist with')
def step_user_has_blocklist_with(context, firstname, lastname):
    context.table.require_columns(['label', 'number'])
    expected_blocklist = [row.as_dict() for row in context.table]
    tracking_id = f"{firstname} {lastname}".strip()
    user_token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.confd_client, user_token):
        blocklist = context.confd_client.users.my_blocklist.numbers.list()
        assert_that(blocklist, has_entries(
            items=contains_inanyorder(
                *(
                    has_entries(blocked_number)
                    for blocked_number in expected_blocklist
                )
            ),
            total=len(expected_blocklist),
        ))


@given('tenant country is "{country}"')
def given_tenant_country_is(context, country):
    tenant_uuid = context.default_auth_tenant['uuid']
    context.confd_client.localization.update(dict(
        country=country
    ), wazo_tenant=tenant_uuid)
    tenant_info = context.confd_client.localization.get(wazo_tenant=tenant_uuid)
    assert_that(tenant_info, has_entries(
        country=country
    ))
