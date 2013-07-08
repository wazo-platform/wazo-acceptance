Feature: Outcall

    Scenario: Add an outcall
        Given there is no outcall "outdoor"
        Given there is a trunksip "door"
        When I create an outcall with name "outdoor" and trunk "door"
        Then outcall "outdoor" is displayed in the list

    Scenario: Remove an outcall
        Given there is an outcall "outdoor" with trunk "door" and no extension matched
        When I remove the outcall "outdoor"
        Then there is no outcall "outdoor"

    Scenario: Add an extension in outcall
        Given there is an outcall "outdoor" with trunk "door" and no extension matched
        When I add the following extension patterns to the outcall "outdoor":
          | extension_pattern |
          |              7000 |
        Then the outcall "outdoor" has the extension patterns:
          | extension_pattern |
          |              7000 |

    Scenario: Remove an extension in outcall
        Given there is an outcall "outdoor" with trunk "door" with extension patterns:
          | extension_pattern |
          |              7000 |
        When I remove extension patterns from outcall "outdoor":
          | extension_pattern |
          |              7000 |
        Then the outcall "outdoor" does not have extension patterns:
          | extension_pattern |
          |              7000 |

    Scenario: Edit an outcall and change the context
        Given there is an outcall "linguini" in context "interco" with trunk "pasta"
        When i edit the outcall "linguini" and set context to "to-extern"
        Then there are outcalls with infos:
          | name    | context   |
          | linguini | to-extern |
