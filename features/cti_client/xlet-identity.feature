Feature: Xlet identity

    Scenario: Display identity infos
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Yoda      | Kenobi   | 1151   | default | Client      |

        When I start the XiVO Client
        When I log in the XiVO Client as "yoda", pass "kenobi"

        Then the Xlet identity shows name as "Yoda" "Kenobi"
        Then the Xlet identity shows phone number as "1151"

    Scenario: Display voicemail icon and number
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | voicemail_name | voicemail_number |
         | Bail      | Tarkin   | 1152   | default | Client      | 1152           | 1152             |
         
        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "1152"

    Scenario: Display agent icon and number
        Given there are users with infos:
         | firstname | lastname  | agent_number | cti_profile |
         | Darth     | Chewbacca | 1153         | Client      |

        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent "Agent 1153"

        When I log out of the XiVO Client
        When I delete agent number "1153"

        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
