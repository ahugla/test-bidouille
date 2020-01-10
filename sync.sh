# On recupere la difference depuis Github
echo "  ---> GIT PULL ..."
cd /tmp/test-bidouille
git pull



# Copy dans le repertoire web
echo "  ---> COPY TO HTML DIRECTORY ET DROITS ..."
cd /var/www/html
rm -rf *
cp -R  /tmp/test-bidouille/* /var/www/html/
# creation du fichier de log
touch /var/www/html/script1.log
# rendre les fichiers executables
chmod 777 /var/www/html/*.py
chmod 777 /var/www/html/script1.log



# redemarrage du service apache
echo "  ---> RESTART WEB SERVER ..."
systemctl stop httpd
systemctl start httpd


echo "  ---> SYNC COMPLETED !"
