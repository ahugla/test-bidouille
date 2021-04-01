

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



# recup du repo git et install web php 
#cd /tmp/
#git clone https://github.com/ympondaven/POCNDC.git
#cp /tmp/POCNDC/sources/poc.php  /var/www/html/poc.php


# recup du repo git et install web php 
cd /tmp
git clone https://github.com/ahugla/test-bidouille.git
cp /tmp/test-bidouille/testDoca/poc.php  /var/www/html/poc.php



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


#UTILISER LE FICHIER poc.php du template ou sur git alex
# Remplacer 'ma_secret_key_API' et 'MINIO_IP' par leur valeur
sed -i -e 's/ma_secret_key_API/'"$DB_password"'/g'  /var/wwww/html/poc.php
sed -i -e 's/MINIO_IP/'"$minIO_IP"'/g'  /var/wwww/html/poc.php



# redemarrage des services
systemctl restart httpd
systemctl enable httpd




#EXEMPLE OK
#echo "<p>\n";
#require 'aws/aws-autoloader.php';
#use Aws\S3\S3Client;
#
#    $bucket = 'truc';
#    $fichier = 'test.txt';
    #$clef_API = 'minioadmin';
    #$secret_API = 'changeme';
#
#try {
    #$s3 = new S3Client([
        #'region' => 'eu-west-3',
        #'version' => '2006-03-01',
        #'endpoint' => 'http://10.11.10.33:9000',
        #'credentials' => [
            #'key'    => $clef_API ,
            #'secret' => $secret_API ,
        #],
    #]);
    #$contenu = $s3->getObject(array(
        #'Bucket' => $bucket,
#


