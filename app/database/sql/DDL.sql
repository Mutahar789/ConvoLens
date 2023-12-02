CREATE TYPE mood_change AS ENUM (
    'No change in the mood',
    'Customer left in a better mood',
    'Customer left in a worse mood'
);

CREATE TABLE audios(
    id serial PRIMARY KEY,
    customer_id VARCHAR(32),
    csr_id VARCHAR(32),
    customer_satisfied boolean,
    query_resolved boolean,
    unprofessional_csr boolean,
    call_purpose text,
    user_qoi integer,
    customer_mood_change mood_change,
    transcript text,
    embedding vector(1536),
    audio_path text
);

CREATE INDEX ON audios USING hnsw (embedding vector_ip_ops)  WITH (m = 32, ef_construction = 128);
SET hnsw.ef_search = 64;
