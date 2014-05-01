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
         | destination_exten | duration | user_field | answered |
         | 1101              | 0:00:03  |            | True     |

    Scenario: Call with extension call recording activated
        Given there is "Call recording" activated in extenfeatures page
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 100      |   1100 | default | sip      |
         | User      | 101      |   1101 | default | sip      |
        When a call is started:
         | caller   | dial | callee   | talk_time | hangup |
         | User 100 | 1101 | User 101 | 3         | callee |
        Then I see no recording file of this call in monitoring audio files page

    Scenario: Calls are still logged after a reload of cel_pgsql
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     |          |   1100 | default | sip      |
         | Bob       |          |   1101 | default | sip      |
        When I reload the module "cel_pgsql.so"
        When a call is started:
         | caller | dial | callee | talk_time | hangup |
         | Alice  | 1101 | Bob    | 3         | callee |
        Then I have the last call log matching:
         | destination_exten | duration | user_field | answered |
         | 1101              | 0:00:03  |            | True     |

    Scenario: Call to line that is disabled
        Given there are users with infos:
            | firstname | lastname | number | context | protocol |
            | Bountrabi | Sylla    | 1102   | default | sip      |
            | Papa      | Sylla    | 1103   | default | sip      |
        Given the line "1103@default" is disabled
        When "Bountrabi Sylla" calls "1103"
        Then "Bountrabi Sylla" last dialed extension was not found

    Scenario: No answer destination with disabled forward exten on no answer
        Given the "Enable forwarding on no-answer" extension is "disabled"
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | James     | Bond     |   1101 | default | sip      |
        | Tiffany   | Case     |   1102 | default | sip      |
        | Pussy     | Galore   |   1103 | default | sip      |
        Given "James Bond" has a "5 seconds" ringing time
        Given "James Bond" has a dialaction on "No answer" to "User" "Pussy Galore"
        When "Tiffany Case" calls "1101"
        Then "James Bond" is ringing
        When I wait 9 seconds
        Then "Pussy Galore" is ringing
