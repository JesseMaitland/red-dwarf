UNLOAD
('
SELECT *
  FROM {{config.schema}}.{{config.table}}
 WHERE {{config.timestamp_column}} < DATEADD(DAY, -{{config.days_to_keep}}, GETDATE())
')
TO 's3://{{config.s3_bucket}}/{{config.s3_key}}/';
