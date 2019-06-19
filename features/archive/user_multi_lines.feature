Feature: User multi lines

    Scenario: Incoming call rings all lines that have the same extension as the main line
        Given there are users with infos:
        | firstname | lastname | protocol | number | context |
        | Multi     | Lines    |          |        |         |
        Given I have the following lines:
        | context | username | protocol |
        | default |   line1  |   sip    |
        | default |   line2  |   sip    |
        | default |   line3   |   sip    |
        Given I have the following extensions:
        | context | exten |
        | default |  1801 |
        | default |  1802 |
        Given SIP line "line1" is associated to extension "1801@default"
        Given SIP line "line2" is associated to extension "1801@default"
        Given SIP line "line3" is associated to extension "1802@default"
        Given SIP line "line1" is associated to user "Multi" "Lines"
        Given SIP line "line2" is associated to user "Multi" "Lines"
        Given SIP line "line3" is associated to user "Multi" "Lines"
        Given there is an incall "1801" in context "from-extern" to the "user" "Multi Lines"
        Given a softphone is registered on SIP line "line1"
        Given a softphone is registered on SIP line "line2"
        Given a softphone is registered on SIP line "line3"

        When chan_test calls "1801@from-extern" with id "callid"

        Then "line1" is ringing
        Then "line2" is ringing
        Then "line3" is hungup
