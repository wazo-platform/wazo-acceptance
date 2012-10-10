<?xml version="1.0" encoding="ISO-8859-1" ?>
<scenario name="answer call then wait">

<recv request="INVITE">
</recv>

<send>
  <![CDATA[
    SIP/2.0 180 Ringing
    [last_Via:]
    [last_To:];tag=[call_number]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Contact: <sip:[local_ip]:[local_port]>
    Content-Length: 0

  ]]>
</send>

<pause{% for k, v in (pause|default({})).iteritems() %} {{ k }}="{{ v }}"{% endfor %}/>

<send retrans="500">
  <![CDATA[
    SIP/2.0 200 OK
    [last_Via:]
    [last_To:];tag=[call_number]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Contact: <sip:[local_ip]:[local_port]>
    Content-Type: application/sdp
    Content-Length: [len]

    v=0
    o=user1 53655765 2353687637 IN IP[local_ip_type] [local_ip]
    s=-
    c=IN IP[media_ip_type] [media_ip]
    t=0 0
    m=audio [media_port] RTP/AVP 3
    a=rtpmap:3 GSM/8000
    a=ptime:20
    a=sendrecv

  ]]>
</send>

<recv request="ACK">
</recv>

<nop>
  <action>
    <exec play_pcap_audio="silence600s-gsm.pcap"/>
  </action>
</nop>

<recv request="BYE">
</recv>

<send>
  <![CDATA[
    SIP/2.0 200 OK
    [last_Via:]
    [last_To:]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Contact: <sip:[local_ip]:[local_port]>
    Content-Length: 0

  ]]>
</send>

</scenario>
