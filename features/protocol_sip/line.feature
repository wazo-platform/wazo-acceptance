Feature: Line

    Scenario: Add a SIP line and remove it
        When I add a SIP line with infos:
        | context |
        | default |
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

    # BUG #3642
    Scenario: See IPBX infos in line page with accent in callerid
        Given there are users with infos:
         | firstname | lastname | number | context |
         | André     | óíúéåäë  |   1801 | default |
        When I edit the line "1801"
        When I go to the "IPBX Infos" tab
        Then I see in IPBX Infos tab value "callerid" has set to "André óíúéåäë" <1801>

    #Test X-325
    Scenario: Choose custom SIP codec
        When I add a SIP line with infos:
        | context | custom_codecs              |
        | default | Siren14 (G.722.1C) (Audio) |
        Then the codec "siren14" appears after typing 'sip show peer' in asterisk
        When I disable custom codecs for this line
        Then the codec "siren14" does not appear after typing 'sip show peer' in asterisk

    Scenario: Edit SIP line with no modifications
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then I see no errors
        When I edit the line "1601" without changing anything
        Then I see no errors

    Scenario: Add custom SIP codec to user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        When I add the codec "SpeeX (Audio)" to the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"

    Scenario: Edit custom SIP line without changing anything
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "SpeeX (Audio)"
        When I edit the line "1601" without changing anything
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"

    Scenario: Remove custom SIP codec from user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "SpeeX (Audio)"
        When I remove the codec "SpeeX (Audio)" from the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" does not have the codec "speex"

    Scenario: Add 2 custom SIP codecs to user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        When I add the codec "SpeeX (Audio)" to the line with number "1601"
        When I add the codec "iLBC (Audio)" to the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"
        Then the line with number "1601" has the codec "ilbc"

    Scenario: Remove a single custom SIP codec from user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "SpeeX (Audio)"
        Given the line "1601" has the codec "iLBC (Audio)"
        When I remove the codec "SpeeX (Audio)" from the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "ilbc"
        Then the line with number "1601" does not have the codec "speex"
