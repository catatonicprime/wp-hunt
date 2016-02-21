# wp-hunt
bug hunting in wordpress (plugins)

# Install
install RIPS PHP scanner into /var/www/html/rips-0.55/
install wordpress into /var/www/html/wordpress

service apache2 start

Perform a bulk audit:
python wp_search.py -s https://wordpress.org/plugins/browse/popular/page/27/  -l 0 -d /var/www/html/wordpress/wp-content/plugins/
