Feature: User Forward

    Scenario: Change unconditional forward from phone
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten  | context |
         | James     | Bond     | sip      | 1101   | default |
        When "James Bond" calls "*211102" and waits until the end
        Then the user "James Bond" has an "unconditional" forward set to "1102"
        When "James Bond" calls "*211103" and waits until the end
        Then the user "James Bond" has an "unconditional" forward set to "1103"
        When "James Bond" calls "*21" and waits until the end
        Then the user "James Bond" has no "unconditional" forward
        When "James Bond" calls "*211102" and waits until the end
        Then the user "James Bond" has an "unconditional" forward set to "1102"
        When "James Bond" calls "*211102" and waits until the end
        Then the user "James Bond" has no "unconditional" forward

    Scenario: When two users configure a forward loop the call does not get stuck
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten | context |
         | Mia       | Wallace  | sip      | 1001  | default |
         | Vincent   | Vega     | sip      | 1002  | default |
        When "Mia Wallace" calls "*211002" and waits until the end
        When "Vincent Vega" calls "*211001" and waits until the end
        When "Mia Wallace" calls "1002" and waits for "120" seconds
        Then "Mia Wallace" is hungup