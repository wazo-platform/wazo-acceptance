Feature: Call Permissions

  Scenario: User call permission
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Lagherta  | Unknown  | 1001  | default | yes        |
      | Ragnar    | Lodbrok  | 1002  | default | yes        |
      | Björn     | Ironside | 1003  | default | yes        |
    Given there are call permissions with infos:
      | name       | extensions | users            |
      | permission | 1002       | Lagherta Unknown |
    When "Lagherta Unknown" calls "1002"
    When I wait 2 seconds for the call processing
    Then "Ragnar Lodbrok" is hungup
    When I wait 4 seconds for the no permission message to complete
    Then "Lagherta Unknown" is hungup
    When "Björn Ironside" calls "1002"
    Then "Ragnar Lodbrok" is ringing

  Scenario: User call permission with password
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Gerard    | Tremblay | 1101  | default | yes        |
      | Sylvie    | Duquette | 1102  | default | yes        |
    Given there are call permissions with infos:
      | name       | extensions | users            | password |
      | perm-pwd   | 1102       | Gerard Tremblay  | 1234     |
    When "Gerard Tremblay" calls "1102"
    When I wait 2 seconds for the call processing
    Then "Sylvie Duquette" is hungup
    When I wait 4 seconds for the password input message to complete
    When "Gerard Tremblay" sends multiple DTMF "2222#"
    When I wait 4 seconds for the no permission message to complete
    Then "Sylvie Duquette" is hungup
    When I wait 4 seconds for the password input message to complete
    When "Gerard Tremblay" sends multiple DTMF "1234#"
    When I wait 2 seconds for the call processing
    Then "Sylvie Duquette" is ringing
