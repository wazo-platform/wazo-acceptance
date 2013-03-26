Feature: User

    Scenario: Add a user with first name and last name and remove it
        Given there is no user "John" "Willis"
        When I create a user "John" "Willis"
        Then user "John Willis" is displayed in the list
        When I remove user "John" "Willis"
        Then user "John Willis" is not displayed in the list

    Scenario: Add a user in a group
        Given there is a user "Bob" "Marley" with extension "1101@default" in group "rastafarien"
        When I rename "Bob" "Marley" to "Bob" "Dylan"
        Then I should be at the user list page
        Then "Bob" "Dylan" is in group "rastafarien"

    Scenario: Update a user
        Given there is no user "Bill" "Bush"
        When I create a user "Bill" "Bush"
        Then user "Bill Bush" is displayed in the list
        When I rename "Bill" "Bush" to "George" "Orwell"
        Then user "George Orwell" is displayed in the list

    Scenario: Save user and line forms
    # The problem is that saving the user form may erase values previously
    # set in the line form (bug #2918)
        Given there are users with infos:
        | firstname | lastname | number | context |
        | Tom       | Sawyer   |   1405 | default |
        Given I set the following options in line "1405":
        | NAT | IP addressing type | IP address |
        | No  | Static             | 10.0.0.1   |
        Then the line "1405" has the following line options:
        | Call limit |
        |         10 |
        When I edit the user "Tom" "Sawyer" without changing anything
        Then the line "1405" has the following line options:
        | NAT | IP addressing type | IP address |
        | No  | Static             |   10.0.0.1 |

    Scenario: Save user and voicemail forms
        Given there is a user "Tom" "Sawyer" with extension "1405@default"
        Given there is no voicemail "1405"
        When I add a voicemail "" to the user "Tom" "Sawyer" with errors
        Then I see errors
        When I add a voicemail "1405" to the user "Tom" "Sawyer"
        Then voicemail "1405" is displayed in the list

    Scenario: Delete user in group
        Given there is a user "Tom" "Sawyer" with extension "1405@default" in group "american_dream"
        When I remove user "Tom" "Sawyer"
        Then I see a group "american_dream" with no users

    Scenario: Delete user in queue
        Given there is a user "Tom" "Sawyer" with extension "1405@default"
        Given there are queues with infos:
            |      name      |  display name  | number | context | users_number |
            | americandream  | American Dream |  3203  | default |    1405      |
        When I remove user "Tom" "Sawyer"
        Then there is no data about this user remaining in the database.

    Scenario: Add user with function keys
        When I add a user "Tom" "Sawyer" with a function key with type Customized and extension "1234"
        Then I see the user "Tom" "Sawyer" exists
        Then i see user with username "Tom" "Sawyer" has a function key with type Customized and extension "1234"

    Scenario: Delete line from user with voicemail
        Given there is a user "Abraham" "Maharba" with extension "1456@default" and voicemail
        When I remove line from user "Abraham" "Maharba" with errors
        Then I see errors
        When I remove line "1456" from lines then I see errors
