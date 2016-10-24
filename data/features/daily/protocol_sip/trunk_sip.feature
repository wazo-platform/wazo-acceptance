Feature: TrunkSIP

    Scenario: Add a trunk sip
        Given there is no trunksip "tokyo_paris"
        When I create a trunksip with name "tokyo_paris"
        Then the "sip.conf" file should contain peer "tokyo_paris"

    Scenario: Remove a trunk sip
        Given there is a trunksip "tokyo_paris"
        When I remove the trunksip "tokyo_paris"
        Then the "sip.conf" file should not contain peer "tokyo_paris"
