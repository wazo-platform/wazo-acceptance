Feature: Incalls

  Scenario: Add an incall with DID and remove it
    Given there are incalls with infos in the webi:
    | extension | context     |
    |      1657 | from-extern |
    Then incall "1657" is displayed in the list
    When incall "1657" is removed in the webi
    Then incall "1657" is not displayed in the list

  Scenario: Search an incall
    Given there are incalls with infos in the webi:
    | extension | context     |
    |      1830 | from-extern |
    |      1831 | from-extern |
    |      1832 | from-extern |
    Then incall "1830" is displayed in the list
    Then incall "1831" is displayed in the list
    Then incall "1832" is displayed in the list

  Scenario: Disabled incall should not be in the available
    Given there are incalls with infos in the webi:
    | extension | context     |
    |      1888 | from-extern |
    When I "disable" incall "1888" in the webi
    Then extension "1888" is not in context "from-extern"
    When I "enable" incall "1888" in the webi
    Then extension "1888" is in context "from-extern"
