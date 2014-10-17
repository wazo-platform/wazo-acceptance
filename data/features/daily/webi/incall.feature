Feature: Incalls

    Scenario: Add an incall with DID and remove it
        Given there is no incall "1657"
        When I create an incall with DID "1657" in context "from-extern"
        Then incall "1657" is displayed in the list
        When incall "1657" is removed
        Then incall "1657" is not displayed in the list

    Scenario: Search an incall
        Given there is no incall "1830"
        Given there is no incall "1831"
        Given there is no incall "1832"
        When I create an incall with DID "1830" in context "from-extern"
        When I create an incall with DID "1831" in context "from-extern"
        When I create an incall with DID "1832" in context "from-extern"
        Then incall "1830" is displayed in the list
        Then incall "1831" is displayed in the list
        Then incall "1832" is displayed in the list
