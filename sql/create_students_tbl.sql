CREATE TABLE students (
    --id              SERIAL,     PRIMARY KEY,
    grade           SMALLINT,
    age             SMALLINT,
    parent1_id      INTEGER     REFERENCES contacts(id),
    parent2_id      INTEGER     REFERENCES contacts(id),
    ec_id           INTEGER     REFERENCES contacts(id),
    PRIMARY KEY(id)
) INHERITS (contacts);

