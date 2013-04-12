Feature: Devices

    Scenario: Creating a campaign
    	Given there are queues with infos:
            |      name     |     display name    | number | context |
            | campaignqueue |    campaignqueue    | 3105   | default |
    	Given there is no campaign "sample campaign"
    	When I create a campaign with the following parameters:
			|      name       |     queue      | start_date |  end_date  |
    		| sample campaign | campaignqueue | 2012-01-01 | 2012-02-02 |
    	Then there is a campaign in the list with the following values:
    		|      name       |     queue      | start_date |  end_date  |
    		| sample campaign |  campaignqueue | 2012-01-01 | 2012-02-02 |
    	
    Scenario: Editing a campaign
    	Given there is a campaign "sample campaign"
    	When I edit the campaign "sample campaign" with the values:
    		|        name        | start_date |  end_date  |
    		| my sample campaign | 2012-02-02 | 2012-03-03 |
    	Then there is a campaign in the list with the following values:
    		|        name        | start_date |  end_date  |
    		| my sample campaign | 2012-02-02 | 2012-03-03 |
    		
    Scenario: Deleting a campaign
    	Given there is a campaign "my sample campaign" with no recording
    	When I delete the campaign "my sample campaign"
    	Then campaign "my sample campaign" is not displayed in the list
