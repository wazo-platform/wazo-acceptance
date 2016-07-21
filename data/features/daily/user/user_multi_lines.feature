Feature: User multi lines

    Scenario: Do ringing all lines of a user
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1802   | default |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default | 1801  |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1801@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP Line "line1" register to softphone
        Given SIP Line "line2" register to softphone

        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is ringing

    Scenario: User multi lines multi extensions
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1803   | default |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default | 1801  |
        | default | 1802  |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1802@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP Line "line1" register to softphone
        Given SIP Line "line2" register to softphone

        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is hungup

    Scenario: Activate a forward on user multi lines
        Given the "Enable unconditional forwarding" extension is enabled
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1802   | default |
        | Forward   | Unc      | sip      | 1803   | default |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default | 1801  |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1801@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP Line "line1" register to softphone
        Given SIP Line "line2" register to softphone
        Given user "Multi Lines" has enabled "unconditional" forward to "1803"

        When "Bob Field" calls "1801"
        When I wait 2 seconds for the calls processing

        Then "Forward Unc" is ringing

    Scenario: Activate dnd on user multi lines
        Given the "Do not disturb" extension is enabled
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1802   | default |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default | 1801  |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1801@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP Line "line1" register to softphone
        Given SIP Line "line2" register to softphone
        Given user "Multi Lines" has enabled "dnd" service

        When "Bob Field" calls "1801"
        When I wait 5 seconds for the calls processing

        Then "Bob Field" is hungup

    Scenario: Ringing time are respected on user multi lines
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        | Bob       | Field    | sip      | 1802   | default |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default | 1801  |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1801@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP Line "line1" register to softphone
        Given SIP Line "line2" register to softphone
        Given "Multi Lines" has a "5 seconds" ringing time

        When "Bob Field" calls "1801"
        Then "line1" is ringing
        Then "line2" is ringing

        When I wait 5 seconds for the end of ringing time
        When I wait 5 seconds for the calls processing
        Then "Bob Field" is hungup
        Then "line1" is hungup
        Then "line2" is hungup
