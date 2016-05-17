Feature: Synchronization master - slave

  Scenario: Database synchronisation

    Given there is no user on the slave "Test" "HA replication"
    Given there are users on the master with infos:
    | firstname | lastname       |
    | Test      | HA replication |
    When I start the replication between master and slave
    Then I see a user on the slave with infos:
    | fullname             |
    | Test HA replication  |
