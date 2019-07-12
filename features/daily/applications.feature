Feature: Application

    Scenario: Base application creation
        Given there are telephony users with infos:
        | firstname | exten | context | with_phone |
        | Alice     |  1001 | default | yes        |
        Given there are applications with infos:
        | name  | destination | destination_type | incall |
        | zeapp | node        | holding          | 1700   |
        When chan_test calls "1700@from-extern"
        When "Alice" picks up the call from the application "zeapp"
        Then "zeapp" contains a node with "2" calls
