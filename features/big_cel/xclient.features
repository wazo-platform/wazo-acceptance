Feature: XiVOClient

    Scenario: Add a user and connect it to XiVOClient
        Given there are users with infos:
          | firstname | lastname   | cti_profile | cti_login | cti_passwd |
          | Abraham   | Washington | Client      | abraham   | washington |
        When I start the XiVO Client
        Then I can connect the CTI Client of "Abraham" "Washington" 192.168.32.174
        