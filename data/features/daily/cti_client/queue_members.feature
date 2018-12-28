Feature: Queue Member xlet

    Scenario: No selected queue
        Given there is a group with "2" users
        Given there is a call center supervisor:
         | firstname | lastname | cti_login | cti_passwd |
         | Bertrand  | Caron    | bertrand  | caron      |

        When I start the XiVO Client
        When I log in the XiVO Client as "bertrand", pass "caron"
        Then the Queue members xlet is empty

    Scenario: Enable and Disable Hide Unlogged Agents
        Given there is a call center supervisor:
         | firstname | lastname | cti_login | cti_passwd |
         | Etienne   | Lessard  | etienne   | lessard    |
        Given there are users with infos:
         | firstname | lastname          | number | context | protocol | agent_number |
         | Cédric    | Abunar            |   1202 | default | sip      | 1202         |
         | Sébastien | Duthil            |   1203 | default | sip      | 1203         |
         | Pascal    | Cadotte Michaud   |   1204 | default | sip      | 1204         |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | superqueue | SuperQueue   | 3006   | default | 1202,1203     |
         
        When I log agent "1204"
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
