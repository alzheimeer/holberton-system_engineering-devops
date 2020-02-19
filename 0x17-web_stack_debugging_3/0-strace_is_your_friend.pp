# error php conf, a row says phpp and it must be php use sed -i to change this
exec { 'change ext error':
  command => '/bin/sed -i "s/phpp/php/g" /var/www/html/wp-settings.php':
}
exec { 'restart server':
  command => 'sudo service apache2 restart'
}