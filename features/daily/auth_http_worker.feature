Feature: wazo-auth HTTP workers

  Scenario: the HTTP worker serves requests without running background jobs
    Given an HTTP worker is running
    When I send 50 requests to the local auth API
    Then the HTTP worker served at least one request
    And the HTTP worker does not run the expired-token remover
