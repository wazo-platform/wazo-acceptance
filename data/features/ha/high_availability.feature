Feature: High availability

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

  Scenario: Enable/disable HA master changes cron jobs
    Given I switch to the XiVO master
    Given the HA is enabled as master
    When I disable the HA
    Then the file "/etc/cron.d/xivo-ha-master" does not exist
    When I enable the HA as master
    Then there are cron jobs in "/etc/cron.d/xivo-ha-master":
    | cron job                                                                              |
    | 0 * * * * root /usr/sbin/xivo-master-slave-db-replication {{ slave_voip_ip_address }} |
    | 0 * * * * root /usr/bin/xivo-sync                                                     |

  Scenario: Enable/disable HA slave changes cron jobs
    Given I switch to the XiVO slave
    Given the HA is enabled as slave
    When I disable the HA
    Then the file "/etc/cron.d/xivo-ha-slave" does not exist
    When I enable the HA as slave
    Then there are cron jobs in "/etc/cron.d/xivo-ha-slave":
    | cron job                                                                       |
    | * * * * * root /usr/sbin/xivo-check-master-status {{ master_voip_ip_address }} |
