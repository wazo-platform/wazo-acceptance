entityid|firstname|lastname|language|phonenumber|context|protocol|mobilephonenumber|voicemailname|voicemailmailbox|voicemailpassword|voicemailemail
{% for user in users -%}
{{ user.entityid }}|{{ user.firstname }}|{{ user.lastname }}|{{ user.language }}|{{ user.phonenumber }}|{{ user.context }}|{{ user.protocol }}|{{ user.mobilephonenumber }}|{{ user.firstname }} {{ user.lastname }}|{{ user.mailbox }}|{{ user.mailbox_passwd }}|{{ user.mailbox_mail }}
{% endfor %}
