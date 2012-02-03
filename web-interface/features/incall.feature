Feature: Incalls

    In order to get an incall
    I have to create an incall

    Scenario Outline: Add an incall with DID and remove it
        Given I am logged in
        Given there is no incall with DID "6000"
        When I create an incall with DID "6000"
        Then incall "6000" is displayed in the list
        When incall "6000" is removed
        Then incall "6000" is not displayed in the list

    Scenario Outline: Search an incall
        Given I am logged in
        Given there is no incall with DID "6000"
        When I create an incall with DID "6000"
        Given there is no incall with DID "6001"
        When I create an incall with DID "6001"
        Given there is no incall with DID "6002"
        When I create an incall with DID "6002"
        Then incall "6000" is displayed in the list
        Then incall "6001" is displayed in the list
        Then incall "6002" is displayed in the list
