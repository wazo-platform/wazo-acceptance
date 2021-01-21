Feature: Boss Secretary Filter

  Scenario: bsfilter function key workflow
    Given there are devices with infos:
      | mac               |
      | 00:11:22:33:44:00 |
      | 00:11:22:33:44:01 |
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | device            | with_phone |
      | Charlie   | Unknown  | 1001  | default | 00:11:22:33:44:00 | yes        |
      | Angel     | 001      | 1002  | default | 00:11:22:33:44:01 | yes        |
      | Bad       | Guy      | 1010  | default |                   | yes        |
    Given there are call filters with infos:
      | name             | strategy                               | recipients      | surrogates |
      | Charlie's Angels | linear-surrogates-then-all-recipients  | Charlie Unknown | Angel 001  |
    Given "Charlie Unknown" has function keys:
      | position | destination_type | destination_filter_name | destination_filter_member |
      | 1        | bsfilter         | Charlie's Angels        | Angel 001                 |
    Given "Angel 001" has function keys:
      | position | destination_type | destination_filter_name | destination_filter_member |
      | 1        | bsfilter         | Charlie's Angels        | Angel 001                 |
    When "Charlie Unknown" press function key "1"
    When I wait 4 seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint enabled
    Then "Angel 001" has function key "1" hint enabled
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    When "Bad Guy" hangs up

    When "Charlie Unknown" press function key "1"
    When I wait 4 seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint disabled
    Then "Angel 001" has function key "1" hint disabled
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is ringing
    Then "Angel 001" is hungup
    When "Bad Guy" hangs up
    
    When "Angel 001" press function key "1"
    When I wait 4 seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint enabled
    Then "Angel 001" has function key "1" hint enabled
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    When "Bad Guy" hangs up

    When "Angel 001" press function key "1"
    When I wait 4 seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint disabled
    Then "Angel 001" has function key "1" hint disabled
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is ringing
    Then "Angel 001" is hungup
    
  Scenario: Strategy "all"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Charlie   | Unknown  | 1001  | default | yes        |
      | Angel     | 001      | 1002  | default | yes        |
      | Bad       | Guy      | 1010  | default | yes        |
    Given there are call filters with infos:
      | name             | strategy | recipients      | surrogates | caller_id_mode | caller_id_name |
      | Charlie's Angels | all      | Charlie Unknown | Angel 001  | prepend        | FILTER         |
    Given "Angel 001" enable call filter "Charlie's Angels"
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is ringing showing "FILTER - Bad Guy"
    Then "Angel 001" is ringing showing "FILTER - Bad Guy"

  Scenario: Strategy "all-recipients-then-linear-surrogates"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Charlie   | Unknown  | 1001  | default | yes        |
      | Angel     | 001      | 1002  | default | yes        |
      | Angel     | 002      | 1003  | default | yes        |
      | Bad       | Guy      | 1010  | default | yes        |
    Given there are call filters with infos:
      | name             | strategy                              | recipients      | surrogates          | caller_id_mode | caller_id_name |
      | Charlie's Angels | all-recipients-then-linear-surrogates | Charlie Unknown | Angel 001,Angel 002 | append         | FILTER         |
    Given "Angel 001" enable call filter "Charlie's Angels"
    Given "Angel 002" enable call filter "Charlie's Angels"
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is ringing showing "Bad Guy - FILTER"
    Then "Angel 001" is hungup
    Then "Angel 002" is hungup
    When "Charlie Unknown" hangs up
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing showing "Bad Guy - FILTER"
    Then "Angel 002" is hungup
    When "Angel 001" hangs up
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is hungup
    Then "Angel 002" is ringing showing "Bad Guy - FILTER"

  Scenario: Strategy "all-recipients-then-all-surrogates"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Charlie   | Unknown  | 1001  | default | yes        |
      | Angel     | 001      | 1002  | default | yes        |
      | Angel     | 002      | 1003  | default | yes        |
      | Bad       | Guy      | 1010  | default | yes        |
    Given there are call filters with infos:
      | name             | strategy                           | recipients      | surrogates          | recipients_timeout |
      | Charlie's Angels | all-recipients-then-all-surrogates | Charlie Unknown | Angel 001,Angel 002 | 5                  |
    Given "Angel 001" enable call filter "Charlie's Angels"
    Given "Angel 002" enable call filter "Charlie's Angels"
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is ringing
    Then "Angel 001" is hungup
    Then "Angel 002" is hungup
    When I wait 5 seconds for the timeout to expire
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    Then "Angel 002" is ringing

  Scenario: Strategy "all-surrogates-then-all-recipients"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Charlie   | Unknown  | 1001  | default | yes        |
      | Angel     | 001      | 1002  | default | yes        |
      | Angel     | 002      | 1003  | default | yes        |
      | Bad       | Guy      | 1010  | default | yes        |
    Given there are call filters with infos:
      | name             | strategy                           | recipients      | surrogates          | surrogates_timeout | caller_id_mode | caller_id_name |
      | Charlie's Angels | all-surrogates-then-all-recipients | Charlie Unknown | Angel 001,Angel 002 | 5                  | overwrite      | FILTER         |
    Given "Angel 001" enable call filter "Charlie's Angels"
    Given "Angel 002" enable call filter "Charlie's Angels"
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing showing "FILTER"
    Then "Angel 002" is ringing showing "FILTER"
    When I wait 5 seconds for the timeout to expire
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is hungup
    Then "Angel 002" is hungup
    # NOTE(fblackburn): if surrogates hangup, recipients will not ring

  Scenario: Strategy "linear-surrogates-then-all-recipients"
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone |
      | Charlie   | Unknown  | 1001  | default | yes        |
      | Angel     | 001      | 1002  | default | yes        |
      | Angel     | 002      | 1003  | default | yes        |
      | Bad       | Guy      | 1010  | default | yes        |
    Given there are call filters with infos:
      | name             | strategy                              | recipients      | surrogates          |
      | Charlie's Angels | linear-surrogates-then-all-recipients | Charlie Unknown | Angel 001,Angel 002 |
    Given "Angel 001" enable call filter "Charlie's Angels"
    Given "Angel 002" enable call filter "Charlie's Angels"
    When "Bad Guy" calls "1001"
    When I wait 2 seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    Then "Angel 002" is hungup
    When "Angel 001" hangs up
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is hungup
    Then "Angel 002" is ringing
    # NOTE(fblackburn): if surrogates hangup, recipients will not ring
