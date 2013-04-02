Feature: Line

    Scenario: Add a custom line with 127 characters
        Given there are no custom lines with interface beginning with "12345670000000000111111111122"
        When I add a custom line with infos:
        |                                                                                                                       interface |
        | 1234567000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111 |
        Then I see no errors
