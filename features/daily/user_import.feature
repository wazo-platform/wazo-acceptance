Feature: CSV import of users

  Scenario: wazo-auth users are not leaked on error
    Given there are authentication users with infos:
      | firstname | lastname | username | password |
      | John      | Doe      | john     | lonen0   |
    When I import the following users ignoring errors:
      | firstname | lastname | username | password |
      | One       | Un       | one      | love     |
      | Two       | Deux     | john     | drag0n   |
    Then my import result has an error on line "2"
    Then the user with username "one" does not exist
