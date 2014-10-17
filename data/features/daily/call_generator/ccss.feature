Feature: CCSS

     Scenario: CCSS after no-answer
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     | A        |   1100 | default | sip      |
         | Bob       | B        |   1101 | default | sip      |
         When "Alice A" calls "1101"
         When "Alice A" waits for 3 seconds
         When "Alice A" hangs up
         When "Alice A" calls "*40" and waits until the end

         When "Bob B" calls "*10"
         When "Bob B" waits for 3 seconds
         When "Bob B" hangs up

         Then "Alice A" is ringing
         When "Alice A" answers
         Then "Bob B" is ringing
         When "Bob B" answers
         Then "Alice A" is talking
         Then "Bob B" is talking

     Scenario: CCSS requested then cancelled after no-answer
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Alice     | A        |   1100 | default | sip      |
         | Bob       | B        |   1101 | default | sip      |
         When "Alice A" calls "1101"
         When "Alice A" waits for 3 seconds
         When "Alice A" hangs up
         When "Alice A" calls "*40" and waits until the end
         When "Alice A" calls "*40" and waits until the end

         When "Bob B" calls "*10"
         When "Bob B" waits for 3 seconds
         When "Bob B" hangs up

         Then "Alice A" is hungup
