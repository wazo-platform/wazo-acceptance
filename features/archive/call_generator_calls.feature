Feature: Call Generation

    Scenario: Bus messages on hold and resume
        Given I listen on the bus for messages:
        | queue | routing_key  |
        | test  | calls.hold.# |
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Marty     | McFly    |   1001 | default | sip      |
        | George    | McFly    |   1002 | default | sip      |
        Given "Marty McFly" calls "1002"
        Given "George McFly" answers
        When "George McFly" puts his call on hold
        Then I receive a "call_held" on the queue "test" with data:
        | call_id | origin_uuid | user_uuid |
        | ANY     | yes         | ANY       |
        When "George McFly" resumes his call
        Then I receive a "call_resumed" on the queue "test" with data:
        | call_id | origin_uuid | user_uuid |
        | ANY     | yes         | ANY       |

    Scenario: Transfer timeout is respected
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Marty     | McFly    |   1001 | default | sip      |
        | George    | McFly    |   1002 | default | sip      |
        | Zzyxz     | Axalotl  |   1003 | default | sip      |
        Given "Marty McFly" calls "1002"
        Given "George McFly" answers
        When "George McFly" transfers "Marty McFly" to "1003" with timeout "3" via xivo-ctid-ng
        Then "Zzyxz Axalotl" is ringing
        When I wait 4 seconds
        Then "Zzyxz Axalotl" is hungup
