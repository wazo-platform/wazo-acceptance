Feature: Link a line and an extension

    Scenario: Associate an extension already associated with a queue
        Given there are queues with infos:
            | name    | number | context |
            | zohkaro | 3442   | default |
        Given I have the following lines:
            | username | protocol | context | device_slot |
            | zohkaro  | sip      | default | 1           |
        When I associate extension "3442@default" to sip line "zohkaro"
        Then I get a response with status "400"
        Then I get an error message matching "Resource Error - Extension is associated with a queue"
