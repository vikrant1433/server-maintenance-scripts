#!/bin/bash - 
#===============================================================================
#
#          FILE: notify.sh
# 
#         USAGE: ./notify.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Vikrant (), vikrant@cse.iitb.ac.in
#  ORGANIZATION: 
#       CREATED: Tuesday 27 September 2016 01:06
#      REVISION:  ---
#===============================================================================

source /home/vikrant/.py_envs/server_maintenance/bin/activate
python /home/vikrant/server-maintenance/main.py >> /home/vikrant/server-maintenance/logs &
