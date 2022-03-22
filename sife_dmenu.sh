function=$(cat ~/sife_dmenu/functions | dmenu) 
LANG="en_IN.UTF-8"  

cd /usr/share/sife
if [[ $function == "find-password" ]] 
then
	website=$(echo "" | dmenu -p "enter website: ")
	username=$(echo "" | dmenu -p "enter username: ")
	set SUDO_ASKPASS = ~/sife_dmenu/myaskpass.sh
	sudo -A python3 sife_dmenu.py fn-pwd $website $username
elif [[ $function == "enter-password" ]]
then
	website=$(echo "" | dmenu -p "enter website: ")
	password=$(echo "" | dmenu -p "enter password: ")
	username=$(echo "" | dmenu -p "enter username: ")
	sudo -A python3 sife_dmenu.py en-pwd $website $password $username
elif [[ $function == "delete" ]]
then
	website=$(echo "" | dmenu -p "enter website: ")
	username=$(echo "" | dmenu -p "enter username: ")
	sudo -A python3 sife_dmenu.py delete $website $username
elif [[ $function == "show" ]]
then
	sudo -A python3 sife_dmenu.py show
elif [[ $function == "set-db-engine" ]]
then
	db_engine=$(printf "mysql \nsqlite3" | dmenu -p "enter db engine: ")
	sudo -A python3 sife_dmenu.py set-db-engine $db_engine
elif [[ $function == "backup" ]]
then
	task=$(printf "create \nload" | dmenu -p "enter task: ")
	format=$(printf "hdn \nxlsx" | dmenu -p "enter format: ")
	cloud=$(printf "true \nfalse" | dmenu -p "upload to cloud?: ")
	cmp=$(printf "gz \nzip \n None" | dmenu -p "compress?")
	if [[ $cmp == "None" ]]
	then
		$cmp = ""
	fi
	sudo -A python3 sife_dmenu.py backup -cloud $cloud -cmp $cmp $task $format

fi
