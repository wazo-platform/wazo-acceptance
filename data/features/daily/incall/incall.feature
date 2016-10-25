Feature: Incalls

    Scenario: Incall to destination user
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |
          | Incall    | User     |   1801 | default | sip      |

        Given there is an incall "1801" in context "from-extern" to the "User" "Incall User"
        When chan_test calls "1801@from-extern"
        Then "Incall User" is ringing

