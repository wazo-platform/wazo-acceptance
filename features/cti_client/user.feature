Feature: CTI User

    Scenario: Start XiVO Client with a new user
        Given there are users with infos:
        | firstname | lastname   | cti_profile | cti_login | cti_passwd |
        | Abraham   | Washington | noservices  | abraham   | washington |

        When I start the XiVO Client
        Then I can connect the CTI Client of "Abraham" "Washington"
        