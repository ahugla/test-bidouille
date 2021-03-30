

# sur CentOS 7 showroom
# WEB test : 10.11.10.36   vra-002512
# URL :  http://10.11.10.36/poc.php






# Recuperation des variables
DB_IP=$1
DB_password=$2
echo "DB_IP = " $DB_IP
echo "DB_password = " $DB_password




# installs additionnelles dont php
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install -y httpd php5 mysql php-mysql
#rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
#yum --enablerepo=remi,remi-php72 install -y httpd php php-common php5 mysql php-mysql



# recup du repo git
cd /tmp/
git clone https://github.com/ympondaven/POCNDC.git



#install web php 
cp /tmp/POCNDC/sources/poc.php  /var/www/html/poc.php



#update  /etc/httpd/conf/httpd.conf
# creation du fichier
cat >>/etc/httpd/conf/httpd.conf <<EOF
LoadModule proxy_fcgi_module modules/mod_proxy_fcgi.so
<VirtualHost *:8080>
  DocumentRoot "/app"
  ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://lamp-php-fpm:9000/app/$1
  <Directory "/app">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
    DirectoryIndex index.php
  </Directory>
</VirtualHost>
EOF



# Update de poc.php pour DB
sed -i -e "s/$serveur = 'localhost';/$serveur = '"$DB_IP"';/g"  /var/www/html/poc.php
sed -i -e "s/$user = 'testndcuser';/$user = 'root';/g"  /var/www/html/poc.php
sed -i -e "s/$password = 'mon_password';/$password = '"$DB_password"';/g"  /var/www/html/poc.php



# Update de poc.php pur S3
################################   A FAIRE  ##############################


# redemarrage des services
systemctl restart httpd
systemctl enable httpd