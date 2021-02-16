Feature: Call Generation

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
