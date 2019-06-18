Feature: Service discovery

    Scenario Outline: Get services from consul
        Then consul returns a running "<service>" service

    Examples:
        | service       |
        | xivo-ctid     |
        | xivo-ctid-ng  |
        | wazo-agentd   |
        | wazo-auth     |
        | wazo-dird     |
        | wazo-plugind  |
        | wazo-webhookd |
