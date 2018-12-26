CREATE TABLE contacts (
    id              SERIAL      PRIMARY KEY,
    given_names     VARCHAR(64) NOT NULL,
    surname         VARCHAR(64) NOT NULL,
    preferred_name  VARCHAR(64) NOT NULL,
    email           VARCHAR(64),
    phone_no1       VARCHAR(64),
    phone_no2       VARCHAR(64)
);

