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
    | GET    | /api/ctid-ng/1.0/status      |
    | GET    | /api/dird/0.1/config         |
    | GET    | /api/plugind/0.2/config      |
    | GET    | /api/provd/configure         |
    | GET    | /api/webhookd/1.0/config     |
    | GET    | /api/websocketd/             |
