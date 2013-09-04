Feature: Call Log access via Webi

    Scenario: Request call logs with start date but no end date
        When I request call logs in the webi with dates:
          |      start | end |
          | 2013-01-01 |     |
        #  for call logs from "2013-01-01T00:00:00" to today
        Then the REST API received a request with infos:
          | path           | query                                                                     |
          | /1.1/call_logs | start_date=2013-01-01T00:00:00&end_date=\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d |
