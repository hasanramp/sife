import sys
from config import Configuration

def main():
   
    cnf_file = 'data/sif_configuration.json'

    print("Record changes (true/false) ?")
    record_change = input()
    
    if(not 'True' in record_change.capitalize() and not 'False' in record_change.capitalize()):
        print('RECORD_CHANGE specified not valid!')
        sys.exit(-1)

    print("Make change logs (true/false) ?")
    make_change_logs = input()
    
    if(not 'True' in make_change_logs.capitalize() and not 'False' in make_change_logs.capitalize()):
        print('MAKE_CHANGE_LOGS specified not valid!')
        sys.exit(-1)

    print("Which type of engine do you want to use (sqlite3/mysql) ?")
    set_engine = input()

    if('mysql' not in set_engine and 'sqlite3' not in set_engine):
        print('ENGINE specified not valid!')
        sys.exit(-1)

    print("Configuration file ?")
    cnf_file = input()     

    if(cnf_file == ''):
        print('CONFIG FILE specified not valid!')
        sys.exit(-1)

    conf = Configuration(record_change,make_change_logs,set_engine,cnf_file)
    conf.writeSifeConfiguration(record_change.capitalize(),make_change_logs.capitalize(),set_engine,cnf_file)


if __name__ == "__main__":
    main()

