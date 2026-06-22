SELECT COUNT(*)
FROM bronze.schema_registry
WHERE schema_id = 4;



SELECT *
FROM bronze.schema_registry
WHERE schema_id = 4
LIMIT 10;



CREATE TABLE bronze.figure_schema_4 (

    id BIGSERIAL PRIMARY KEY,

    source_file TEXT,

    year TEXT,
    survey_question TEXT,
    response TEXT,
    grouping_variable TEXT,
    category TEXT,

    value NUMERIC,
    value_unit TEXT,
    value_label TEXT,

    null_reason TEXT,
    metadata_1 TEXT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT
    schema_id,
    schema_name,
    file_count,
    jsonb_pretty(column_list)
FROM bronze.schema_registry
WHERE schema_id = 4;
	
	SELECT
	    COUNT(*)
	FROM bronze.schema_registry
	WHERE schema_id = 4;

SELECT *
FROM bronze.schema_registry
WHERE schema_id = 4
LIMIT 5;


SELECT *
FROM bronze.file_catalog
WHERE source_folder = 'Figure.nz data'
LIMIT 20;

SELECT *
FROM bronze.file_catalog
LIMIT 20;

SELECT
    COUNT(*)
FROM bronze.schema_registry
WHERE schema_id = 4;

SELECT *
FROM bronze.schema_registry
WHERE schema_id = 4
LIMIT 5;

SELECT COUNT(*)
FROM bronze.file_catalog
WHERE minio_path LIKE '%Adults taking part in sport and active recreation%'
   OR minio_path LIKE '%Participation%'
   OR minio_path LIKE '%active recreation%';

SELECT
    file_name,
    minio_path
FROM bronze.file_catalog
WHERE source_folder = 'Figure.nz data'
AND file_extension = 'csv'
ORDER BY file_name
LIMIT 50;


SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'bronze'
AND table_name = 'file_catalog';



CREATE TABLE bronze.schema_files (
    schema_id INT,
    file_name TEXT,
    minio_path TEXT
);


CREATE TABLE bronze.schema_files (
    id SERIAL PRIMARY KEY,
    schema_id INT,
    file_name TEXT,
    minio_path TEXT,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT COUNT(*)
FROM bronze.schema_files;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'bronze'
AND table_name = 'schema_registry'
ORDER BY ordinal_position;



DROP TABLE IF EXISTS bronze.figure_schema_4;

CREATE TABLE bronze.figure_schema_4 (
    id BIGSERIAL PRIMARY KEY,
    source_file TEXT,

    year TEXT,
    survey_question TEXT,
    response TEXT,
    grouping_variable TEXT,
    category TEXT,

    value NUMERIC,
    value_unit TEXT,
    value_label TEXT,

    null_reason TEXT,
    metadata_1 TEXT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT *
FROM bronze.figure_schema_4
LIMIT 1;


SELECT
    schema_id,
    schema_name,
    file_count
FROM bronze.schema_registry
ORDER BY file_count DESC;

SELECT
    schema_id,
    COUNT(*) AS files
FROM bronze.schema_files
GROUP BY schema_id
ORDER BY files DESC;

SELECT
    file_name,
    minio_path
FROM bronze.file_catalog
WHERE minio_path ILIKE '%Current ratio%'
LIMIT 20;

CREATE TABLE bronze.figure_schema_19 (

    id BIGSERIAL PRIMARY KEY,

    source_file TEXT,

    financial_year TEXT,
    industry TEXT,
    industry_code TEXT,
    quartile_label TEXT,
    financial_benchmark TEXT,
    value_type TEXT,

    value NUMERIC,
    value_unit TEXT,
    value_label TEXT,
    null_reason TEXT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT *
FROM bronze.figure_schema_19
LIMIT 1;


SELECT COUNT(*)
FROM bronze.figure_schema_19;


SELECT COUNT(DISTINCT source_file)
FROM bronze.figure_schema_19;

SELECT pg_size_pretty(
    pg_total_relation_size(
        'bronze.figure_schema_19'
    )
);











