Feature: Switchboard
    Scenario: Setup
        Given there are users with infos:
        | firstname | lastname    | cti_profile | cti_login | cti_passwd | number | context | agent_number |
        | Switch    | Board       | Switchboard | switch    | board      |   1631 | default |         1631 |
        | User      | Caller      |             |           |            |   1784 | default |              |
        | Transfer  | Destination |             |           |            |   1863 | default |              |
        Given the user "Switch Board" is configured for switchboard use
        Given there is a switchboard configured as:
        | incalls queue name | hold calls queue name   | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
        | __switchboard-test | __switchboard_hold-test | 3009                 | default               | 3010                    | default                  | 1631@default |
