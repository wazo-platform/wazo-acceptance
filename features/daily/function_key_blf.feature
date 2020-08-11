Feature: Function Key BLF

  Scenario: Forwards
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | BLFMan    | Forward  | 1801  | default |
    Given "BLFMan Forward" has function keys:
      | position | blf  | destination_type | destination_forward | destination_exten |
      | 1        | true | forward          | noanswer            |                   |
      | 2        | true | forward          | noanswer            | 1234              |
      | 3        | true | forward          | unconditional       |                   |
      | 4        | true | forward          | unconditional       | 5678              |
      | 5        | true | forward          | busy                |                   |
      | 6        | true | forward          | busy                | 9012              |
    When "BLFMan Forward" enable forwarding on no-answer to "1234"
    When "BLFMan Forward" enable unconditional forwarding to "5678"
    When "BLFMan Forward" enable forwarding on busy to "9012"
    Then "BLFMan Forward" has all forwards hints enabled
    When "BLFMan Forward" disable all forwards
    Then "BLFMan Forward" has all forwards hints disabled

    When "BLFMan Forward" enable forwarding on no-answer to "4321"
    Then "BLFMan Forward" has function key "1" hint enabled
    Then "BLFMan Forward" has function key "2" hint disabled

    When "BLFMan Forward" enable unconditional forwarding to "8765"
    Then "BLFMan Forward" has function key "3" hint enabled
    Then "BLFMan Forward" has function key "4" hint disabled

    When "BLFMan Forward" enable forwarding on busy to "2109"
    Then "BLFMan Forward" has function key "5" hint enabled
    Then "BLFMan Forward" has function key "6" hint disabled

  Scenario: Services
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | BLFMan    | Service  | 1802  | default |
    Given "BLFMan Service" has function keys:
      | position | blf  | destination_type | destination_service |
      | 1        | true | service          | enablednd           |
      | 2        | true | service          | incallfilter        |
    When "BLFMan Service" enable DND
    Then "BLFMan Service" has function key "1" hint enabled
    When "BLFMan Service" disable DND
    Then "BLFMan Service" has function key "1" hint disabled

    When "BLFMan Service" enable incoming call filtering
    Then "BLFMan Service" has function key "2" hint enabled
    When "BLFMan Service" disable incoming call filtering
    Then "BLFMan Service" has function key "2" hint disabled
