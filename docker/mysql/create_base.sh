#!/usr/bin/env bash

password=$(cat /var/log/mysql/error.log | grep "A temporary password is generated for" | tail -1 | sed -n 's/.*root@localhost: //p')

MYPASSWD=$password
#mysqladmin -u root password $MYPASSWD;
#mysql -uroot -p$password -Bse "ALTER USER 'root'@'localhost' IDENTIFIED BY '$MYPASSWD';"

mysql -uroot -p$MYPASSWD -e "CREATE DATABASE IF NOT EXISTS domain_statistic DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -uroot -p$MYPASSWD -e "CREATE USER 'pma'@'%' IDENTIFIED BY 'pma';"
mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'pma'@'%';"
mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'pma'@'localhost';"
mysql -uroot -p$MYPASSWD -e "CREATE USER 'domain_statistic'@'%' IDENTIFIED BY 'domain_statistic';"
mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'domain_statistic'@'%';"
mysql -uroot -p$MYPASSWD -e "GRANT ALL PRIVILEGES ON * . * TO 'domain_statistic'@'localhost';"
mysql -uroot -p$MYPASSWD -e "FLUSH PRIVILEGES;"
sleep 5
mysql -uroot -p$MYPASSWD domain_statistic < /root/structure.sql
touch /root/.my.cnf;
echo "[client]" > /root/.my.cnf 
echo "password=$MYPASSWD" >> /root/.my.cnf

echo "Done"