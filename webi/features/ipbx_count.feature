Feature: IPBX count

    Scenario: Show active sip trunk
        Given I am logged in
        Given there is no trunksip "trunk_0"
        Given i remember the number of available trunk as "nb_trunk_exist"
        Given I have 1 enabled trunk
        When I open the ibpx count page
        Then I should have 1 more then remembered value "nb_trunk_exist"
