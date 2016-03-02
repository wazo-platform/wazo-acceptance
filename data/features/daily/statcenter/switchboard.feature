Feature: Switchboard statistics

  Scenario: Call abandoned in the incoming queue
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    Given "Bob B" calls "3009"
    Given "Alice A" is ringing
    When "Bob B" hangs up
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardAbandonedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call abandoned in the hold queue
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number | cti_login | cti_passwd | cti_profile |
    | Alice     | A        |   1001 | default | sip      |         1001 | alicea    | secr37     | Switchboard |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    Given "Bob B" calls "3009"
    Given "Alice A" answers
    Given I connect to xivo-ctid:
    | username | password |
    | alicea   | secr37   |
    Given I send a SwitchboardHold message
    When "Bob B" hangs up
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardAbandonedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call transferred
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    | Charles   | C        |   1003 | default | sip      |
    Given "Bob B" calls "3009"
    Given "Alice A" is ringing
    Given "Alice A" answers
    When "Alice A" transfers to "1003"
    Then I should receive the following switchboard statistics:
    | Event                       |
    | SwitchboardEnteredEvent     |
    | SwitchboardTransferredEvent |
    | SwitchboardWaitTimeEvent    |

  Scenario: Call answered by the operator with no transfer
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    Given "Bob B" calls "3009"
    Given "Alice A" answers
    When "Bob B" hangs up
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardCompletedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call on a full switchboard
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    | Charles   | C        |   1003 | default | sip      |
    Given the switchboard is configured to receive a maxium of "1" call
    Given "Bob B" calls "3009"
    When "Charles C" calls "3009" and waits until the end
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardForwardedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call on no answer
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    When "Bob B" calls "3009" and waits until the end
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardForwardedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call on no agent logged
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number | logged |
    | Alice     | A        |   1001 | default | sip      |         1001 | false  |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    When "Bob B" calls "3009" and waits until the end
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardForwardedEvent |
    | SwitchboardWaitTimeEvent  |

  Scenario: Call on all agents leaving
    Given a configured switchboard with an operator with infos:
    | firstname | lastname | number | context | protocol | agent_number |
    | Alice     | A        |   1001 | default | sip      |         1001 |
    Given there are users with infos:
    | firstname | lastname | number | context | protocol |
    | Bob       | B        |   1002 | default | sip      |
    Given "Bob B" calls "3009" and waits until the end
    When I unlog agent "1001"
    Then I should receive the following switchboard statistics:
    | Event                     |
    | SwitchboardEnteredEvent   |
    | SwitchboardForwardedEvent |
    | SwitchboardWaitTimeEvent  |
