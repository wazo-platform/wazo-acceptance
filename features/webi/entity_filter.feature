Feature: Entity Filter

    Scenario: Context
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |
        
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module | category           | section  | active |
          | IPBX   | IPBX configuration | Contexts | yes    |
        
        Given there are contexts with infos:
          | type | name | range_start | range_end | entity_name   |
          | user | foo  | 1000        | 1101      | entity_filter |
          | user | bar  | 1000        | 1101      | default       |
        
        When I logout from the web interface
        When I login as admin1 with password admin1 in en
        
        Then I see the context "foo" exists
        Then I see the context "bar" not exists

    Scenario: User / Line
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |
        
        Given there are contexts with infos:
          | type | name | range_start | range_end | entity_name   |
          | user | foo  | 1000        | 1101      | entity_filter |
        
        Given there are users with infos:
          | firstname      | lastname | number | context | entity_name   |
          | _entity_filter | default  |   1101 | default |               |
          | _entity_filter | foo      |   1101 | foo     | entity_filter |
        
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module | category      | section | active |
          | IPBX   | IPBX settings | Users   | yes    |
          | IPBX   | IPBX settings | Lines   | yes    |
          
        When I logout from the web interface
        When I login as admin1 with password admin1 in en
        
        When I search for user "_entity_filter" "foo"
        Then user "_entity_filter foo" is displayed in the list
        When I search for user "_entity_filter" "default"
        Then user "_entity_filter default" is not displayed in the list

        Then I see the line "1101" exists
        Then I see the line "1501" not exists

    Scenario: Group
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |
        
        Given there are contexts with infos:
          | type  | name | range_start | range_end | entity_name   |
          | group | foo  | 2000        | 2999      | entity_filter |
        
        Given there are groups:
         | name          | exten | context |
         | groupeeeeeeee |  2222 | default |
         | entity_filter |  2555 | foo     |
        
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module | category      | section | active |
          | IPBX   | IPBX settings | Groups  | yes    |
        
        When I logout from the web interface
        When I login as admin1 with password admin1 in en

        Then I see the group "entity_filter" exists
        Then I see the group "groupeeeeeeee" not exists

    Scenario: Voicemail
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |
        
        Given I have the following voicemails:
          | name          | number | context |
          | entity_filter |  1234  | foo     |
          | vm003         |  4321  | default |
        
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module | category      | section    | active |
          | IPBX   | IPBX settings | Voicemails | yes    |
          
        When I logout from the web interface
        When I login as admin1 with password admin1 in en

        Then I see the voicemail "entity_filter" exists
        Then I see the voicemail "groupeeeeeeee" not exists
