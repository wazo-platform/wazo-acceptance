Feature: Line

    @skip_old_cti_step
    Scenario: Change SIP line username
        Given there are no SIP lines with username "newusername"
        Given there are users with infos:
        | firstname | lastname | number | context | protocol | with_phone |
        | Ruffnut   | Thorson  |   1602 | default | sip      | yes        |
        | Tuffnut   | Thorson  |   1603 | default | sip      | no         |
        When I set the following options in line "1603@default":
        | username    |
        | newusername |
        When I reconfigure the phone "Tuffnut Thorson" on line 1603@default
        When "Ruffnut Thorson" calls "1603"
        Then "Tuffnut Thorson" is ringing
        Then I have the following hints:
        | exten        | line              |
        | 1603@default | PJSIP/newusername |
