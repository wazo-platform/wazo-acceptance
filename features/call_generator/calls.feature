Feature: Callgen

    Scenario: Call to inexistant extension
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     |          | 1100   | default | sip      |
        When "Alice" calls "1190"
        Then "Alice" last call should be "Extension not found"

    Scenario: Call to existant extension with answer
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     |          |   1100 | default | sip      |
         | Bob       |          |   1101 | default | sip      |
        When a call is started:
         | caller | dial | callee | talk_time | hangup |
         | Alice  | 1101 | Bob    | 3         | callee |
        When I generate call logs
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
