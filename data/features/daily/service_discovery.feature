Feature: Service discovery

    Scenario Outline: Get services from consul
        Then consul returns a running "<service>" service

    Examples:
        | service       |
        | xivo-agentd   |
        | xivo-auth     |
        | xivo-ctid     |
        | xivo-ctid-ng  |
        | xivo-dird     |
        | wazo-plugind  |
        | wazo-webhookd |
