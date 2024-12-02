Feature: HTTP

  Scenario Outline: REST APIs are reachable from port 443
    Then "<method>" "<url>" does not answer 404

  Examples:
    | method | url                          |
    | GET    | /api/agentd/1.0/agents       |
    | POST   | /api/amid/1.0/action/Command |
    | GET    | /api/asterisk/ws             |
    | GET    | /api/auth/0.1/backends       |
    | GET    | /api/call-logd/1.0/cdr       |
    | GET    | /api/calld/1.0/status        |
    | GET    | /api/chatd/1.0/status        |
    | GET    | /api/confd/1.1/infos         |
    | GET    | /api/dird/0.1/config         |
    | GET    | /api/plugind/0.2/config      |
    | GET    | /api/provd/0.2/configure     |
    | GET    | /api/webhookd/1.0/config     |
    | GET    | /api/websocketd/             |

  Scenario Outline: Unauthenticated HTTP resources are throttled
    Then "<method>" "<url>" eventually receive the answer 429 instead of "<status_code>"

  Examples:
    | method | url                                                                 | status_code |
    | GET    | /api/confd/1.1/guests/meetings/a0fede2a-55a1-44cf-8de5-f249002d8db0 | 404         |
    | GET    | /api/auth/0.1/backends                                              | 200         |
    | HEAD   | /api/auth/0.1/status                                                | 200         |
