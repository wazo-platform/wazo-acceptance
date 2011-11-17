Feature: User
    In order to get a user
    I have to create a user

    Scenario Outline: Add_a_user_with_first_name_and_last_name_and_remove_it
        Given I login as root with password superpass at http://skaro-daily.lan-quebec.avencall.com/
        When I create a user John Willis
        Then user John Willis is displayed in the list
        When user John Willis is removed
        Then user John Willis is not displayed in the list
