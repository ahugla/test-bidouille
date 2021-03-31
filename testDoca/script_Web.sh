

# sur CentOS 7 showroom
# URL :  http://IP/poc.php




# Recuperation des variables
DB_IP=$1
DB_password=$2
minIO_IP=$3
echo "DB_IP = " $DB_IP
echo "DB_password = " $DB_password
echo "minIO_IP = " $minIO_IP




# installs additionnelles dont php 7.3
yum install -y epel-release yum-utils vim unzip wget git httpd mysql php-mysql
yum install -y http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager --enable remi-php73
yum install -y php php-common php-opcache php-mcrypt php-cli php-gd php-curl php-mysqlnd php-simplexml php-mbstring



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
sed -i -e "s/$password = 'mon_password';/$password = '"$DB_password"';/g"  /var/www/html/poc.php




#Install aws-sdk-php V3 par zip :
mkdir /var/www/html/aws
cd /var/www/html/aws
wget https://docs.aws.amazon.com/aws-sdk-php/v3/download/aws.zip        # AWS SDK for PHP - Version 3
unzip aws.zip



############################TO DO  DEBUT ##################################

# en tout debut de php
date_default_timezone_set('Europe/Paris');

# ajouter dans php:
 'endpoint' => 'http://10.11.10.33:9000',
  credential
  bucket
  fichier
############################TO DO  FIN   ##################################



# redemarrage des services
systemctl restart httpd
systemctl enable httpd