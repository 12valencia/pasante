
from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    empresa = request.form['empresa']
    direccion = request.form['direccion']
    nit = request.form['nit']
    telefono = request.form['telefono']
    email = request.form['email']

    if empresa and direccion and nit and telefono and email:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (empresa, direccion, nit,telefono, email) VALUES (%s, %s, %s,%s,%s)"
        data = (empresa, direccion, nit,telefono, email)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    empresa = request.form['empresa']
    direccion = request.form['direccion']
    nit = request.form['nit']
    telefono = request.form['telefono']
    email = request.form['email']

    if empresa and direccion and nit and telefono and email:
        cursor = db.database.cursor()
        sql = "UPDATE users SET empresa = %s, direccion = %s, nit = %s telefono = %s, email =%s,  WHERE id = %s"
        data = (empresa, direccion, nit,telefono, email, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)








