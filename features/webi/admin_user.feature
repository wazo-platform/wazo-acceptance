Feature: Admin User

    Scenario: Add an admin user with limited access
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1"
        When I assign the following rights to the admin user "admin1":
          | module        | category         | section      | active |
          | Configuration | Management       | Directories  | yes    |
          | IPBX          | General settings | SIP Protocol | yes    |
        When I logout from the web interface
        When I login as admin1 with password admin1 in en
        Then I can access the directory configuration
        Then I see no errors
        Then I can access the SIP Protocol configuration
        Then I see no errors
        Then I cannot access the SCCP Protocol configuration
