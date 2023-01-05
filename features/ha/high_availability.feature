Feature: High availability

  Scenario: Enable/disable HA master changes cron jobs
    Given the HA is enabled as master on "master"
    When I disable the HA on "master"
    Then the file "/etc/cron.d/xivo-ha-master" does not exist on "master"
    When I enable the HA as master on "master"
    Then there are cron jobs in "/etc/cron.d/xivo-ha-master" on "master"
      | cron job                                                                              |
      | 0 * * * * root /usr/sbin/xivo-master-slave-db-replication {{ slave_voip_ip_address }} |
      | 0 * * * * root /usr/bin/xivo-sync                                                     |
    Then the provd config "default" has the following values on "master"
      | X_type    | proxy_backup                | registrar_backup            |
      | registrar | {{ slave_voip_ip_address }} | {{ slave_voip_ip_address }} |

  Scenario: Enable/disable HA slave changes cron jobs
    Given the HA is enabled as slave on "slave"
    When I disable the HA on "slave"
    Then the file "/etc/cron.d/xivo-ha-slave" does not exist on "slave"
    When I enable the HA as slave on "slave"
    Then there are cron jobs in "/etc/cron.d/xivo-ha-slave" on "slave"
      | cron job                                                                       |
      | * * * * * root /usr/sbin/xivo-check-master-status {{ master_voip_ip_address }} |
    Then the provd offline config "default" has the following values on "slave"
      | X_type    | proxy_backup | registrar_backup |
      | registrar |              |                  |

  Scenario: HA synchronization
    Given the HA is enabled as master on "master"
    Given the HA is enabled as slave on "slave"
    Given there is a user "test-replication" on "master"
    Given there is no user "test-replication" on "slave"
    When I start the replication from "master" to unknown
    Then there is a mail with content "Slave replication failed" on "master"
    When I start the replication from "master" to "slave"
    Then there is a user "test-replication" on "slave"

    Given the file "/root/.ssh/xivo_id_rsa" does not exist on "master"
    Given the file "/root/.ssh/xivo_id_rsa.pub" does not exist on "master"
    Given the file "/root/.ssh/authorized_keys" does not contain "XiVO HA" on "slave"
    When I initialize xivo-sync on "master" to "slave"
    Then the file "/root/.ssh/xivo_id_rsa" exists on "master"
    Then the file "/root/.ssh/xivo_id_rsa.pub" exists on "master"
    Then the file "/root/.ssh/authorized_keys" contains "XiVO HA" on "slave"

    Given the file "/etc/asterisk/extensions_extra.d/acceptance.conf" exists on "master"
    Given the file "/etc/asterisk/extensions_extra.d/acceptance.conf" does not exist on "slave"
    When I execute "xivo-sync" command on "master"
    Then the file "/etc/asterisk/extensions_extra.d/acceptance.conf" exists on "slave"

    # Workaround WAZO-2999
    Then I execute "wazo-service restart" command on "slave"
    Then I wait until services are ready on "slave"
