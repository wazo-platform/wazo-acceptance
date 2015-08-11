Feature: Directed pickup

    Scenario: Pickup a call
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 100      |   1100 | default | sip      |
         | User      | 101      |   1101 | default | sip      |
         | User      | 102      |   1102 | default | sip      |
         
        When "User 100" calls "1101"
        Then "User 101" is ringing
        When "User 102" calls "*81101"
        Then "User 100" is talking
        Then "User 102" is talking

    Scenario: Pickup a call coming from a group
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 100      |   1100 | default | sip      |
         | User      | 101      |   1101 | default | sip      |
         | User      | 102      |   1102 | default | sip      |
        Given there is a group "group1" with extension "2001@default" and users:
          | firstname | lastname |
          | User      | 101      |
          
        When "User 100" calls "2001"
        Then "User 101" is ringing
        When "User 102" calls "*81101"
        Then "User 100" is talking
        Then "User 102" is talking

    Scenario: Pickup a call coming from an incoming call
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 143      |   1143 | default | sip      |
         | User      | 148      |   1148 | default | sip      |
        Given there is an incall "1143" in context "from-extern" to the "user" "User 143"
        
        When chan_test calls "1143@from-extern"
        Then "User 143" is ringing
        When "User 148" calls "*81143"
        Then "User 148" is talking
