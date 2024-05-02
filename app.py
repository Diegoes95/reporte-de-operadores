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
    cursor.execute("SELECT * FROM reportes3")
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
    cruce_1 = request.form["cruce_1"]
    cruce_2 = request.form["cruce_2"]
    evento = request.form["evento"]
    reportado_via = request.form["reportado_via"]
    operador = request.form["operador"]
    derivado_a = request.form["derivado_a"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    if cruce_1 and cruce_2 and evento and reportado_via and operador and derivado_a and fecha and hora:
        cursor = db.database.cursor()
        sql = "INSERT INTO reportes3 (cruce_1, cruce_2, evento, reportado_via, operador, derivado_a, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (cruce_1,cruce_2,evento,reportado_via,operador,derivado_a,fecha,hora)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM reportes3 WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    cruce_1 = request.form["cruce_1"]
    cruce_2 = request.form["cruce_2"]
    evento = request.form["evento"]
    reportado_via = request.form["reportado_via"]
    operador = request.form["operador"]
    derivado_a = request.form["derivado_a"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]


    if cruce_1 and cruce_2 and evento and reportado_via and operador and derivado_a and fecha and hora:
        cursor = db.database.cursor()
        sql = "UPDATE reportes3 SET cruce_1 = %s, cruce_2 = %s, evento = %s , reportado_via = %s, operador = %s , derivado_a = %s, fecha = %s, hora= %s WHERE id = %s"
        data = (cruce_1, cruce_2, evento, reportado_via, operador, derivado_a, fecha, hora, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)