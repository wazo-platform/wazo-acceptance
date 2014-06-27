Feature: Queue Member xlet

    Scenario: No selected queue
        Given there is a group with "2" users
        Given there is a call center supervisor "Bertrand" "Caron"

        When I start the XiVO Client
        When I log in the XiVO Client as "bertrand", pass "caron"
        Then the Queue members xlet is empty

    Scenario: Enable and Disable Hide Unlogged Agents
        Given there is a call center supervisor "Etienne" "Lessard"
        Given there is a queue "SuperQueue" with number "3006" in "default" and unlogged members:
         | firstname | lastname | number | context | protocol |
         | Cédric    | Abunar   |   1202 | default | sip      |
         | Sébastien | Duthil   |   1203 | default | sip      !
        Given there is a logged agent "Pascal" "Cadotte Michaud" with number "1204" in "default"
        When I start the XiVO Client
        When I enable the hide unlogged agents option
        When I log in the XiVO Client as "etienne", pass "lessard"
        Then the Queue members xlet for queue "superqueue" is empty

        When I log agent "1202"
        Then the Queue members xlet for queue "superqueue" should display agents:
         | number |
         |   1202 |

        When I unlog agent "1202"
        Then the Queue members xlet for queue "superqueue" is empty

        When I add agent "1204" to "superqueue"
        Then the Queue members xlet for queue "superqueue" should display agents:
         | number |
         |   1204 |

        When I remove agent "1204" from "superqueue"
        Then the Queue members xlet for queue "superqueue" is empty

        When I disable the hide unlogged agents option
        Then the Queue members xlet for queue "superqueue" should display agents:
         | number |
         |   1202 |
         |   1203 |
