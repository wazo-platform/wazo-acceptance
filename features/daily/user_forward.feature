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
