Feature: TrunkSIP

    Scenario: Add a trunksip
        Given I am logged in
        Given there is no trunksip "tokyo_paris"
        When I create a trunksip with name "tokyo_paris"
        Then there is a trunksip "tokyo_paris"

    Scenario: Remove a trunksip
        Given I am logged in
        Given there is a trunksip "tokyo_paris"
        When I remove the trunksip "tokyo_paris"
        Then there is no trunksip "tokyo_paris"
