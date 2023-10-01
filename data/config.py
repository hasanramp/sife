import json
class Configuration:
    def __init__(self,record_changes,make_change_logs,db_engine,config_file):
        self.record_changes = record_changes
        self.make_change_logs = make_change_logs
        self.db_engine = db_engine
        self.config_file = config_file

    def writeSifeConfiguration(self,record_changes,make_change_logs,db_engine,config_file):

        try:
            
            if(record_changes == 'False'):
                record_changes = ''
            
            if(make_change_logs == 'False'):
                make_change_logs = ''
            
            json_data =  {
                        "record_changes": bool(record_changes),
                        "make_change_logs": bool(make_change_logs),
                        "db_engine": db_engine }

            # Writing JSON config file sif_configuration.json
            with open(config_file, "w") as outfile:
                json.dump(json_data, outfile)
        except FileNotFoundError as fnf:
            print("Configuration file sif_configuration.json not found!")