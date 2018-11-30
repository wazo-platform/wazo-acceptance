Feature: Meetme

    @skip_old_webi_step
    Scenario: Add a conference room
        Given I have no extension with exten "4000@default"
        When I add the following conference rooms:
            | name | number |
            | red  | 4000   |
        Then meetme "red" is displayed in the list

    @skip_old_webi_step
    Scenario: Add a conference room with max participants set to 0
        Given I have no extension with exten "4000@default"
        When I add the following conference rooms:
            | name | number | max users |
            | blue | 4000   | 0         |
        Then meetme "blue" is displayed in the list
