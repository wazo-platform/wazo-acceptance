Feature: TrunkCustom

    Scenario: Add a trunkcustom
        Given I am logged in
        Given there is no trunkcustom "tokyo_paris"
        When I create a trunkcustom with name "tokyo_paris"
        Then there is a trunkcustom "tokyo_paris"

    Scenario: Remove a trunkcustom
        Given I am logged in
        Given there is a trunkcustom "tokyo_paris"
        When I remove the trunkcustom "tokyo_paris"
        Then there is no trunkcustom "tokyo_paris"
