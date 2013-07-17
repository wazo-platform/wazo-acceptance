Feature: SCCP calls

    Scenario: Alice calls the phone status extension
      Given there are users with infos:
      | firstname | number | context | protocol | device | register |
      | Alice     |  1234  | default | sccp     | auto   |     yes  |
      When "Alice" calls "*10"
      Then I see a "Playback" "status-phone" on line "SCCP/1234" in the asterisk log
