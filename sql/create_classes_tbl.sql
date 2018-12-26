CREATE TABLE classes (
    id          SERIAL      PRIMARY KEY,
    first_date  DATE        NOT NULL,
    last_date   DATE        NOT NULL,
    day_of_week VARCHAR(16) NOT NULL,
    location_id INTEGER     REFERENCES locations(id),
    start_time  TIMETZ      NOT NULL,
    duration    INTEGER     NOT NULL,
    course_id   INTEGER     NOT NULL
);

