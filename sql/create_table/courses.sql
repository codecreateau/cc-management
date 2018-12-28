CREATE TABLE courses (
    id              SERIAL          PRIMARY KEY,
    topic           VARCHAR(64)     UNIQUE NOT NULL,
    description     VARCHAR(1024),
    resource_link   VARCHAR(256),
    resource_type   VARCHAR(64)     CHECK (resource_type IN ('project', 'notes', 'outline'))
);
