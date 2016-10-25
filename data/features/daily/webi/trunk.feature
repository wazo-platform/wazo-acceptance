Feature: Trunk

    Scenario: Add a trunksip in the webi
        Given there is no trunksip "tokyo_paris"
        When I create a trunksip with name "tokyo_paris" in the webi
        Then trunksip "tokyo_paris" is displayed in the list
        Then the "sip.conf" file should contain peer "tokyo_paris"

    Scenario: Remove a trunksip in the webi
        Given there is a trunksip "tokyo_paris"
        When I remove the trunksip "tokyo_paris" in the webi
        Then trunksip "tokyo_paris" is not displayed in the list
        Then the "sip.conf" file should not contain peer "tokyo_paris"

    Scenario: Add a trunkcustom in the webi
        Given there is no trunkcustom "tokyo_paris"
        When I create a trunkcustom with name "tokyo_paris" in the webi
        Then trunkcustom "tokyo_paris" is displayed in the list

    Scenario: Remove a trunkcustom in the webi
        Given there is a trunkcustom "tokyo_paris"
        When I remove the trunkcustom "tokyo_paris" in the webi
        Then trunkcustom "tokyo_paris" is not displayed in the list
