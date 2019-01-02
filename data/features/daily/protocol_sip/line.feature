Feature: Line

    @skip_old_webi_step
    Scenario: Add a SIP line and remove it
        When I add a SIP line with infos:
        | context |
        | default |
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

    @skip_old_webi_step
    Scenario: Choose custom SIP codec
        When I add a SIP line with infos:
        | context | custom_codecs              |
        | default | Siren14 (G.722.1C) (Audio) |
        Then the codec "siren14" appears after typing 'sip show peer' in asterisk
        When I disable custom codecs for this line
        Then the codec "siren14" does not appear after typing 'sip show peer' in asterisk

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
