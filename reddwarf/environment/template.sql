UNLOAD
('
   SELECT * {% if config.cast_partition_by_time %},
          {{config.partition_by}}::DATE AS event_date {% endif %}
     FROM {{config.schema}}.{{config.table}}
    WHERE {{config.timestamp_column}} < DATEADD(DAY, -{{config.days_to_keep}}, GETDATE())
')
TO 's3://{{config.s3_bucket}}/{{config.s3_key}}/'
IAM_ROLE '{{iam_role}}'
FORMAT {{config.unload_format.upper()}}
PARTITION BY({% if config.cast_partition_by_time %} event_date {% else %} {{config.partition_by}} {% endif %})
ALLOWOVERWRITE;
