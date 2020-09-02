{% extends "base.sql" %}
{%block unload%}
UNLOAD
('
SELECT *
  FROM {{config.table.schema}}.{{config.table.name}}
 WHERE {{config.partition.column}} < ''{{config.execution.start_date}}''
')
TO 's3://{{config.s3.bucket}}/{{config.s3.key_prefix}}/'
IAM_ROLE '{{config.s3.iam_role}}'
{% for option in config.unload.options %}
{{option}}
{%endfor%}
PARTITION BY();
{% endblock %}
{%block delete%}
{% if config.unload.delete%}
DELETE
  FROM {{config.table.schema}}.{{config.table.name}}
 WHERE {{config.partition.column}} < '{{config.execution.start_date}}';
{%endif%}
{% endblock %}
