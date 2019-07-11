Feature: Pickup

    Scenario: Directed pickup
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | Dilbert   | Bologna  | 1001  | default |
         | Wally     | Lasagna  | 1002  | default |
         | Alice     | Wonder   | 1003  | default |
        When "Dilbert Bologna" calls "1002"
        Then "Wally Lasagna" is ringing
        When "Alice Wonder" calls "*81002"
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Alice Wonder" is talking

    Scenario: Intercepting user
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | Dilbert   | Bologna  | 1001  | default |
         | Wally     | Lasagna  | 1002  | default |
         | Alice     | Wonder   | 1003  | default |
        Given there are pickups:
         | name  | user_interceptor | user_target   |
         | first | Alice Wonder     | Wally Lasagna |
        When "Dilbert Bologna" calls "1002"
        Then "Wally Lasagna" is ringing
        When "Alice Wonder" calls "*8"
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Alice Wonder" is talking

    Scenario: Intercepting group
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | Dilbert   | Bologna  | 1001  | default |
         | Wally     | Lasagna  | 1002  | default |
         | Dogbert   | Canine   | 1003  | default |
        Given there are telephony groups with infos:
         | name | exten | context | timeout | noanswer_destination |
         | hr   | 2001  | default |         |                      |
        Given the telephony group "hr" has users:
         | firstname | lastname |
         | Dogbert   | Canine   |
        Given there are pickups:
         | name  | group_interceptor | user_target   |
         | first | hr                | Wally Lasagna |
        When "Dilbert Bologna" calls "1002"
        Then "Wally Lasagna" is ringing
        When "Dogbert Canine" calls "*8"
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Dogbert Canine" is talking

    Scenario: Intercepted group
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | Dilbert   | Bologna  | 1001  | default |
         | Wally     | Lasagna  | 1002  | default |
         | Dogbert   | Canine   | 1003  | default |
        Given there are telephony groups with infos:
         | name | exten | context | timeout | noanswer_destination |
         | hr   | 2001  | default |         |                      |
        Given the telephony group "hr" has users:
         | firstname | lastname |
         | Dogbert   | Canine   |
        Given there are pickups:
         | name  | group_target | user_interceptor |
         | first | hr           | Wally Lasagna    |
        When "Dilbert Bologna" calls "1003"
        Then "Dogbert Canine" is ringing
        When "Wally Lasagna" calls "*8"
        Then "Dogbert Canine" is hungup
        Then "Dilbert Bologna" is talking
        Then "Wally Lasagna" is talking

    Scenario: Pickup a call coming from a group
        Given there are telephony users with infos:
         | firstname | lastname | exten | context |
         | User      | 100      | 1100  | default |
         | User      | 101      | 1101  | default |
         | User      | 102      | 1102  | default |
        Given there are telephony groups with infos:
         | name   | exten | context | timeout | noanswer_destination |
         | group1 | 2001  | default |         |                      |
        Given the telephony group "group1" has users:
         | firstname | lastname |
         | User      | 101      |
        When "User 100" calls "2001"
        Then "User 101" is ringing
        When "User 102" calls "*81101"
        Then "User 100" is talking
        Then "User 102" is talking

    Scenario: Pickup a call coming from an incoming call
        Given there are telephony users with infos:
         | firstname | lastname | exten  | context |
         | User      | 143      | 1143   | default |
         | User      | 148      | 1148   | default |
        Given there is an incall "1143@from-extern" to the user "User 143"
        When chan_test calls "1143@from-extern"
        Then "User 143" is ringing
        When "User 148" calls "*81143"
        Then "User 148" is talking
