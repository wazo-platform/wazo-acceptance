Feature: User password

  Scenario: Change password using a user token
    Given there are authentication users with info
      | firstname | username | password |
      | Greg      | greg     | 123test  |
    When "greg" changes its password from "123test" to "foobar"
    Then I can get a user token with username "greg" and password "foobar"
