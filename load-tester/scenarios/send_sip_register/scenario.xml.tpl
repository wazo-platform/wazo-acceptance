<?xml version="1.0" encoding="ISO-8859-1" ?>
<scenario name="register with auth">

<send retrans="500">
  <![CDATA[
    REGISTER sip:[remote_ip]:[remote_port] SIP/2.0
    Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]
    Max-Forwards: 70
    To: <sip:[field0]@[remote_ip]:[remote_port]>
    From: <sip:[field0]@[remote_ip]:[remote_port]>;tag=[call_number]
    Call-ID: [call_id]
    CSeq: [cseq] REGISTER
    Contact: <sip:[field0]@[local_ip]:[local_port]>
    Content-Length: 0
    Expires: {{ expires }}

  ]]>
</send>

<recv response="401" auth="true">
</recv>

<send retrans="500">
  <![CDATA[
    REGISTER sip:[remote_ip]:[remote_port] SIP/2.0
    Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]
    Max-Forwards: 70
    To: <sip:[field0]@[remote_ip]:[remote_port]>
    From: <sip:[field0]@[remote_ip]:[remote_port]>;tag=[call_number]
    Call-ID: [call_id]
    CSeq: [cseq] REGISTER
    Contact: <sip:[field0]@[local_ip]:[local_port]>
    [field1]
    Content-Length: 0
    Expires: {{ expires }}

  ]]>
</send>

<recv response="200">
</recv>

</scenario>

