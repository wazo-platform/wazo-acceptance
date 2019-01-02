Feature: Xlet identity

    Scenario: Display identity infos
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd |
         | Yoda      | Kenobi   | Client      | yoda      | kenobi     |

        When I start the XiVO Client
        When I log in the XiVO Client as "yoda", pass "kenobi"

        Then the Xlet identity shows name as "Yoda" "Kenobi"

    Scenario: Display voicemail icon and number
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | cti_login | cti_passwd | voicemail_name  | voicemail_number | voicemail_context |
         | Bail      | Tarkin   | 1152   | default | Client      | bail      | tarkin     | 1152            | 1152             | default           |

        When I start the XiVO Client
        When I log in the XiVO Client as "bail", pass "tarkin"
        Then the Xlet identity shows a voicemail "1152"

    Scenario: Display agent icon and number
        Given there are users with infos:
         | firstname | lastname  | agent_number | cti_profile | cti_login | cti_passwd |
         | Darth     | Chewbacca | 1153         | Client      | darth     | chewbacca  |

        When I start the XiVO Client
        When I log in the XiVO Client as "darth", pass "chewbacca", unlogged agent
        Then the Xlet identity shows an agent

        When I log out of the XiVO Client
        When I delete agent number "1153"

        When I log in the XiVO Client as "darth", pass "chewbacca"
        Then the Xlet identity does not show any agent
