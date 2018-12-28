CREATE TABLE course_history (
    id          SERIAL          PRIMARY KEY,
    teacher_id  INTEGER         REFERENCES teachers(id),
    course_id   INTEGER         REFERENCES courses(id),
    commit_date DATE            NOT NULL,
    commit_msg  VARCHAR(1024)
);

