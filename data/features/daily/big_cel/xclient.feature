Feature: XiVOClient

    Scenario: Add a user and connect it to XiVOClient
        Given there are users with infos:
          | firstname | lastname   | cti_profile | cti_login | cti_passwd | protocol | number | context |
          | Abraham   | Washington | Client      | abraham   | washington | sip      |  1777  | default |
        When I start the XiVO Client
        Then I can connect the CTI Client with "abraham" "washington"
