Feature: PSTN mobile fallback

  Scenario: PSTN fallback call is triggered when push notification is not answered in time
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | username | password | ring_seconds | mobile_phone_number | mobile_fallback_enabled |
      | Rick      | Grimes   |       |         |            | rick     | gR1m3    | 20           | 1803                | yes                     |
      | Daryl     | Dixon    | 1802  | default | yes        | daryl    | d1x0N    |              |                     |                         |
      | Carol     | Peletier | 1803  | default | yes        |          |          |              |                     |                         |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    When "Daryl Dixon" calls "1801"
    Then "Rick Grimes" is ringing on its contact "1"
    When I wait 12 seconds for the end of ringing time
    Then "Carol Peletier" is ringing

  Scenario: PSTN fallback is not triggered when mobile_fallback_enabled is false
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | with_phone | username | password | ring_seconds | mobile_phone_number | mobile_fallback_enabled |
      | Rick      | Grimes   |       |         |            | rick     | gR1m3    | 20           | 1803                | no                      |
      | Daryl     | Dixon    | 1802  | default | yes        | daryl    | d1x0N    |              |                     |                         |
      | Carol     | Peletier | 1803  | default | yes        |          |          |              |                     |                         |
    Given "Rick Grimes" has lines:
      | name  | exten | context | with_phone | webrtc |
      | rick1 | 1801  | default | yes        | no     |
      | rick2 | 1801  | default | no         | yes    |
    Given I create a mobile session with username "rick" password "gR1m3"
    When "Daryl Dixon" calls "1801"
    Then "Rick Grimes" is ringing on its contact "1"
    When I wait 12 seconds for the end of ringing time
    Then "Carol Peletier" is not ringing
