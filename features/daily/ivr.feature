Feature: IVR

  Scenario: IVR to destination user
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context |
      | Jake      | Gittes   | 1801   | default |
    Given there are IVR with infos:
      | name | menu_sound | timeout | max_tries |
      | ivr1 | beep       | 10      | 1         |
    Given the IVR "ivr1" choices are:
      | exten | destination_type | destination_arg |
      | 1     | user             | Jake Gittes     |
      | 2     | none             |                 |
    Given there is an incall "1801@from-extern" to the IVR "ivr1"
    When chan_test calls "1801@from-extern" with id "1337"
    When I wait "5" seconds for the call processing
    When chan_test queues DTMF "1" on channel with id "1337"
    When I wait "1" seconds
    Then "Jake Gittes" is ringing
