Feature: CTI Server

    Scenario: Default Services Activated
        When i edit CTI Profile "client"
        Then i see default services activated
