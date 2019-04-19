Feature: Agent

    Scenario: Agent login status update events
        Given there is no agents logged
        Given there are users with infos:
        | firstname | lastname | number | context     | agent_number | protocol |
        | User      |      003 |   1003 | statscenter |         1003 | sip      |
        Given there are queues with infos:
        | name     | number | context     | agents_number |
        | thequeue |   5010 | statscenter |          1003 |
        Given I listen on the bus for messages:
        | queue             | routing_key  |
        | test_status_agent | status.agent |
        When I log agent "1003"
        Then I receive a "agent_status_update" on the queue "test_status_agent" with data:
        | agent_id | agent_number | status    | xivo_uuid |
        | yes      |         1003 | logged_in | yes       |

    Scenario: Login and logout an agent from the phone
        Given there are users with infos:
        | firstname | lastname | number | context     | agent_number | protocol |
        | User      |      003 |   1003 | statscenter |         1003 | sip      |
        When I log agent "1003" from the phone
        Then the agent "1003" is logged
        When I unlog agent "1003" from the phone
        Then the agent "1003" is not logged

    Scenario: Mandatory token authentication for xivo-agentd
        When I request the agent statuses with an invalid token
        Then I get an "invalid token" response from xivo-agentd
