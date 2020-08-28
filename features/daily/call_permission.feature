Feature: Call Permissions

  Scenario: User call permission
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Lagherta  | Unknown  | 1001  | default | yes        |
      | Ragnar    | Lodbrok  | 1002  | default | yes        |
    Given there are call permissions with infos:
      | name       | extensions | users            |
      | permission | 1002       | Lagherta Unknown |
    When "Lagherta Unknown" calls "1002"
    Then "Ragnak Lodbrok" is hungup
