Feature: SCCP function keys

  @skip_old_cti_step
  Scenario: Reorder SCCP function keys
      Given there are no devices with mac "00:00:00:00:aa:01"
      Given I have the following devices:
          | ip             | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
      Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            |
          | Roger     | Rabbit   |   1234 | default | sccp     | 00:00:00:00:aa:01 |
      Given user "Roger" "Rabbit" has the following function keys:
          | Key | Type       | Destination | Label | Supervision |
          |   1 | Customized |        1001 |  1001 | Disabled    |
          |   2 | Customized |        1002 |  1002 | Disabled    |
          |   3 | Customized |        1003 |  1003 | Disabled    |
      When I reorder "Roger" "Rabbit"s function keys such that:
          | Old | New |
          |   1 |   3 |
          |   3 |   1 |
      Then the sccp.conf file should contain "3" function keys for "Roger" "Rabbit" sorted by key number
