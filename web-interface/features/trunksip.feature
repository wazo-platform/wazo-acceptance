Feature: TrunkSIP

    Scenario: Add an trunksip
        Given I am logged in
        Given there is no trunksip "tokyo_paris"
        When I create an trunksip with name "tokyo_paris"
        Then there is an trunksip "tokyo_paris"

    Scenario: Remove an trunksip
        Given I am logged in
        Given there is an trunksip "tokyo_paris"
        When I remove the trunksip "tokyo_paris"
        Then there is no trunksip "tokyo_paris"
