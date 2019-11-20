Feature: Skill

  Scenario: Skill based routing
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | English   | Man      | 1801  | default | 1801         |
      | French    | Potato   | 1802  | default | 1802         |
    Given there are queues with infos:
      | name  | exten | context | agents    |
      | lobby | 3801  | default | 1801,1802 |
    Given there are skill rules with infos:
      | name    | definition                 |
      | english | english > 90               |
      | french  | french > 0 \| french < 100 |
    Given agent "1801" has skill "english" with weight "95"
    Given agent "1802" has skill "french" with weight "50"
    Given there is an incall "3851@from-extern" to the queue "lobby" with skill "english"
    Given there is an incall "3852@from-extern" to the queue "lobby" with skill "french"
    Given agent "1801" is logged
    Given agent "1802" is logged
    When chan_test calls "3851@from-extern"
    Then "English Man" is ringing
    Then "French Potato" is hungup
    Given "English Man" hangs up
    When chan_test calls "3852@from-extern"
    Then "French Potato" is ringing
    Then "English Man" is hungup
