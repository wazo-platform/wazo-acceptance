Feature: Call Generation

  Scenario: Call to inexistant extension
    Given there are telephony users with infos:
      | firstname | exten | context |
      | Alice     | 1100  | default |
    When "Alice" calls "1190"
    Then "Alice" is hungup immediately

  Scenario: Call to existant extension with answer
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Alice     | 1100     | 1100  | default |
      | Bob       | 1101     | 1101  | default |
    When a call is started:
      | caller      | dial | callee      | talk_time | hangup |
      | Alice 1100  | 1101 | Bob 1101    | 3         | callee |
    Then I have the last call log matching:
      | destination_extension | duration | answered |
      | 1101                  | 3        | True     |

  Scenario: No answer destination with disabled forward exten on no answer
    Given the "fwdrna" extension is disabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | James     | Bond     | 1101  | default |
      | Tiffany   | Case     | 1102  | default |
      | Pussy     | Galore   | 1103  | default |
    Given "James Bond" has a 5 seconds ringing time
    Given "James Bond" has a "noanswer" fallback to user "Pussy Galore"
    When "Tiffany Case" calls "1101"
    Then "James Bond" is ringing
    When I wait 5 seconds for the end of ringing time
    When I wait 4 seconds for the call processing
    Then "Pussy Galore" is ringing

  Scenario: Busy destination with disabled forward exten on busy
    Given the "fwdbusy" extension is disabled
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | James     | Bond     | 1101  | default |
      | Honey     | Ryder    | 1102  | default |
      | Sylvia    | Trench   | 1103  | default |
    Given "James Bond" has a "busy" fallback to user "Sylvia Trench"
    When "Honey Ryder" calls "1101"
    Then "James Bond" is ringing
    When "James Bond" hangs up
    When I wait 2 seconds for the call processing
    Then "Sylvia Trench" is ringing

  Scenario: Call on hold are marked as on_hold when listing calls
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Bruce     | Wayne    | 1001  | default |
      | Clark     | Kent     | 1002  | default |
    Given I listen on the bus for the following events:
      | event            |
      | MusicOnHoldStop  |
      | MusicOnHoldStart |
    Given "Bruce Wayne" calls "1002"
    Given "Clark Kent" answers
    Then "Clark Kent" call is not "on_hold"
    Then "Bruce Wayne" call is not "on_hold"

    When "Clark Kent" puts his call on hold
    Then "Clark Kent" call is "on_hold"
    Then "Bruce Wayne" call is not "on_hold"
    Then I receive a "MusicOnHoldStart" event
    Then I receive no "MusicOnHoldStop" event

    When "Clark Kent" resumes his call
    Then "Clark Kent" call is not "on_hold"
    Then "Bruce Wayne" call is not "on_hold"
    Then I receive a "MusicOnHoldStop" event

  Scenario: Relocate with multiple contacts
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | username | password | with_token |
      | Donald    | Trump    | 1001  | default | donald   | trump    | no         |
      | Darth     | Vader    |       |         | darth    | vader    | yes        |
    Given "Darth Vader" has lines:
      | name  | exten | context | with_phone |
      | line1 | 1002  | default | yes        |
      | line2 | 1002  | default | yes        |
    Given "Donald Trump" calls "1002"
    When "Darth Vader" answers on its contact "1"
    When "Darth Vader" relocates its call to its contact "2"
    When "Darth Vader" answers on its contact "2"
    Then "Darth Vader" is talking to "Donald Trump" on its contact "2"

  Scenario: Bus messages on hold and resume
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Marty     | McFly    | 1001  | default |
      | George    | McFly    | 1002  | default |
    Given I listen on the bus for the following events:
      | event        |
      | call_held    |
      | call_resumed |
    Given "Marty McFly" calls "1002"
    Given "George McFly" answers
    When "George McFly" puts his call on hold
    Then I receive a "call_held" event
    When "George McFly" resumes his call
    Then I receive a "call_resumed" event

  Scenario: Transfer timeout is respected
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Rick      | Sanchez  |  1001 | default |
      | Morty     | Smith    |  1002 | default |
      | Mister    | Meeseeks |  1003 | default |
    Given "Rick Sanchez" calls "1002"
    Given "Morty Smith" answers
    When "Morty Smith" does a blind transfer to "1003@default" with timeout 3 using API
    Then "Mister Meeseeks" is ringing
    When I wait 4 seconds
    Then "Mister Meeseeks" is hungup
