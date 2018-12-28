CREATE TABLE enrolments (
    id          SERIAL  PRIMARY KEY,
    student_id  INTEGER REFERENCES students(id),
    class_id    INTEGER REFERENCES classes(id)
);
