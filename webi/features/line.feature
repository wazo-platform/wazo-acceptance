Feature: Line

    Scenario: Add a SIP line and remove it
        When I add a "sip" line
        When I set the context to "default"
        When I submit
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

    Scenario: Add a custom line with 127 characters
        Given there is no custom lines
        When I add a "custom" line
        When I set the interface to "1234567000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111"
        When I submit
        Then I see no errors

    # BUG #3642
    Scenario: See IPBX infos in line page with accent in callerid
        Given there is a user "André" "óíúéåäë" with extension "1801@default"
        When I edit the line "1801"
        When I go to the "IPBX Infos" tab
        Then I see in IPBX Infos tab value "callerid" has set to "André óíúéåäë" <1801>

    #Test X-325
    Scenario: Choose custom SIP codec
        When I add a "sip" line
        When I set the context to "default"
        When I go to the "Signalling" tab
        When I activate custom codecs
        When I add the codec "Siren14 (G.722.1C) (Audio)"
        When I submit
        Then the codec "siren14" appears after typing 'sip show peer' in asterisk
        When I search for this line
        When I edit this line
        When I go to the "Signalling" tab
        When I deactivate custom codecs
        When I submit
        Then the codec "siren14" does not appear after typing 'sip show peer' in asterisk

