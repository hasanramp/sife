from hdn import Parser

parser = Parser('backup.hdn')
parser.replace_value('#none', 'NULL')