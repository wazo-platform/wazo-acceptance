Feature: Files

    Scenario: Add a long file name
        Given a recording file with name "a.wav"
        Given a recording file with name "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.wav"
        Given a recording file with name "rec-1316188241-166453-sip-lasotel-in-23-000158c6-out.wav.wav"
        Then recording file "a.wav" is displayed in the list
        Then recording file "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.wav" is displayed in the list
        Then recording file "rec-1316188241-166453-sip-lasotel-in-23-000158c6-out.wav.wav" is displayed in the list

    Scenario: List g722 asterisk moh sound
        Given a musiconhold file with name "macroform-cold_day.g722"
        Then musiconhold file "macroform-cold_day.g722" is displayed in the list

    Scenario: Recording meetme
        Given a recording meetme file with name "meetme-4000-1351609395.wav"
        Then recording meetme file "meetme-4000-1351609395.wav" is displayed in the list
