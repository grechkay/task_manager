#!/bin/bash

# this function takes 1 argument ("work" or "personal" for example to change the .bash_profile directory of the personal_directory)
# usage: ./switch_to.sh work
# corresponding change in .bash_profile: export personal_directory="work"
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
fi
sed -i .bak 's/export PERSONAL_DIRECTORY=.*/export PERSONAL_DIRECTORY='\"$1\"'/g' ~/.bash_profile
echo "Switched personal directory to: $1"
source deactivate
source ~/.bash_profile
source activate tasky