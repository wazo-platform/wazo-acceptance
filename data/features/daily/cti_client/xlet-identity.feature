Feature: Xlet identity

    Scenario: Display identity infos
        Given there are users with infos:
         | firstname | lastname | cti_profile |
         | Yoda      | Kenobi   | Client      |

        When I start the XiVO Client
        When I log in the XiVO Client as "yoda", pass "kenobi"

        Then the Xlet identity shows name as "Yoda" "Kenobi"

    Scenario: Display voicemail icon and number
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | voicemail_name | voicemail_number | voicemail_context |
         | Bail      | Tarkin   | 1152   | default | Client      | 1152           | 1152             | default           |

        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "1152"

    Scenario: Display agent icon and number
        Given there are users with infos:
         | firstname | lastname  | agent_number | cti_profile |
         | Darth     | Chewbacca | 1153         | Client      |

        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent

        When I log out of the XiVO Client
        When I delete agent number "1153"

        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
