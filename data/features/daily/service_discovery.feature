Feature: Service discovery

    Scenario: Get xivo-ctid-ng from consul
        Then consul returns a running "xivo-ctid-ng" service
