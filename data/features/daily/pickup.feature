 Feature: Pickup

   Scenario: Directed pickup
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Alice     |          |   1003 | default | sip      |
     Given "Dilbert" calls "1002"
     Given "Wally" is ringing
     When "Alice" calls "*81002"
     Then "Wally" is hungup
     Then "Dilbert" is talking
     Then "Alice" is talking

   Scenario: Intercepting user
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Alice     |          |   1003 | default | sip      |
     Given there are pickups:
      | name  | intercepting users | intercepted users |
      | first | Alice              | Wally             |
     Given "Dilbert" calls "1002"
     Given "Wally" is ringing
     When "Alice" calls "*8"
     Then "Wally" is hungup
     Then "Dilbert" is talking
     Then "Alice" is talking

   Scenario: Intercepting group
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Dogbert   |          |   1003 | default | sip      |
     Given there is a group "hr" with extension "2001@default" and users:
      | firstname |
      | Dogbert   |
     Given there are pickups:
      | name  | intercepting groups | intercepted users |
      | first | hr                  | Wally             |
     Given "Dilbert" calls "1002"
     Given "Wally" is ringing
     When "Dogbert" calls "*8"
     Then "Wally" is hungup
     Then "Dilbert" is talking
     Then "Dogbert" is talking

   Scenario: Intercepting queue
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Asok      |          |   1003 | default | sip      |
     Given there are queues with infos:
      | name | display name | number | context | users_number |
      | eng  | Engineering  |   3001 | default |         1003 |
     Given there are pickups:
      | name  | intercepting queues | intercepted users |
      | first | eng                 | Wally             |
     Given "Dilbert" calls "1002"
     Given "Wally" is ringing
     When "Asok" calls "*8"
     Then "Wally" is hungup
     Then "Dilbert" is talking
     Then "Asok" is talking

   Scenario: Intercepted group
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Dogbert   |          |   1003 | default | sip      |
     Given there is a group "hr" with extension "2001@default" and users:
      | firstname |
      | Dogbert   |
     Given there are pickups:
      | name  | intercepted groups | intercepting users |
      | first | hr                 | Wally              |
     Given "Dilbert" calls "1003"
     Given "Dogbert" is ringing
     When "Wally" calls "*8"
     Then "Dogbert" is hungup
     Then "Dilbert" is talking
     Then "Wally" is talking

   Scenario: Intercepted queue
     Given there are users with infos:
      | firstname | lastname | number | context | protocol |
      | Dilbert   |          |   1001 | default | sip      |
      | Wally     |          |   1002 | default | sip      |
      | Asok      |          |   1003 | default | sip      |
     Given there are queues with infos:
      | name | display name | number | context | users_number |
      | eng  | Engineering  |   3001 | default |         1003 |
     Given there are pickups:
      | name  | intercepted queues | intercepting users |
      | first | eng                | Wally              |
     Given "Dilbert" calls "1003"
     Given "Asok" is ringing
     When "Wally" calls "*8"
     Then "Asok" is hungup
     Then "Dilbert" is talking
     Then "Wally" is talking
