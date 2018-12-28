# database.py
# Defines an interface which can be used to interact with the Code Create database
# Written by Nathan Lam (nathan@codecreate.com.au)
# Started on 25th December, 2018

import json, os, psycopg2, csv, logging, traceback, time


# Code Create Database Details
#
# Contacts - given name, surname, preferred name, email, phone_no1, phone_no2
# Students - grade, age, parents and emergency contact details
# Teachers - start_day, DoB, WWCC, WWCC expiry date, bank account details (BSB, account number)
# Institutions - stores information about the name, location, admin contact, IT contact, supervising teacher
# Locations - stores the room name, school associated, and capacity
# Roster - stores information about the teacher and the classes they teach
# Classes - stores information about the first date, last date, day of week, school, start time, duration, classroom and course
# Enrolments - stores information about the students enrolled in classes
# Courses - stores information about the topic, resource location, type of resource (project, notes, outline)
# Course History - stores the teacher, course and date of contribution
# Absences - date, student_id and class_id
# Breaks - date, class_id


# CONSTANTS
#
# Define constants describing the database structure and constraints

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
            'abn',
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
            'class_id'],
        'absences': [
            'absence_date',
            'enrolment_id'],
        'breaks': [
            'break_date',
            'class_id'],
        'roster': [
            'teacher_id',
            'class_id',
            'status']}

NOT_NULL_FIELDS = {
        'contacts': [
            'given_names',
            'surname',
            'preferred_name'],
        'students': [],
        'teachers': [
            'start_day',
            'dob',
            'wwcc',
            'wwcc_expiry'],
        'courses': [
            'topic',
            'resource_type'],
        'course_history': [
            'teacher_id',
            'course_id',
            'commit_date'],
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
            'institution_id'],
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
            'class_id'],
        'absences': [
            'absence_date',
            'enrolment_id'],
        'breaks': [
            'break_date',
            'class_id'],
        'roster': [
            'teacher_id',
            'class_id',
            'status']}

RESOURCE_TYPES = [
        'project',
        'notes',
        'outline']

STATUS_TYPES = [
        'available',
        'tentative',
        'accepted']


def main():
    # Initialise log file
    dirname = os.path.dirname(os.path.abspath(__file__))
    log_name = 'cc_db' + time.strftime('%Y%m%d-%H%M%S') + '.log'
    filename = os.path.join(dirname, '..', 'logs', log_name)
    logging.basicConfig(filename=filename, level=logging.DEBUG)

    # Begin basic tests
    logging.info('Executing basic tests...')
    basic_tests()


def basic_tests():
    # Establish connection with Postgres database server
    conn = connect2db()
    init(conn)

    # Define test records for inputs
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

def close_db(conn):
    conn.close()


def init(conn):
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, '..', 'sql', 'views', 'check_tables_exist.sql')
    with open(filename, 'r') as fp:
        cur = conn.cursor()
        sql_cmd = fp.read().replace('<table_names>', ', '.join(f'\'{name}\'' for name in TABLE_FIELDS.keys()))
        logging.info('Executing SQL query:\n' + sql_cmd)
        cur.execute(sql_cmd)
        results = cur.fetchall()
        existing_tables = []
        for row in results:
            existing_tables.append(row[0])
        cur.close()
    for table in TABLE_FIELDS.keys():
        logging.debug('Checking if ' + table + ' is an existing table')
        check_for_table(conn, existing_tables, table)


def check_for_table(conn, tables, table_name):
    dirname = os.path.dirname(os.path.abspath(__file__))
    if table_name not in tables:
        cur = conn.cursor()
        filename = os.path.join(dirname, '..', 'sql', 'create_table', table_name + '.sql')
        with open(filename, 'r') as sql_cmd:
            cur.execute(sql_cmd.read())
        cur.close()
    conn.commit()


def get_insert_query(table, details):
    if type(details) is not dict:
        logging.error('Invalid Parameter: details must be of type dict')
        return
    if table not in TABLE_FIELDS.keys():
        logging.error('Invalid Parameter: table must be one of the following -> '
                + str(TABLES_FIELDS.keys()))
    query = 'INSERT INTO ' + table + ' ('
    is_first = True
    for field in details.keys():
        if is_first:
            is_first = False
        else:
            query += ', '
        query += field
    query += ') VALUES ('
    #is_first = True
    values = []
    for value in details.values():
        #if is_first:
        #    is_first = False
        #else:
        #    query += ', '
        if type(value) is str:
            #query = query + '\'' + str(value) + '\''
            values.append('\'' + str(value) + '\'')
        else:
            values.append(str(value))
        #else:
        #query += str(value)
    query += ', '.join(values)
    query += ');'
    return query


def is_valid_record(table_name, details):
    if type(details) is not dict:
        logging.error('Invalid Parameter: contact_details must be of type dict')
        return False
    if type(table_name) is not str:
        logging.error('Invalid Parameter: Table name must be a string')
        return False
    if table_name not in TABLE_FIELDS.keys():
        logging.error('Invalid Parameter: table_name does not exist in this database')
        return False
    valid_fields = 0
    table_fields = []
    for field in TABLE_FIELDS[table_name]:
        table_fields.append(field)
    if table_name in ['students', 'teachers']:
        for field in TABLE_FIELDS['contacts']:
            table_fields.append(field)
    for field in table_fields:
        if field in details:
            valid_fields += 1
        elif table_name == 'contacts' and field == 'preferred_name':
            logging.info('Assigning first given name to preferred name')
            contact_fields['preferred_name'] = contact_fields['given_names'].split(' ', 1)[0]
            valid_fields += 1
        elif (table_name == 'courses'
                and field == 'resource_type'
                and details[field] not in RESOURCE_TYPES):
            logging.error('Invalid Parameter: resource_type must be one of the following -> ' + str(RESOURCE_TYPES))
            return False
        elif (table_name == 'roster'
                and field == 'status'
                and details[field] not in STATUS_TYPES):
            logging.error('Invalid Parameter: resource_type must be one of the following -> ' + str(STATUS_TYPES))
            return False
        elif (table_name == 'locations'
                and field == 'capacity'
                and field < 0):
            logging.error('Invalid Parameter: capacity must be greater than or equal to 0')
            return False
        elif field in NOT_NULL_FIELDS[table_name]:
            logging.error('Invalid Parameter: Missing ' + field + ' field')
            return False
    if valid_fields != len(details):
        logging.error('Invalid Parameter: Field(s) which are not valid fields for ' + table_name)
        logging.error('\tFound ' + str(valid_fields) + ' valid fields, record has ' + str(len(details)))
        return False
    return True


def insert_record(conn, table_name, details):
    if not is_valid_record(table_name, details):
        return False
    query = get_insert_query(table_name, details)
    logging.info('Inserting new record in ' + table_name + '...')
    logging.debug('Insert Query: ' + query)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except Exception:
        logging.error('Unable to execute SQL query:\n\t' + traceback.format_exc())
    cur.close()
    conn.commit()
    return True


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
