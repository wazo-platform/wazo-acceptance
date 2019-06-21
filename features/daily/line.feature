Feature: Line

    Scenario: Change SIP line username
        Given there are telephony users with infos:
        | firstname | lastname | exten | context | protocol | with_phone |
        | Ruffnut   | Thorson  |  1602 | default | sip      | yes        |
        | Tuffnut   | Thorson  |  1603 | default | sip      | no         |
        When I update lines with infos
        | exten | context | username    |
        | 1603  | default | newusername |
        Given the user "Tuffnut Thorson" has reconfigured the line "1603@default"
        When "Ruffnut Thorson" calls "1603"
        Then "Tuffnut Thorson" is ringing
        Then I have the following hints:
        | exten        | line              |
        | 1603@default | PJSIP/newusername |
