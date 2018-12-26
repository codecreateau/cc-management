CREATE TABLE teachers (
    --id          SERIAL      PRIMARY KEY
    start_day   DATE        NOT NULL,
    dob         DATE        NOT NULL,
    wwcc        VARCHAR(32) UNIQUE NOT NULL,
    wwcc_expiry DATE        NOT NULL,
    bsb         VARCHAR(8),
    acc_no      VARCHAR(32),
    PRIMARY KEY(id)
) INHERITS (contacts);

