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
