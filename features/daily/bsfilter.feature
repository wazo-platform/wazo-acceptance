Feature: Boss Secretary Filter

  Scenario: Login and logout an agent from function keys
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
    When I wait "4" seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint enabled
    Then "Angel 001" has function key "1" hint enabled
    When "Bad Guy" calls "1001"
    When I wait "2" seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    When "Bad Guy" hangs up

    When "Charlie Unknown" press function key "1"
    When I wait "4" seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint disabled
    Then "Angel 001" has function key "1" hint disabled
    When "Bad Guy" calls "1001"
    When I wait "2" seconds for the call processing
    Then "Charlie Unknown" is ringing
    Then "Angel 001" is hungup
    When "Bad Guy" hangs up
    
    When "Angel 001" press function key "1"
    When I wait "4" seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint enabled
    Then "Angel 001" has function key "1" hint enabled
    When "Bad Guy" calls "1001"
    When I wait "2" seconds for the call processing
    Then "Charlie Unknown" is hungup
    Then "Angel 001" is ringing
    When "Bad Guy" hangs up

    When "Angel 001" press function key "1"
    When I wait "4" seconds for the call processing
    Then "Charlie Unknown" has function key "1" hint disabled
    Then "Angel 001" has function key "1" hint disabled
    When "Bad Guy" calls "1001"
    When I wait "2" seconds for the call processing
    Then "Charlie Unknown" is ringing
    Then "Angel 001" is hungup
    
