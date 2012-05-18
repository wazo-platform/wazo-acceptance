SEQUENTIAL
{% for called_exten in called_extens -%}
{{ calling_line.username }};[authentication username={{ calling_line.username }} password={{ calling_line.password }}];{{ called_exten }}
{% endfor %}

