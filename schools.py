import json, os, psycopg2, csv, logging, traceback, time

TABLES = [
        'contacts',
        'students',
        'teachers',
        'courses',
        'course_history',
        'institutions',
        'locations',
        'classes',
        'enrolments']

TABLE_FIELDS = {
        'contacts': [
            'given_names',
            'surname',
            'preferred_name',
            'email',
            'phone_no1',
            'phone_no2'],
        'students': [
            'grade',
            'age',
            'parent1_id',
            'parent2_id',
            'ec_id'],
        'teachers': [
            'start_day',
            'dob',
            'wwcc',
            'wwcc_expiry',
            'bsb',
            'acc_no'],
        'courses': [
            'topic',
            'description',
            'resource_link',
            'resource_type'],
        'course_history': [
            'teacher_id',
            'course_id',
            'commit_date',
            'commit_msg'],
        'institutions': [
            'name',
            'street_address',
            'city',
            'state',
            'postcode',
            'admin_id',
            'it_contact_id',
            'supervisor_id'],
        'locations': [
            'name',
            'institution_id',
            'capacity'],
        'classes': [
            'first_date',
            'last_date',
            'day_of_week',
            'location_id',
            'start_time',
            'duration',
            'course_id'],
        'enrolments': [
            'student_id',
            'class_id']}


def main():
    log_name = 'schools' + time.strftime('%Y%m%d-%H%M%S') + '.log'
    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    logging.info('Executing basic tests...')
    basic_tests()

def basic_tests():
    conn = connect2db()
    init(conn)
    new_contact_1 = {
            'given_names': 'Jonathan',
            'surname': 'Smith',
            'preferred_name': 'Johnny',
            'email': 'johnny.smith@me.com',
            'phone_no1': '+614200000000'}
    new_contact_2 = {
            'given_names': 'Lucy',
            'surname': 'Jones',
            'preferred_name': 'Lu',
            'email': 'lucy.jones@jmail.com',
            'phone_no1': '+614204200000'}
    new_student = {
            'given_names': 'Jackie',
            'surname': 'Lee',
            'preferred_name': 'Jay',
            'email': 'jackie.lee@abc.com',
            'phone_no1': '+614242000000',
            'grade': 5,
            'age': 11,
            'parent1_id': 1}
    new_teacher = {
            'given_names': 'Tony',
            'surname': 'Stark',
            'preferred_name': 'Iron Man',
            'email': 'tony.stank@marvel.com',
            'start_day': '2008-05-01',
            'dob': '1970-05-29',
            'wwcc': 'WWC01234567E',
            'wwcc_expiry': '2018-04-23'}
    insert_record(conn, 'contacts', new_contact_1)
    insert_record(conn, 'contacts', new_contact_2)
    insert_record(conn, 'students', new_student)
    insert_record(conn, 'teachers', new_teacher)
    conn.close()


def connect2db():
    DATABASE_URL = os.environ['DATABASE_URL']
    logging.info('Connecting to ' + DATABASE_URL)
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='allow')
    except:
        logging.critical('Unable to connect to database: ' + DATABASE_URL)
        exit()
    return conn

def init(conn):
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, 'sql', 'check_tables_exist.sql')
    with open(filename, 'r') as sql_cmd:
        cur = conn.cursor()
        cur.execute(sql_cmd.read())
        results = cur.fetchall()
        existing_tables = []
        for row in results:
            existing_tables.append(row[0])
        cur.close()
    for table in TABLE_FIELDS.keys():
        check_for_table(conn, existing_tables, table)

def check_for_table(conn, tables, table_name):
    dirname = os.path.dirname(os.path.abspath(__file__))
    if table_name not in tables:
        cur = conn.cursor()
        filename = os.path.join(dirname, 'sql', 'create_' + table_name +'_tbl.sql')
        with open(filename, 'r') as sql_cmd:
            cur.execute(sql_cmd.read())
        cur.close()
    conn.commit()

def get_insert_query(table, details):
    if type(details) is not dict:
        logging.error('Invalid Parameter: details must be of type dict')
        return
    if table not in TABLES:
        logging.error('Invalid Parameter: table must be one of the following -> '
                + str(TABLES))
    query = 'INSERT INTO ' + table + ' ('
    is_first = True
    for field in details.keys():
        if is_first:
            is_first = False
        else:
            query += ', '
        query += field
    query += ') VALUES ('
    is_first = True
    for value in details.values():
        if is_first:
            is_first = False
        else:
            query += ', '
        if type(value) is str:
            query = query + '\'' + str(value) + '\''
        else:
            query += str(value)
    query += ');'
    return query


def is_valid_contact(contact_details):
    if type(contact_details) is not dict:
        logging.error('Invalid Parameter: contact_details must be of type dict')
        return False
    valid_fields = 0
    for field in TABLE_FIELDS['contacts']:
        if field in contact_details:
            valid_fields += 1
        elif field in ['given_names', 'surname']:
            logging.error('Invalid Parameter: Missing ' + field + ' field')
            return False
        elif field == 'preferred_name':
            logging.info('Assigning first given name to preferred name')
            contact_fields['preferred_name'] = contact_fields['given_names'].split(' ', 1)[0]
    if valid_fields != contact_details.len():
        logging.error('Invalid Parameter: Field(s) which are not valid fields for contacts')
        return False
    return True

def is_valid_student(student_details):
    if not is_valid_contact(student_details):
        return False
    valid_fields = 0
    for field in TABLE_FIELDS['students']:
        if field in student_details:
            valid_fields += 1
    if valid_fields != student_details.len():
        logging.error('Invalid Parameter: Field(s) which are not valid fields for students')
        return False
    return True

def is_valid_teacher(teacher_details):
    if not is_valid_contact(teacher_details):
        return False
    valid_fields = 0
    for field in TABLE_FIELDS['teachers']:
        if field in teachers_details:
            valid_fields += 1
        elif field in ['start_day', 'dob', 'wwcc', 'wwcc_expiry']:
            logging.error('Invalid Parameter: Missing ' + field + ' field')
            return False
    if valid_fields != teachers_details.len():
        logging.error('Invalid Parameter: Field(s) which are not valid fields for teachers')
        return False
    return True


def insert_record(conn, table_name, contact_details):
    if type(table_name) is not str:
        logging.error('Invalid Parameter: Table name must be a string')
    if table_name == 'contact':
        if not is_valid_contact(contact_details):
            return False
    query = get_insert_query(table_name, contact_details)
    logging.info('Inserting new record in ' + table_name + '...')
    logging.debug('Insert Query: ' + query)
    try:
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit()
    except Exception:
        logging.error('Unable to execute SQL query: ' + traceback.format_exc())
    return True

# Contacts - given name, surname, preferred name, email, phone_no1, phone_no2

# Institutions - stores information about the name, location, admin contact, IT contact, supervising teacher

# Locations - stores the room name, school associated,

# Roster - stores information about the teacher and the classes they teach

# Classes - stores information about the first date, last date, day of week, school, start time, duration, classroom and course

# Enrolments - stores information about the students enrolled in classes

# Courses - stores information about the topic, resource location, type of resource (project, notes, outline)

# Course History - stores the teacher, course and date of contribution

# Student Feedback

# Teacher Feedback


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
