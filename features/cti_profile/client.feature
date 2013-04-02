Feature: CTI Profile

    Scenario: Start XiVO Client without any services enabled
        Given there is a profile "noservices" with no services and xlets:
        | xlet     |
        | Features |

        Given there are users with infos:
        | firstname | lastname   | cti_profile | cti_login | cti_passwd |
        | Abraham   | Washington | noservices  | abraham   | washington |

        When I start the XiVO Client
        Then I can connect the CTI Client of "Abraham" "Washington"
