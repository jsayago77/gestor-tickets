# Gestor de Tickets

## Descripcion

Sistema gestor de tickets para la materia electiva Bases de Datos - Ing. Informatica, UCLA

## Autores

Jose Sayago, Dorieliz Guerrero, Alyeluz Perez

## Intalacion

Crear entorno virtual:

~~~shell
py -m venv .env 
~~~

Activar entorno virtual Linux:

~~~shell
source env/bin/activate 
~~~

Activar entorno virtual Windows:

~~~shell
env\Scripts\activate
~~~

Ejecutar con pip:

~~~shell
pip install flask flask_bcrypt email_validator flask-wtf sqlalchemy flask_login mysql-connector-python
~~~

Luego configurar la linea de conexion a la base de datos con el usuario, password, servidor, puerto, nombre de base de datos

~~~python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://<usuario>:<password>@<servidor>:<puerto>/<basededatos>"
~~~

Ejemplo:

~~~python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://usuario:password@localhost:3306/mydb"
~~~

## Ejecucion

Ejecutar en la linea de comandos:

~~~shell
flask --app index run
~~~
