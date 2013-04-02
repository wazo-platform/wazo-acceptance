Feature: TrunkCustom

    Scenario: Add a trunkcustom
        Given there is no trunkcustom "tokyo_paris"
        When I create a trunkcustom with name "tokyo_paris"
        Then trunkcustom "tokyo_paris" is displayed in the list

    Scenario: Remove a trunkcustom
        Given there is a trunkcustom "tokyo_paris"
        When I remove the trunkcustom "tokyo_paris"
        Then trunkcustom "tokyo_paris" is not displayed in the list
