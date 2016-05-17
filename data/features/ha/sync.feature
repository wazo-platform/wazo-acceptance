Feature: Synchronization master - slave

  Scenario: Database synchronisation
    Given I switch to the XiVO slave
    Given there is no user "Test" "HA replication"
    Given I switch to the XiVO master
    Given there are users with infos:
    | firstname | lastname       |
    | Test      | HA replication |
    When I start the replication between master and slave
    When I switch to the XiVO slave
    Then I see a user with infos:
    | fullname             |
    | Test HA replication  |
