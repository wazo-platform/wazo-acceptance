Feature: User

    Scenario: Enable XiVO Client
        Given there is a user "Charles" "Magne"
        When I disable access to XiVO Client to user "Charles" "Magne"
        When I start the XiVO Client
        Then I can't connect the CTI client of "Charles" "Magne"

        When I enable access to XiVO Client to user "Charles" "Magne"
        Then I can connect the CTI client of "Charles" "Magne"
