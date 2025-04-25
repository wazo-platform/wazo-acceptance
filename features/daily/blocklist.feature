Feature: user blocklist
  Scenario: incall to user blocked by user blocklist
    Given tenant country is "FR"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_token | with_phone | protocol |
      | Charlie   | Blocker  | 1001  | default | yes        | yes        | sip      |
    Given there is an incall "1001@from-extern" to the user "Charlie Blocker"
    Given the user "Charlie Blocker" has a blocklist with:
      | label | number         |
      | bad   | +15555555555   |
    When incoming call received from "trunk" to "1001@from-extern" with callerid ""Bad" <+15555555555>"
    When I wait 1 seconds for the call processing
    Then "Charlie Blocker" is not ringing
    Then "trunk" hears the sound file "user-unreachable"
    When I wait 6 seconds for the call processing
    Then "trunk" is hungup

  Scenario: incall to user not blocked by user blocklist
    Given tenant country is "FR"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_token | with_phone | protocol |
      | Charlie   | Blocker  | 1001  | default | yes        | yes        | sip      |
    Given there is an incall "1001@from-extern" to the user "Charlie Blocker"
    Given the user "Charlie Blocker" has a blocklist with:
      | label | number         |
      | bad   | +15555555551   |
    When incoming call received from "trunk" to "1001@from-extern" with callerid ""Good" <+15555555555>"
    When I wait 1 seconds for the call processing
    Then "Charlie Blocker" is ringing showing "Good"
