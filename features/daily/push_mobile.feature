Feature: Push mobile

  Scenario: No push when no WebRTC line
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone |
      | Rick      | Grimes   |        |         |            |
      | Daryl     | Dixon    | 1802   | default | yes        |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone |
      | rick1 | 1801  | default | yes        |
    Given I listen on the bus for "call_push_notification" messages
    When "Daryl Dixon" calls "1801"
    Then "Rick Grimes" is ringing on its contact "1"
    Then I receive no "call_push_notification" event

  Scenario: Push notification is triggered with WebRTC line and mobile session one line
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone |
      | Rick      | Grimes   |        |         |            |
      | Daryl     | Dixon    | 1802   | default | yes        |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | no         | yes    |
    Given I listen on the bus for "call_push_notification" messages
    When "Daryl Dixon" calls "1801"
    Then I receive no "call_push_notification" event

  Scenario: Push notification is triggered by mobile session and WebRTC line
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone | username | password |
      | Rick      | Grimes   |        |         |            | rick     | gR1m3    |
      | Daryl     | Dixon    | 1802   | default | yes        | daryl    | d1x0N    |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    Given I listen on the bus for "call_push_notification" messages
    When "Daryl Dixon" calls "1801"
    Then "Rick Grimes" is ringing on its contact "1"
    Then I receive a "call_push_notification" event

  Scenario: Push notification is not triggered by a WebRTC line with no mobile session
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone | username | password |
      | Rick      | Grimes   |        |         |            | rick     | gR1m3    |
      | Daryl     | Dixon    | 1802   | default | yes        | daryl    | d1x0N    |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I listen on the bus for "call_push_notification" messages
    When "Daryl Dixon" calls "1801"
    Then "Rick Grimes" is ringing on its contact "1"
    Then I receive no "call_push_notification" event

  Scenario: Cancel push notification is triggered when caller hangs up
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone | username | password |
      | Rick      | Grimes   |        |         |            | rick     | gR1m3    |
      | Daryl     | Dixon    | 1802   | default | yes        | daryl    | d1x0N    |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    Given I listen on the bus for "call_cancel_push_notification" messages
    Given "Daryl Dixon" calls "1801"
    Given "Rick Grimes" is ringing on its contact "1"
    When "Daryl Dixon" hangs up
    Then I receive a "call_cancel_push_notification" event

  Scenario: Cancel push notification is triggered when the call is answered
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone | username | password |
      | Rick      | Grimes   |        |         |            | rick     | gR1m3    |
      | Daryl     | Dixon    | 1802   | default | yes        | daryl    | d1x0N    |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    Given I listen on the bus for "call_cancel_push_notification" messages
    Given "Daryl Dixon" calls "1801"
    Given "Rick Grimes" is ringing on its contact "1"
    When "Rick Grimes" answers on its contact "1"
    Then I receive a "call_cancel_push_notification" event

  Scenario: Cancel push notification is triggered when rejecting the call
    Given there are telephony users with infos:
      | firstname | lastname | exten  | context | with_phone | username | password |
      | Rick      | Grimes   |        |         |            | rick     | gR1m3    |
      | Daryl     | Dixon    | 1802   | default | yes        | daryl    | d1x0N    |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    Given I listen on the bus for "call_cancel_push_notification" messages
    Given "Daryl Dixon" calls "1801"
    Given "Rick Grimes" is ringing on its contact "1"
    When "Rick Grimes" hangs up on its contact "1"
    Then I receive a "call_cancel_push_notification" event
