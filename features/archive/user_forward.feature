Feature: User Forward

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
