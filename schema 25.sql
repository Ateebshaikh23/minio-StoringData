



ALTER USER postgres WITH PASSWORD 'postgres';


SELECT COUNT(*)
FROM bronze.file_catalog;


SELECT
    file_extension,
    COUNT(*) AS total_files
FROM bronze.file_catalog
GROUP BY file_extension
ORDER BY total_files DESC;


SELECT
    source_folder,
    COUNT(*) AS total_files
FROM bronze.file_catalog
GROUP BY source_folder
ORDER BY total_files DESC;


SELECT
    source_folder,
    COUNT(*) AS csv_files
FROM bronze.file_catalog
WHERE file_extension = 'csv'
GROUP BY source_folder
ORDER BY csv_files DESC;

SELECT
    source_folder,
    COUNT(*) AS excel_files
FROM bronze.file_catalog
WHERE file_extension IN ('xlsx','xls','xlsb')
GROUP BY source_folder
ORDER BY excel_files DESC;

SELECT *
FROM bronze.file_catalog
WHERE source_folder = 'Figure.nz data'
LIMIT 20;


SELECT *
FROM bronze.file_catalog
WHERE source_folder = 'School data'
LIMIT 20;


CREATE TABLE bronze.raw_files (
    id SERIAL PRIMARY KEY,
    file_catalog_id INT,
    source_folder TEXT,
    file_name TEXT,
    minio_path TEXT,
    raw_content JSONB,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bronze.schema_registry (
    schema_id SERIAL PRIMARY KEY,
    schema_name TEXT,
    column_list JSONB,
    file_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bronze.figure_schema_25 (
    id SERIAL PRIMARY KEY,
    source_file TEXT,

    year_ended_june TEXT,
    local_authority TEXT,
    local_authority_code TEXT,
    activity TEXT,
    income_expenditure_item TEXT,

    value NUMERIC,
    value_unit TEXT,
    value_label TEXT,

    null_reason TEXT,
    metadata_1 TEXT,
    metadata_2 TEXT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT COUNT(*)
FROM bronze.figure_schema_25;


SELECT *
FROM bronze.figure_schema_25
LIMIT 10;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'bronze'
AND table_name = 'figure_schema_25';

TRUNCATE TABLE bronze.figure_schema_25;



-- Row count should be 66,336,048
SELECT COUNT(*) FROM bronze.figure_schema_25;

SELECT COUNT(*)
FROM bronze.figure_schema_25;

SELECT COUNT(DISTINCT source_file)
FROM bronze.figure_schema_25;

SELECT
    pg_size_pretty(
        pg_total_relation_size(
            'bronze.figure_schema_25'
        )
    );

