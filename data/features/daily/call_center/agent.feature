Feature: Agent

    Scenario: Add an agent with first name and last name and remove it
        When I create an agent "Aaliyah" "Stuart" "23000"
        Then agent "Aaliyah Stuart" is displayed in the list of "default" agent group
        When I remove agent "Aaliyah" "Stuart"
        Then agent "Aaliyah Stuart" is not displayed in the list of "default" agent group

    Scenario: Agent modification
        Given there is a agent "John" "Wayne" with number "24000"
        Then the agent "24000" password is ""
        When I change the agent "24000" password to "8888"
        Then the agent "24000" password is "8888"

    Scenario: Agent search
        Given there is a agent "Il" "buono" with number "24001"
        Given there is a agent "Il" "brutto" with number "24002"
        Given there is a agent "Il" "cattivo" with number "24003"
        When I search an agent "24002"
        Then agent "24002" is displayed in the list of "default" agent group
        When I search an agent "cattivo"
        Then agent "cattivo" is displayed in the list of "default" agent group

    Scenario: Agent group
        When I create an agent group "blue"
        Then agent group "blue" is displayed in the list
        When I create an agent "Bisounours" "Red" "24500" in group "blue"
        Then agent "24500" is displayed in the list of "blue" agent group
        Then agent group "blue" has "1" agents
        When I create an agent group "black"
        When I create an agent "bobi" "cash" "26000" in group "black"
        When I create an agent "toto" "bobo" "26001" in group "black"
        Then agent group "black" has "2" agents
        When I remove agent group "blue"
        Then agent group "blue" is not displayed in the list
        When I create an agent group "green"
        Then agent group "green" is displayed in the list
        When I select a list of agent group "black, green"
        When I remove selected agent group
        Then agent group "black" is not displayed in the list
        Then agent group "green" is not displayed in the list

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
