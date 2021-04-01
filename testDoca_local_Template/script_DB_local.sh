
# sur CentOS 7 




# Recuperation des variables
DB_password=$1
echo "DB_password = " $DB_password


cd /tmp/


# install MySLQ
systemctl start mariadb
systemctl enable mariadb


# Allow remote connections
/etc/mysql/mysql.conf.d/mysqld.cnf


# set password
mysql -e "UPDATE mysql.user SET Password = PASSWORD('$DB_password') WHERE User = 'root'"
systemctl restart mariadb



# creation du fichier de compte
cat >/var/lib/mysql/extra <<EOF
[client]
user=root
password=$DB_password
EOF


# create base et populate
mysql  --defaults-extra-file=/var/lib/mysql/extra  < /tmp/sources/dump_testndc.sql


# create user testndcuser and enable remote connection
sed -i '2 i\bind-address = 0.0.0.0' /etc/my.cnf
mysql --defaults-extra-file=/var/lib/mysql/extra -e "CREATE USER 'testndcuser'@'%' IDENTIFIED BY '$DB_password';"
mysql --defaults-extra-file=/var/lib/mysql/extra -e "GRANT ALL PRIVILEGES ON testndc.* TO 'testndcuser'@'%';"
mysql --defaults-extra-file=/var/lib/mysql/extra -e "FLUSH PRIVILEGES;"



systemctl restart mariadb


