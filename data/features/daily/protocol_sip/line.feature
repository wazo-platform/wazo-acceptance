Feature: Line

    @skip_old_webi_step
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
        Then the line "1801" has the following line options:
         | Caller ID              |
         | "André óíúéåäë" <1801> |

    @skip_old_webi_step
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
        When I add the codec "Speex (Audio)" to the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"

    Scenario: Edit custom SIP line without changing anything
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "Speex (Audio)"
        When I edit the line "1601" without changing anything
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"

    Scenario: Remove custom SIP codec from user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "Speex (Audio)"
        When I remove the codec "Speex (Audio)" from the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" does not have the codec "speex"

    Scenario: Add 2 custom SIP codecs to user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        When I add the codec "Speex (Audio)" to the line with number "1601"
        When I add the codec "iLBC (Audio)" to the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "speex"
        Then the line with number "1601" has the codec "ilbc"

    Scenario: Remove a single custom SIP codec from user line
        Given there are users with infos:
        | firstname | lastname   | number | context |
        | Johnny    | Wilkinson  | 1601   | default |
        Given the line "1601" has the codec "Speex (Audio)"
        Given the line "1601" has the codec "iLBC (Audio)"
        When I remove the codec "Speex (Audio)" from the line with number "1601"
        When I edit the user "Johnny" "Wilkinson" without changing anything
        Then the line with number "1601" has the codec "ilbc"
        Then the line with number "1601" does not have the codec "speex"

    Scenario: Change SIP line username
        Given there are no SIP lines with username "newusername"
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Ruffnut   | Thorson  |   1602 | default | sip      |
        | Tuffnut   | Thorson  |   1603 | default | sip      |
        When I set the following options in line "1603@default":
        | username    |
        | newusername |
        When I reconfigure the phone "Tuffnut Thorson" on line 1603@default
        When "Ruffnut Thorson" calls "1603"
        Then "Tuffnut Thorson" is ringing
        Then I have the following hints:
        | exten        | line            |
        | 1603@default | SIP/newusername |
