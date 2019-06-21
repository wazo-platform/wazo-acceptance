Feature: Pickup

    Scenario: Directed pickup
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten | context |
         | Dilbert   | Bologna  | sip      | 1001  | default |
         | Wally     | Lasagna  | sip      | 1002  | default |
         | Alice     | Wonder   | sip      | 1003  | default |
        When "Dilbert Bologna" calls "1002"
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is ringing
        When "Alice Wonder" calls "*81002"
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Alice Wonder" is talking

    Scenario: Intercepting user
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten | context |
         | Dilbert   | Bologna  | sip      | 1001  | default |
         | Wally     | Lasagna  | sip      | 1002  | default |
         | Alice     | Wonder   | sip      | 1003  | default |
        Given there are pickups:
         | name  | user_interceptor | user_target   |
         | first | Alice Wonder     | Wally Lasagna |
        When "Dilbert Bologna" calls "1002"
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is ringing
        When "Alice Wonder" calls "*8"
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Alice Wonder" is talking

    Scenario: Intercepting group
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten | context |
         | Dilbert   | Bologna  | sip      | 1001  | default |
         | Wally     | Lasagna  | sip      | 1002  | default |
         | Dogbert   | Canine   | sip      | 1003  | default |
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
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is ringing
        When "Dogbert Canine" calls "*8"
        When I wait "3" seconds for the call processing
        Then "Wally Lasagna" is hungup
        Then "Dilbert Bologna" is talking
        Then "Dogbert Canine" is talking

    Scenario: Intercepted group
        Given there are telephony users with infos:
         | firstname | lastname | protocol | exten | context |
         | Dilbert   | Bologna  | sip      | 1001  | default |
         | Wally     | Lasagna  | sip      | 1002  | default |
         | Dogbert   | Canine   | sip      | 1003  | default |
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
        When I wait "3" seconds for the call processing
        Then "Dogbert Canine" is ringing
        When "Wally Lasagna" calls "*8"
        When I wait "3" seconds for the call processing
        Then "Dogbert Canine" is hungup
        Then "Dilbert Bologna" is talking
        Then "Wally Lasagna" is talking
