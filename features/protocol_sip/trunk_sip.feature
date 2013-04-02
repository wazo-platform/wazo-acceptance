Feature: TrunkSIP

    Scenario: Add a trunksip
        Given there is no trunksip "tokyo_paris"
        When I create a trunksip with name "tokyo_paris"
        Then trunksip "tokyo_paris" is displayed in the list

    Scenario: Remove a trunksip
        Given there is a trunksip "tokyo_paris"
        When I remove the trunksip "tokyo_paris"
        Then trunksip "tokyo_paris" is not displayed in the list
