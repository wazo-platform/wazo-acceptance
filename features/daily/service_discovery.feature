Feature: Service discovery

    Scenario Outline: Get services from consul
        Then consul returns a running "<service>" service

    Examples:
        | service       |
        | wazo-agentd   |
        | wazo-auth     |
        | wazo-calld    |
        | wazo-chatd    |
        | wazo-confd    |
        | wazo-dird     |
        | wazo-plugind  |
        | wazo-setupd   |
        | wazo-webhookd |
