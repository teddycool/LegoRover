# This folder is used for html content for a web app to control the user data

# install Apache2 web server
sudo apt-get install apache2 -y
# install php
sudo apt-get install php5 libapache2-mod-php5 -y

#After install of Apache2 and PHP the content of this folder should be put in /var/www/html

#To be able to deploy:
sudo chmod g+w /var/www/html -R
sudo usermod -a -G www-data pi
sudo usermod -a -G root pi  #TODO is this secure