Feature: User Forward

    Scenario: Change unconditional forward from phone
        Given there are telephony users with infos:
         | firstname | lastname | exten  | context |
         | James     | Bond     | 1101   | default |
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has an "unconditional" forward set to "1102"
        When "James Bond" calls "*211103" and waits until the end
        Then "James Bond" has an "unconditional" forward set to "1103"
        When "James Bond" calls "*21" and waits until the end
        Then "James Bond" has no "unconditional" forward
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has an "unconditional" forward set to "1102"
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has no "unconditional" forward

    Scenario: When two users configure a forward loop the call does not get stuck
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | Mia       | Wallace  | 1001  | default |
         | Vincent   | Vega     | 1002  | default |
        Given "Mia Wallace" has an "unconditional" forward set to "1002"
        Given "Vincent Vega" has an "unconditional" forward set to "1001"
        When "Mia Wallace" calls "1002" and waits for "120" seconds
        Then "Mia Wallace" is hungup
