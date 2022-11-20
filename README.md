# Sife

## what is sife?
sife is a password manager

prerequisites:
python3
sqlite3 or mysql insallation

## Database:
Note: Only for mysql
Make a database named passwords with a table named passwords
In that table should be three rows- website, password, username
set the character limit according to your preference

put the username and password in the UsernamePassword.json file in data directory

## Installation:
### Windows:
clone the repo
do the above steps for database
install the following pip packages:
dropbox, termcolor, sqlite3 or mysql-connector or both, pyperclip, openpyexcel, random2

### Linux:
run the install.sh script as root

## Cloud
note: This is optional

You can create a backup file of your passwords and upload it to dropbox

run: ```sife connect```

