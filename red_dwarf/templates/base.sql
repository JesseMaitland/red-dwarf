{% block unload %}
{% endblock %}

{% block delete %}
{% endblock %}

{%if config.unload.vacuum%}
VACUUM {{config.table.schema}}.{{config.table.name}};
{%endif%}
{%if config.unload.analyse%}
ANALYSE {{config.table.schema}}.{{config.table.name}};
{%endif%}
