Proyecto eShop en Python Flask y MySQL:

Definimos y preparamos el entorno de Programacion.

Creamos la carpeta raiz donde se almacenara nuestro proyecto:

C:\proyecto-integrador>

Luego creamos el entorno virtual:

C:\proyecto-integrador>pip install virtualenv

Creamos el entorno:

C:\proyecto-integrador>virtualenv env

Ahora activamos el entorno virtual:

C:\proyecto-integrador>env\Scripts\activate

Definido el espacio de trabajo instalar:

pip install Flask
pip install flask-mysql

Para integrar SDK Python de Mercado Pago:

pip3 install mercadopago

Verificar que esten instalados los siguientes modulos (ejecutar pip freeze):

certifi==2021.5.30
charset-normalizer==2.0.3
click==8.0.1
colorama==0.4.4
Flask==2.0.1
Flask-MySQL==1.5.2
idna==3.2
itsdangerous==2.0.1
Jinja2==3.0.1
MarkupSafe==2.0.1
mercadopago==2.0.7
PyMySQL==1.0.2
requests==2.26.0
urllib3==1.26.6
Werkzeug==2.0.1

Luego importar la Base de Datos:

final.sql

Inicializar servidor flask:

(env) C:\proyecto-integrador>python app.py

Acceder a la aplicacion:

http://127.0.0.1:5000/