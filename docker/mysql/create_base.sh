#!/usr/bin/env bash

#password=$(cat /var/log/mysql/error.log | grep "A temporary password is generated for" | tail -1 | sed -n 's/.*root@localhost: //p')
#MYPASSWD=$password
#mysql -uroot -p$password -Bse "ALTER USER 'root'@'localhost' IDENTIFIED BY '$MYPASSWD';"

#MYPASSWD=$RANDOM$RANDOM$RANDOM

#mysqladmin -u root password $MYPASSWD;

mysql -uroot -p$$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS clo_statistic DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -uroot -p$$MYSQL_ROOT_PASSWORD -e "CREATE USER 'clo_statistic'@'%' IDENTIFIED WITH mysql_native_password BY 'clo_statistic';"
mysql -uroot -p$$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON * . * TO 'clo_statistic'@'%';"
mysql -uroot -p$$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON * . * TO 'clo_statistic'@'localhost';"
mysql -uroot -p$$MYSQL_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"

#mysql -uroot -p$MYPASSWD -e "CREATE DATABASE IF NOT EXISTS clo_statistic DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
#mysql -uroot -p$MYPASSWD -e "CREATE USER 'clo_statistic'@'%' IDENTIFIED WITH mysql_native_password BY 'clo_statistic';"
#mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'clo_statistic'@'%';"
#mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'clo_statistic'@'localhost';"
#mysql -uroot -p$MYPASSWD -e "FLUSH PRIVILEGES;"
#sleep 5
#mysql -uroot -p$MYPASSWD domain_statistic < /root/structure.sql
#touch /root/.my.cnf;
#echo "[client]" > /root/.my.cnf
#echo "password=$MYPASSWD" >> /root/.my.cnf

echo "Done"