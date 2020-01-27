#  GUIA SSH - MYSQL - REPLICA

# *.SSH

instalar:  sudo apt-get install openssh-server
Generar key ssh:  ssh-keygen  y Enter como 4 veces.
Visualizamos la key: cat .ssh/id_rsa.pub

Esta key la colocamos en el profile de tu usuario en la intranet

Y a los servidores que te habiliten les haces lo siguiente:

  -  Para entrar a un servidor: ssh user@ip  no te pedira password porque es un server y la clave que colocas en el profile ellos se la meten al server.
  -  Para entrar a un contenedor: ssh user@ip y te preguntara password

Para configurar los servers debemos entrar a el archivo en cada servidor:         emacs .ssh/authorized_keys
y agregar en ese archivo las keys que pueden entrar, una ca a ser la de holberton que pongo mas abajo y otra la de cada pc que tengas.

emacs .ssh/authorized_keys

		ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNdtrNGtTXe5Tp1EJQop8mOSAuRGLjJ6DW4PqX4wId/Kawz35ESampIqHSOTJmbQ8UlxdJuk0gAXKk3Ncle4safGYqM/VeDK3LN5iAJxf4kcaxNtS3eVxWBE5iF3FbIjOqwxw5Lf5sRa5yXxA8HfWidhbIG5TqKL922hPgsCGABIrXRlfZYeC0FEuPWdr6smOElSVvIXthRWp9cr685KdCI+COxlj1RdVsvIo+zunmLACF9PYdjB2s96Fn0ocD3c5SGLvDOFCyvDojSAOyE70ebIElnskKsDTGwfT4P6jh9OBzTyQEIS2jOaE5RQq4IB4DsMhvbjDSQrP0MdCLgwkN


# Instalar Mysql: 
1.		echo 'deb http://repo.mysql.com/apt/ubuntu/ trusty mysql-5.7-dmr' | sudo tee -a /etc/apt/sources.list
2.		sudo apt-get update
3.		sudo apt-get install mysql-server-5.7
4.		Escoger clave el usuario es root por default, yo siempre coloco password root

5.		Entrar a Mysql (va direccion y usuario):   mysql -h localhost -u root -p
6.		CREATE USER IF NOT EXISTS 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
7.		GRANT REPLICATION CLIENT ON *.* TO 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
8.		FLUSH PRIVILEGES;
9.		quit

10.		desde afuera miramos permisos:     mysql -uholberton_user -p -e "SHOW GRANTS FOR 'holberton_user'@'localhost'"

		****. Los pasos de arriba son para cuando se tenga que instalar Mysql en dos servidores uno maestro y un esclavo o replica.

Ahora 

1.		creamos BD llamada tyrell_corp: 	CREATE DATABASE IF NOT EXISTS tyrell_corp;
2.		seleccionamos la base de datos: 	USE tyrell_corp;
3.		creamos tabla llamada nexus6:	CREATE TABLE IF NOT EXISTS nexus6 (id INT(10) NOT NULL  AUTO_INCREMENT, name VARCHAR(30), PRIMARY KEY (id));
4.		damos permisos al usuario solo la base: 	GRANT ALL PRIVILEGES ON tyrell_corp.* TO 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
5.		insertamos datos a la tabla: 		INSERT INTO nexus6 (name) VALUES ('Leon');
6.		miramos las columnas de la tabla:		SHOW COLUMNS FROM <tyrell_corp> FROM <nexus6>;


# CONFIGURAMOS EL SERVER 1 PARA SER REPLICADO

1.		creamos usuario replica				CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED BY 'root';
2.		damos permisos SELECT a la tabla mysql.user		GRANT SELECT ON mysql.user TO 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
		(para que holbi pueda revisar)
3.		damos permisos de replica al esclavo;			GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%' IDENTIFIED BY 'root';
4.		refrescamos						FLUSH PRIVILEGES;

4.1		Cuadrando permisos en ambos servers con el puerto 3306:
		sudo ufw allow from 127.0.0.1 to 127.0.0.1 port 3306    
		Y
		sudo ufw allow 3306/tcp

5.		configuramos el archivo conf del server con:		sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
		y agregamos o habilitamos las siguientes lineas:	
							#bind-address           = 12.34.56.789
							server-id               = 1
							log_bin                 = /var/log/mysql/mysql-bin.log
							binlog_do_db            = tyrell_corp
6.		luego reiniciamos con: 				sudo service mysql restart
7.		Ahora de nuevo debemos entrat a Mysql y luego:	USE tyrell_corp;
8.		Bloqueamos la Base:					FLUSH TABLES WITH READ LOCK;
9.		tecleamos:						SHOW MASTER STATUS;

		File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
		+------------------+----------+--------------+------------------+-------------------+
		| mysql-bin.000001 |      154 | tyrell_corp  |                  |                   |

10.		salimos y sacamos una copia de la base de datos	mysqldump -uholberton_user -p --opt tyrell_corp > tyrell_corp.sql
11.		entramos de nuevo a Mysql y desbloqueamos		UNLOCK TABLES;
12.		salimos

# PASO DOS CONFIGURAS EL SERVER ESCLAVO

1.		creamos una base de datos con el mismo nombre.	CREATE DATABASE IF NOT EXISTS tyrell_corp;
2.		quit   y copiamos la base creada del server 1 al 2
3.		importamos la base de datos previamente creada	mysql -u root -p tyrell_corp < tyrell_corp.sql
3.1.		agregamos los permisos de select 			
		GRANT SELECT ON mysql.user TO 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
		
4.		configuramos el archivo conf del server dos:			sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
		agregamos o habilitamos las siguientes lineas:	
							#bind-address           = 12.34.56.789
							server-id               = 2
							relay-log               = /var/log/mysql/mysql-relay-bin.log
							log_bin                 = /var/log/mysql/mysql-bin.log
							binlog_do_db            = tyrell_corp

5.		reiniciamos mysql					sudo service mysql restart
6.		entramos a Mysql y digitamos				
		CHANGE MASTER TO MASTER_HOST='35.227.123.120', MASTER_USER='replica_user', MASTER_PASSWORD='root', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=  154;
		
		el numero 154 es el numero que dio arribaen el punto 9 en el server 1.

7.		iniciamos el esclavo					START SLAVE;
8.		para ver los detalles 				SHOW SLAVE STATUS\G
9.		fin
10.		Si hay un problema en la conexión, puede intentar
		iniciar el esclavo con un comando para omitirlo: 	SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1; SLAVE START;
