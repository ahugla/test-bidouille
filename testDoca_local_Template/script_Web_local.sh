

# sur CentOS 7 
# URL :  http://IP/poc.php




# Recuperation des variables
DB_IP=$1
DB_password=$2
minIO_IP=$3
echo "DB_IP = " $DB_IP
echo "DB_password = " $DB_password
echo "minIO_IP = " $minIO_IP




# recup du repo git et install web php 
cd /tmp
cp /tmp/sources/poc.php  /var/www/html/poc.php



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
copy /tmp/sources/aws.zip /var/www/html/aws/aws.zip
cd /var/www/html/aws
unzip aws.zip



# set parameters
sed -i -e 's/ma_secret_key_API/'"$DB_password"'/g'  /var/www/html/poc.php
sed -i -e 's/MINIO_IP/'"$minIO_IP"'/g'  /var/www/html/poc.php



# redemarrage des services
systemctl restart httpd
systemctl enable httpd


