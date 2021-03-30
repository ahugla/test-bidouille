


# sur CentOS 7 showroom
# DB test : 10.11.10.32   vra-002510



# recup du repo git
cd /tmp/
git clone https://github.com/ympondaven/POCNDC.git



# install MySLQ
yum install -y  mariadb-server
systemctl start mariadb
systemctl enable mariadb


# set password
mysql -e "UPDATE mysql.user SET Password = PASSWORD('changeme') WHERE User = 'root'"
systemctl restart mariadb

#mysql -u root -p
#MariaDB [(none)]> SHOW DATABASES;
#+--------------------+
#| Database           |
#+--------------------+
#| information_schema |
#| mysql              |
#| performance_schema |
#| test               |
#+--------------------+
#4 rows in set (0.00 sec)



# creation du fichier de compte
cat >/var/lib/mysql/extra <<EOF
[client]
user=root
password=changeme
EOF



# create base et populate
mysql  --defaults-extra-file=/var/lib/mysql/extra  < /tmp/POCNDC/sources/dump_testndc.sql
#mysql -u root -p
#USE testndc;
#SHOW TABLES;
#select * from contenu_base_testndc;

