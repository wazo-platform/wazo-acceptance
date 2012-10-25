Feature: Incalls

    Scenario: Add an incall with DID and remove it
        Given there is no incall "1000"
        When I create an incall with DID "1000" in context "Incalls (from-extern)"
        Then incall "1000" is displayed in the list
        When incall "1000" is removed
        Then incall "1000" is not displayed in the list

    Scenario: Search an incall
        Given there is no incall "1000"
        Given there is no incall "1001"
        Given there is no incall "1002"
        When I create an incall with DID "1000" in context "Incalls (from-extern)"
        When I create an incall with DID "1001" in context "Incalls (from-extern)"
        When I create an incall with DID "1002" in context "Incalls (from-extern)"
        Then incall "1000" is displayed in the list
        Then incall "1001" is displayed in the list
        Then incall "1002" is displayed in the list
