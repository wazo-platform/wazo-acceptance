SEQUENTIAL
{% for line in lines -%}
{{ line.username }};[authentication username={{ line.username }} password={{ line.password }}]
{% endfor %}

