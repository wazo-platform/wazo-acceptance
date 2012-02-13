Feature: IPBX count

    Scenario: Show active sip trunk
        Given I am logged in
        Given there is no SIP trunk
        Given I have 1 enabled trunk
        When I open the ibpx count page
        Then I should have 1 enabled sip trunk
        Then I should have 0 disabled sip trunk
        Then I should have 1 sip trunk
