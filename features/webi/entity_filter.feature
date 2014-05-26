Feature: Entity Filter

    Scenario: Context / User / Line / Group / Voicemail / Conference Room / Incall / Queue / Agent
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |
        
        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module      | category           | section  |   active |
          | IPBX        | IPBX configuration | Contexts   | yes    |
          | IPBX        | IPBX settings      | Users      | yes    |
          | IPBX        | IPBX settings      | Lines      | yes    |
          | IPBX        | IPBX settings      | Groups     | yes    |
          | IPBX        | IPBX settings      | Voicemails | yes    |
          | IPBX        | IPBX settings      | Meetme     | yes    |
          | IPBX        | Call Management    | Incall     | yes    |
          | Call Center | Settings           | Queues     | yes    |
          | Call Center | Settings           | Agents     | yes    |
        
        Given there are contexts with infos:
          | type   | name    | range_start | range_end | entity_name   | didlength |
          | user   | foo     | 1000        | 1101      | entity_filter |           |
          | user   | bar     | 1000        | 1101      | default       |           |
          | group  | foo     | 2000        | 2999      | entity_filter |           |
          | queue  | foo     | 3000        | 3999      | entity_filter |           |
          | meetme | foo     | 4000        | 4999      | entity_filter |           |
          | incall | alberta | 1000        | 4999      | entity_filter | 4         |
        
        Given there are users with infos:
          | firstname      | lastname | number | context | entity_name   |
          | _entity_filter | default  |   1101 | default |               |
          | _entity_filter | foo      |   1101 | foo     | entity_filter |
          
        Given there are groups:
          | name          | exten | context |
          | groupeeeeeeee |  2222 | default |
          | entity_filter |  2555 | foo     |
        
        Given I have the following voicemails:
          | name          | number | context |
          | entity_filter |  1234  | foo     |
          | vm003         |  4321  | default |
        
        Given there are the following conference rooms:
          | name          | number | context |
          | entity_filter |  4234  | foo     |
          | mm001         |  4321  | default |
        
        Given there is no incall "4234" in context "alberta"
        When I create an incall with DID "4234" in context "alberta (alberta)"
        Given there is no incall "4321" in context "from-extern"
        When I create an incall with DID "4321" in context "Incalls (from-extern)"
        
        Given there is a agent "entity_filter" "" with extension "1111@foo"
        Given there is a agent "agent02" "" with extension "2222@default"
        
        Given there are queues with infos:
          | name           | display name   | number | context |
          | qentity_filter | qentity_filter | 3000   | foo     |
          | q01            | q01            | 3001   | default |
        
        When I logout from the web interface
        When I login as admin1 with password admin1 in en
        
        Then I see the context "foo" exists
        Then I see the context "bar" not exists
        
        When I search for user "_entity_filter" "foo"
        Then user "_entity_filter foo" is displayed in the list
        When I search for user "_entity_filter" "default"
        Then user "_entity_filter default" is not displayed in the list

        Then I see the line "1101" exists
        Then I see the line "1501" not exists

        Then I see the group "entity_filter" exists
        Then I see the group "groupeeeeeeee" not exists

        Then I see the voicemail "entity_filter" exists
        Then I see the voicemail "vm003" not exists

        Then I see the conference room "entity_filter" exists
        Then I see the conference room "mm001" not exists

        Then I see the incall "4234" exists
        Then I see the incall "4321" not exists
        
        Then agent "entity_filter" is displayed in the list of "default" agent group
        Then agent "agent02" is not displayed in the list of "default" agent group
       
        Then I see the queue "qentity_filter" exists
        Then I see the queue "q01" not exists
        