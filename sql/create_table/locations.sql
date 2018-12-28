CREATE TABLE locations (
    id              SERIAL      PRIMARY KEY,
    name            VARCHAR(64) NOT NULL,
    institution_id  INTEGER     REFERENCES institutions(id),
    capacity        SMALLINT    CHECK (capacity > 0)
);

