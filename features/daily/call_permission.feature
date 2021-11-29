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

  Scenario: Group call permission
    Given there are telephony users with infos:
      | firstname | lastname  | exten | context | with_phone |
      | Sonia     | Champoux  | 1201  | default | yes        |
      | Charles   | Patenaude | 1202  | default | yes        |
      | Flavien   | Bouchard  | 1203  | default | yes        |
    Given there are telephony groups with infos:
      | label        | exten | context |
      | RomanoFafard | 2000  | default |
    Given the telephony group "RomanoFafard" has users:
      | firstname | lastname  |
      | Sonia     | Champoux  |
    Given there are call permissions with infos:
      | name       | extensions | groups            |
      | permission | 1202       | RomanoFafard      |
    When "Sonia Champoux" calls "1202"
    When I wait 2 seconds for the call processing
    Then "Charles Patenaude" is hungup
    When I wait 4 seconds for the no permission message to complete
    Then "Sonia Champoux" is hungup
    When "Flavien Bouchard" calls "1202"
    Then "Charles Patenaude" is ringing

  Scenario: Outcall call permission
    Given there are telephony users with infos:
      | firstname | lastname  | exten | context | with_phone |
      | Bill      | Gates     | 1201  | default | yes        |
      | Steve     | Ballmer   | 1202  | default | yes        |
    Given there is an outcall using extension "11234@to-extern"
    Given there are call permissions with infos:
      | name       | extensions  | outcalls      |
      | permission | 1202        | outcall-11234 |
    When "Steve Ballmer" calls "11234"
    When I wait 4 seconds for the no permission message to complete
    When "Bill Gates" calls "11234"
    When I wait 2 seconds for the call processing
    Then "outcall-11234" is ringing
