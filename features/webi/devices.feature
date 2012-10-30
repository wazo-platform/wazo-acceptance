Feature: Devices

    Scenario: Search
        Given there is a device with infos:
          | ip             | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
          | 192.168.32.198 | 00:00:00:00:bb:02 |
        When I search device "bb:02"
        Then device "00:00:00:00:bb:02" is displayed in the list
        Then device "00:00:00:00:aa:01" is not displayed in the list
        When I search device "197"
        Then device "00:00:00:00:aa:01" is displayed in the list
        Then device "00:00:00:00:bb:02" is not displayed in the list
