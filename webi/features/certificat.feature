Feature: Certificats

         Scenario: Create a certificat with invalid info
                   Given There are no certificats named "Cert"
                   When i create a certificat with name "Cert" and with email "test@test@test.com" and validity date "10/18/2014"
                   When i submit with errors
                   When i create a certificat with name "Cert" and with email "test@test.com" and validity date "10/18/2014"
                   When i submit
                   Then I see no errors
		   		   