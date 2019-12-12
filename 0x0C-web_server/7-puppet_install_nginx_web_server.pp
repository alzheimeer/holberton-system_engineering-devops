#!/usr/bin/env bash
#Install nginx

exec {'/usr/bin/env apt-get -y update': }
exec {'/usr/bin/env apt-get -y install nginx': }
exec {'/usr/bin/env echo "Holberton School" > /var/www/html/index.nginx-debian.html': }
exec {'/usr/bin/env sed -i "/server_name _;/ a\\\trewrite ^/redirect_me https://www.youtube.com/ permanent;" /etc/nginx/sites-available/default': }
exec {'/usr/bin/env service nginx start': }
