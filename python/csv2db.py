# csv2db.py
# CSV reader which inputs rows as records in the Code Create database
# Written by Nathan Lam (nathan@codecreate.com.au)
# Started on 27th December, 2018
import csv, cc_db, logging, os, sys, time

def main():
    if len(sys.argv) != 3:
        print('Missing Arguments: program must be run using `python <csv_file> <table_name>`')
    dirname = os.path.dirname(os.path.abspath(__file__))
    log_name = 'csv2db' + time.strftime('%Y%m%d-%H%M%S') + '.log'
    filename = os.path.join(dirname, '..', 'logs', log_name)
    logging.basicConfig(filename=filename, level=logging.DEBUG)
    read(sys.argv[1], sys.argv[2])

def read(file_name, table_name):
    conn = cc_db.connect2db()
    cc_db.init(conn)
    details = {}
    path = os.getcwd()
    filename = os.path.join(path, file_name)
    with open(filename, 'r') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            record = dict(row)
            logging.info('Inserting', record)
            cc_db.insert_record(conn, table_name, record)
    cc_db.close_db(conn)

if __name__ == '__main__':
    main()
