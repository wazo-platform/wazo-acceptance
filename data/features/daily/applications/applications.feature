Feature: Application

    Scenario: Base application creation
        Given the are applications with infos:
        | name  | destination | destination_type | incall |
        | myapp | node        | holding          | 1700   |
        When I restart "xivo-ctid-ng"
        Given there are users with infos:
        | firstname | number | context | protocol |
        | Alice     |   1001 | default | sip      |
        When chan_test calls "1700@from-extern"
        When "Alice" picks up the call from the application "myapp"
        Then "myapp" contains a node with "2" calls
