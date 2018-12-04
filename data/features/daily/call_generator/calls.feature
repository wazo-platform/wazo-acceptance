Feature: Callgen

    Scenario: Call to inexistant extension
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     |          | 1100   | default | sip      |
        When "Alice" calls "1190"
        Then "Alice" last dialed extension was not found

    Scenario: Call to existant extension with answer
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     |          |   1100 | default | sip      |
         | Bob       |          |   1101 | default | sip      |
        When a call is started:
         | caller | dial | callee | talk_time | hangup |
         | Alice  | 1101 | Bob    | 3         | callee |
        Then I have the last call log matching:
         | destination_extension | duration | answered |
         | 1101                  | 3        | True     |

    Scenario: Call with extension call recording activated
        Given the "Call recording" extension is enabled
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 100      |   1100 | default | sip      |
         | User      | 101      |   1101 | default | sip      |
        When a call is started:
         | caller   | dial | callee   | talk_time | hangup |
         | User 100 | 1101 | User 101 | 3         | callee |
        Then I see no recording file of this call in monitoring audio files page

    Scenario: Call to line that is disabled
        Given there are users with infos:
            | firstname | lastname | number | context | protocol |
            | Bountrabi | Sylla    | 1102   | default | sip      |
            | Papa      | Sylla    | 1103   | default | sip      |
        Given the line "1103@default" is disabled
        When "Bountrabi Sylla" calls "1103"
        Then "Bountrabi Sylla" last dialed extension was not found

    Scenario: No answer destination with disabled forward exten on no answer
        Given the "Enable forwarding on no-answer" extension is disabled
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | James     | Bond     |   1101 | default | sip      |
        | Tiffany   | Case     |   1102 | default | sip      |
        | Pussy     | Galore   |   1103 | default | sip      |
        Given "James Bond" has a "5" seconds ringing time
        Given "James Bond" has a dialaction on "No answer" to "User" "Pussy Galore"
        When "Tiffany Case" calls "1101"
        Then "James Bond" is ringing
        When I wait 9 seconds
        Then "Pussy Galore" is ringing

    Scenario: Busy destination with disabled forward exten on busy
        Given the "Enable forwarding on busy" extension is disabled
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | James     | Bond     |   1101 | default | sip      |
        | Honey     | Ryder    |   1102 | default | sip      |
        | Sylvia    | Trench   |   1103 | default | sip      |
        Given "James Bond" has a dialaction on "Busy" to "User" "Sylvia Trench"
        When "Honey Ryder" calls "1101"
        When "James Bond" is ringing
        When "James Bond" hangs up
        When I wait 2 seconds
        Then "Sylvia Trench" is ringing

    Scenario: Check that new calls are not marked as on_hold when GETTING calls
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Oliver    | Queen    |   1001 | default | sip      |
        | Thea      | Queen    |   1002 | default | sip      |
        Given "Oliver Queen" calls "1002"
        Given "Thea Queen" answers
        Then "Oliver Queen" call "on_hold" is "False"
        Then "Thea Queen" call "on_hold" is "False"

    Scenario: Call on hold are marked as on_hold when GETTING calls
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Bruce     | Wayne    |   1001 | default | sip      |
        | Clark     | Kent     |   1002 | default | sip      |
        Given "Bruce Wayne" calls "1002"
        Given "Clark Kent" answers
        When "Clark Kent" puts his call on hold
        Then "Clark Kent" call "on_hold" is "True"
        Then "Bruce Wayne" call "on_hold" is "False"

    Scenario: Resumed calls are not marked as on_hold when GETTING calls
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Maggie    | Greene   |   1001 | default | sip      |
        | Rick      | Grimes   |   1002 | default | sip      |
        Given "Maggie Greene" calls "1002"
        Given "Rick Grimes" answers
        When "Maggie Greene" puts her call on hold
        When "Maggie Greene" resumes her call
        Then "Maggie Greene" call "on_hold" is "False"
        Then "Rick Grimes" call "on_hold" is "False"

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
