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

  Scenario: Skill rules based routing
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | agent_number |
      | English   | High     | 1801  | default | 1801         |
      | English   | Medium   | 1802  | default | 1802         |
      | English   | Low      | 1803  | default | 1803         |
    Given there are queues with infos:
      | name  | exten | context | retry_on_timeout | options_timeout | strategy | retry | agents         |
      | lobby | 3801  | default | true             | 5               | ringall  | 1     | 1801,1802,1803 |
    Given there are "waiting" skill rule with infos:
      | definition            |
      | WT < 10, english > 89 |
      | WT < 20, english > 79 |
      | english > 69          |
    Given agent "1801" has skill "english" with weight "90"
    Given agent "1802" has skill "english" with weight "80"
    Given agent "1803" has skill "english" with weight "70"
    Given there is an incall "3801@from-extern" to the queue "lobby" with skill "waiting"
    Given agent "1801" is logged
    Given agent "1802" is logged
    Given agent "1803" is logged
    When chan_test calls "3801@from-extern"
    Then "English High" is ringing
    Then "English Medium" is hungup
    Then "English Low" is hungup
    When I wait "11" seconds to simulate call center
    Then "English High" is ringing
    Then "English Medium" is hungup
    Then "English Low" is hungup
    Then "English High" answers

    When chan_test calls "3801@from-extern"
    Then "English High" is talking
    Then "English Medium" is hungup
    Then "English Low" is hungup
    When I wait "10" seconds to simulate call center
    Then "English High" is talking
    Then "English Medium" is ringing
    Then "English Low" is hungup
    Then "English Medium" answers

    When chan_test calls "3801@from-extern"
    Then "English High" is talking
    Then "English Medium" is talking
    Then "English Low" is hungup
    When I wait "10" seconds to simulate call center
    Then "English High" is talking
    Then "English Medium" is talking
    Then "English Low" is hungup
    When I wait "10" seconds to simulate call center
    Then "English High" is talking
    Then "English Medium" is talking
    Then "English Low" is ringing
    Then "English Low" answers

    When chan_test calls "3801@from-extern"
    Then "English High" is talking
    Then "English Medium" is talking
    Then "English Low" is talking
    Then "English Medium" hangs up
    When I wait "5" seconds to simulate call center
    Then "English Medium" is hungup
    When I wait "5" seconds to simulate call center
    Then "English Medium" is ringing
