Feature: User

    Scenario: Enable XiVO Client
        Given there are users with infos:
        | firstname | lastname | cti_profile | cti_login | cti_passwd |
        | Charles   | Magne    |   Client    | charles   | magne      |

        When I start the XiVO Client
        When I disable auto-reconnect
        When I disable access to XiVO Client to user "Charles" "Magne"
        Then I can't connect the CTI Client with "charles" "magne"
        When I enable access to XiVO Client to user "Charles" "Magne"
        Then I can connect the CTI Client with "charles" "magne"
