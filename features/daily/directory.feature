Feature: Directory integration

    Scenario: List conference rooms as a dird user
        Given there is a user
        Given there are conference rooms with infos:
        | name | exten |
        | test | 4001  |
        When the user lists conference rooms using wazo-dird
        Then the conference rooms list contains:
        | name | exten |
        | test | 4001  |
