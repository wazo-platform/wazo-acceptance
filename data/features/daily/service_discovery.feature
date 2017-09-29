Feature: Service discovery

    Scenario Outline: Get services from consul
        Then consul returns a running "<service>" service

    Examples:
        | service       |
        | xivo-agentd   |
        | xivo-ctid     |
        | xivo-ctid-ng  |
        | xivo-dird     |
        | wazo-auth     |
        | wazo-plugind  |
        | wazo-webhookd |
