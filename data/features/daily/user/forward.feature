Feature: User Forward

    Scenario: Change unconditional forward from phone
        Given the "Enable unconditional forwarding" extension is set to "*21."
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | James     | Bond     |   1101 | default | sip      |
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has an unconditional forward set to "1102"
        When "James Bond" calls "*211103" and waits until the end
        Then "James Bond" has an unconditional forward set to "1103"
        When "James Bond" calls "*21" and waits until the end
        Then "James Bond" has no unconditional forward
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has an unconditional forward set to "1102"
        When "James Bond" calls "*211102" and waits until the end
        Then "James Bond" has no unconditional forward

    Scenario: When two users configure a forward loop the call does not get stuck
        Given the "Enable unconditional forwarding" extension is set to "*21."
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Mia       | Wallace  |   1001 | default | sip      |
        | Vincent   | Vega     |   1002 | default | sip      |
        When "Mia Wallace" calls "*211002" and waits until the end
        When "Vincent Vega" calls "*211001" and waits until the end
        When "Mia Wallace" calls "1002" and wait for "120" seconds
        Then "Mia Wallace" is hungup
