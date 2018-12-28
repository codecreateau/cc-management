CREATE TABLE breaks (
    id          SERIAL      PRIMARY KEY,
    break_date  DATE        NOT NULL,
    class_id    INTEGER     REFERENCES classes(id)
);

