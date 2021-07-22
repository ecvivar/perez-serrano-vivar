from flask import Flask, session, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import re

app = Flask(__name__)

mysql = MySQL()
app.secret_key = 'your secret key'

#Configuracion MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'final'

mysql.init_app(app)

@app.route('/')
def productos():
    sql="SELECT * FROM productos;"
    conn=mysql.connect() #Hacemos la conexion a mysql
    cursor=conn.cursor()
    cursor.execute(sql) #Ejecutamos el string sql
    
    rows=cursor.fetchall()
    print(rows)

    conn.commit()
    return render_template('productos.html',productos=rows) # Renderizo la pagina index.html

@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
   
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(1) FROM usuarios WHERE username = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("SELECT password FROM usuarios WHERE username = %s;", [username_form])
            for row in cursor.fetchall():
                if password_form == row[0]:
                    session['usuario'] = username_form 
                    #session['carrito'] = username_form
                    msg ="Se ha identificado correctamente"
                    return redirect('/')
                else:
                    msg = "Credenciales no validas"
        return render_template('login.html', msg=msg)
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/register', methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO usuarios VALUES (NULL,%s,%s,%s)',(username, password, email, ))
            conn.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg) 
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg = msg)

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    # Aca debemos hacer una validacion para no permitir que usuarios no indenficados generen ordenes de pedido
    if 'usuario' not in session:
        msg = 'Debe iniciar sesion para continuar'
        return render_template('login.html', msg=msg)
    else:
        if request.method == 'POST' and 'codigo' in request.form and 'cantidad' in request.form:
            codigo_form = request.form['codigo']
            cantidad_form = request.form['cantidad']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo=%s",(codigo_form))
            
            itemCarrito = cursor.fetchall()
            for producto in itemCarrito:
                _codigo = producto[0]
                _descripcion = producto[1]
                _precio = producto[2]
                _foto = producto[4]

            # Deberiamos generar otra db e ir almacenando los productos seleccionados
            totalAbonar=float(_precio)*float(cantidad_form)
            usuario=session['usuario']

            # Deberiamo comprobar que el producto se encuentre en el carrito
            '''
            Esto no anda
            if int(codigo_form) == int(_codigo):
                nueva_cantidad = int(cantidad_form) + 1
                print(nueva_cantidad)
                conn = mysql.connect()
                cursor = conn.cursor()         
                cursor.execute("UPDATE carrito SET `cantidad`=%s WHERE codigo=%s",(nueva_cantidad,codigo_form))
                conn.commit()
            else:
            '''    
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "INSERT INTO `carrito`(`id`, `username`, `codigo`, `descripcion`, `precio`, `cantidad`, `foto`, `totalAbonar`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
            datos = (usuario, _codigo,_descripcion, _precio, cantidad_form, _foto, totalAbonar)         
            cursor.execute(sql,datos)
            conn.commit()

            return redirect('/carrito') 

@app.route('/search', methods=['POST'])
def search():
    busqueda = request.form['txtSearch']
    sql="SELECT * FROM productos where descripcion like %s"
    conn=mysql.connect() #Hacemos la conexion a mysql
    cursor=conn.cursor()
    cursor.execute(sql,(('%' + busqueda + '%'))) #Ejecutamos el string sql junto al comodin
    rows=cursor.fetchall()
    conn.commit()
    return render_template('productos.html',productos=rows)

@app.route('/carrito')
def carrito():
    if 'usuario' in session:
        usuario = session['usuario']
        print(usuario)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carrito WHERE username=%s",usuario)
        itemCarrito = cursor.fetchall()
        #conn.commit()
        print(itemCarrito)
        cursor.execute("SELECT COUNT(*) FROM carrito WHERE username=%s",usuario)
        registro = cursor.fetchone()
        mostrarCuantos = registro[0]
        cantidadProductos = int(mostrarCuantos)
        print(cantidadProductos)
        conn.commit()

    return render_template('carrito.html', itemCarrito=itemCarrito) # Renderizo la pagina index.html

@app.route('/borrar/<int:id>')
def borrar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE id=%s",(id))
    conn.commit()
    return redirect('/carrito')

@app.route('/vaciar_carrito/<string:username>')
def vaciar_carrito(username):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE username=%s",(username))
    conn.commit()
    return redirect('/carrito')

if __name__ == '__main__':
    app.run(debug=True)