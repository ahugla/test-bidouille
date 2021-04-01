

cd /tmp



# install packages
yum update -y
yum install -y git wget vim mariadb-server unzip
yum install -y epel-release yum-utils vim unzip wget git httpd mysql php-mysql
yum install -y http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager --enable remi-php73
yum install -y php php-common php-opcache php-mcrypt php-cli php-gd php-curl php-mysqlnd php-simplexml php-mbstring


# download files
mkdir /tmp/sources
wget https://dl.minio.io/server/minio/release/linux-amd64/minio -O /tmp/sources/minio
wget https://raw.githubusercontent.com/ahugla/test-bidouille/master/testDoca/stockage_objet_NDC.txt -O /tmp/sources/stockage_objet_NDC.txt
wget https://raw.githubusercontent.com/ahugla/test-bidouille/master/testDoca/dump_testndc.sql -O /tmp/sources/dump_testndc.sql
wget https://raw.githubusercontent.com/ahugla/test-bidouille/master/testDoca/poc.php -O /tmp/sources/poc.php
wget https://docs.aws.amazon.com/aws-sdk-php/v3/download/aws.zip -O /tmp/sources/aws.zip




#  RESTE A :
#   -  AJUSTER LES SCRIPTS
#   -  COPIER LES SCRIPTS EN LOCAL




