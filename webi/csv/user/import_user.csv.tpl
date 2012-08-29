entityid|firstname|lastname|language|phonenumber|context|protocol|mobilephonenumber
{% for user in users -%}
{{ user.entityid }}|{{ user.firstname }}|{{ user.lastname }}|{{ user.language }}|{{ user.phonenumber }}|{{ user.context }}|{{ user.protocol }}|{{ user.mobilephonenumber }}
{% endfor %}
