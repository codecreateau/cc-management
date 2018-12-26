CREATE TABLE INSTITUTIONS (
    id              SERIAL          PRIMARY KEY,
    name            VARCHAR(128)    UNIQUE,
    street_address  VARCHAR(128)    NOT NULL,
    city            VARCHAR(64)     NOT NULL,
    state           VARCHAR(64)     NOT NULL,
    postcode        SMALLINT        NOT NULL,
    admin_id        INTEGER         REFERENCES contacts(id),
    it_contact_id   INTEGER         REFERENCES contacts(id),
    supervisor_id   INTEGER         REFERENCES contacts(id)
);

