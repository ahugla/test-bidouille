

# sur CentOS 7 showroom
# WEB test : 10.11.10.36   vra-002512
# URL :  http://10.11.10.36/poc.php






# Recuperation des variables
DB_IP = $1
echo "DB_IP = " $DB_IP



# installs additionnelles dont php
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
yum --enablerepo=remi,remi-php72 install -y httpd php php-common


# recup du repo git
cd /tmp/
git clone https://github.com/ympondaven/POCNDC.git



#install web php 
cp /tmp/POCNDC/sources/poc.php  /var/www/html/poc.php



#update  /etc/httpd/conf/httpd.conf
############################################# TO DO ############################################# 
# COPY MANUELLE A LA FIN


# Il faudra modifier le poc.php aux endroits indiqués pour MySql et S3
############################################# TO DO ############################################# 







# redemarrage des services
systemctl restart httpd
systemctl enable httpd