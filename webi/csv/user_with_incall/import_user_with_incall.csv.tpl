entityid|firstname|lastname|language|phonenumber|context|protocol|mobilephonenumber|incallexten|incallcontext
{% for user in users -%}
{{ user.entityid }}|{{ user.firstname }}|{{ user.lastname }}|{{ user.language }}|{{ user.phonenumber }}|{{ user.context }}|{{ user.protocol }}|{{ user.mobilephonenumber }}|{{ user.incallexten }}|{{ user.incallcontext }}
{% endfor %}
