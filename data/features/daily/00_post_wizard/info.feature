Feature: XiVO info

  Scenario: Check that the XiVO server has a uuid
    When I request a list for "infos" using parameters:
    Then I get a response 200 matching ".*uuid.*"
