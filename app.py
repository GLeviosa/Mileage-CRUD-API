from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_restful import Api, Resource, reqparse

app=Flask(__name__)

carros= [
    { 
        'modelo': 'HB20',
        'velocidade_max': '180.0',
        'motor': '1.6',
        'marca': 'Hyundai'
    },

    { 
        'modelo': 'XC60',
        'velocidade_max': '175.0',
        'motor': '2.0',
        'marca': 'Volvo'
    },

    { 
        'modelo': 'Compass',
        'velocidade_max': '195.0',
        'motor': '2.0',
        'marca': 'Jeep'
    },

    { 
        'modelo': 'Fox',
        'velocidade_max': '160.0',
        'motor': '1.6',
        'marca': 'Volkswagen'
    },

    { 
        'modelo': 'Evoque',
        'velocidade_max': '185.0',
        'motor': '2.0',
        'marca': 'Land Rover'
    },

    { 
        'modelo': 'Polo',
        'velocidade_max': '195.0',
        'motor': '1.6',
        'marca': 'Volkswagen'
    }

]

# INSIRA SEU CÓDIGO

# Devolve uma lista de motores dos carros
def getMotors(carros):
    motors = []
    for carro in carros:
        if not carro["motor"] in motors:
            motors.append(carro["motor"])
    motors.sort()

    return motors

# Rota da página inicial
@app.route("/")
def home():
    motores = getMotors(carros)
    return render_template("index.html", cars=carros, motors=motores)

# Rora do filtro dos carros pelo motor selecionado
@app.route("/motorFilter", methods=["POST"])
def motorFilter():
    motores = getMotors(carros)
    if len(request.form) > 0:
        motor = request.form["options"]
        filtered = []
        for carro in carros:
            if motor == carro["motor"]:
                filtered.append(carro)
        return render_template("index.html", cars=filtered, motors=motores)
    else:
        return render_template("index.html", cars=carros, motors=motores)

# Rora para deletar um modelo da lista
@app.route("/deleteModel", methods=["POST"])
def deleteModel():
    motores = getMotors(carros)
    modelo = request.form["modelo"]
    for carro in carros:
        if modelo == carro["modelo"]:
            carros.remove(carro)
    
    return render_template("index.html", cars=carros, motors=motores)

# Rota de edição do modelo
@app.route("/edit", methods=["GET", "POST"])
def edit():
    motores = getMotors(carros)
    if request.method == "GET":
        modelo = request.args.get("modelo")
        for carro in carros:
            if modelo == carro["modelo"]:
                editCar = carro
        
        return render_template("edit.html", car=editCar) 

    elif request.method == "POST":
        if len(request.form) > 0:
            modelo = request.form["modelo"]
            velocidade_max = request.form["velocidade_max"]
            motor = request.form["motor"]
            marca = request.form["marca"]

            for carro in carros:
                if modelo == carro["modelo"]:
                    carro["velocidade_max"] = velocidade_max
                    carro["motor"] = motor
                    carro["marca"] = marca

        return render_template("index.html", cars=carros, motors=motores)
        
# Rota para adicionar um modelo à lista
@app.route("/add", methods=["GET", "POST"])
def add():
    
    if request.method == "GET":

        return render_template("add.html")

    elif request.method == "POST":
        if len(request.form) > 0:
            newCar = {
                "modelo" : request.form["modelo"],
                "velocidade_max" : request.form["velocidade_max"],
                "motor" : request.form["motor"],
                "marca" : request.form["marca"]
            }
            carros.append(newCar)
            motores = getMotors(carros)
        return render_template("index.html", cars=carros, motors=motores)

# Rota para a página de gráficos
@app.route("/grafos")
def grafos():
    motor_max = 0
    vel_max = 0
    motors = getMotors(carros)
    
    for motor in motors:
        if float(motor) > motor_max:
            motor_max = float(motor)
    
    for carro in carros:
        if float(carro["velocidade_max"]) > vel_max:
            vel_max = float(carro["velocidade_max"])
    
    return render_template("grafos.html", cars=carros, motor_max=motor_max, vel_max=vel_max)

if __name__ == '__main__': 
    app.run(debug=True)