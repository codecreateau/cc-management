CREATE TABLE absences (
    id              SERIAL      PRIMARY KEY,
    absence_date    DATE        NOT NULL,
    enrolment_id    INTEGER     REFERENCES enrolments(id)
);

