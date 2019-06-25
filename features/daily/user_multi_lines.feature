Feature: User multi lines

    Scenario: Ring all lines of a user
        Given there are telephony users with infos:
        | firstname | lastname | protocol | exten  | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1802   | default |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1801  | default | yes        |
        | line3 |       | default | yes        |
        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is ringing
        Then "line3" is hungup

    Scenario: User multi lines multi extensions
        Given there are telephony users with infos:
        | firstname | lastname | protocol | exten | context |
        | Multi     | Lines    |          |       |         |
        | Bob       | Field    | sip      | 1803  | default |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1802  | default | yes        |
        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is hungup

    Scenario: Activate a forward on user multi lines
        Given there are telephony users with infos:
        | firstname | lastname | protocol | exten | context |
        | Multi     | Lines    |          |       |         |
        | Bob       | Field    | sip      | 1802  | default |
        | Forward   | Unc      | sip      | 1803  | default |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1801  | default | yes        |
        Given the user "Multi Lines" has enabled "unconditional" forward to "1803"
        When "Bob Field" calls "1801"
        When I wait "3" seconds for the call to be forwarded
        Then "Forward Unc" is ringing

    Scenario: Activate dnd on user multi lines
        Given there are telephony users with infos:
        | firstname | lastname | protocol | exten | context |
        | Multi     | Lines    |          |       |         |
        | Bob       | Field    | sip      | 1802  | default |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1801  | default | yes        |
        Given the user "Multi Lines" has enabled "dnd" service
        When "Bob Field" calls "1801"
        When I wait "5" seconds for the call processing
        Then "Bob Field" is hungup

    Scenario: Ringing time are respected on user multi lines
        Given there are telephony users with infos:
        | firstname | lastname | protocol | exten | context | ring_seconds |
        | Multi     | Lines    |          |       |         | 5            |
        | Bob       | Field    | sip      | 1802  | default |              |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1801  | default | yes        |
        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is ringing
        When I wait "5" seconds for the end of ringing time
        Then "line1" is hungup
        Then "line2" is hungup
        When I wait "5" seconds for the call processing
        Then "Bob Field" is hungup

    Scenario: Incoming call rings all lines that have the same extension as the main line
        Given there are telephony users with infos:
        | firstname | lastname |
        | Multi     | Lines    |
        Given the user "Multi Lines" has lines:
        | name  | exten | context | with_phone |
        | line1 | 1801  | default | yes        |
        | line2 | 1801  | default | yes        |
        | line3 | 1802  | default | yes        |
        Given there is an incall "1801@from-extern" to the user "Multi Lines"
        When chan_test calls "1801@from-extern"
        Then "line1" is ringing
        Then "line2" is ringing
        Then "line3" is hungup
