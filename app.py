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
def getMotors(carros):
    motors = []
    for carro in carros:
        if not carro["motor"] in motors:
            motors.append(carro["motor"])
    motors.sort()

    return motors

@app.route("/")
def home():
    motores = getMotors(carros)
    return render_template("index.html", cars=carros, motors=motores)

@app.route("/motorFilter", methods=["POST"])
def motorFilter():
    motores = getMotors(carros)
    if len(request.form) > 0:
        motor = request.form["options"]
        filtered = []
        for carro in carros:
            if motor == carro["motor"]:
                filtered.append(carro)
    else:
        filtered = carros
    
    return render_template("index.html", cars=filtered, motors=motores)

@app.route("/deleteModel", methods=["POST"])
def deleteModel():
    motores = getMotors(carros)
    modelo = request.form["modelo"]
    for carro in carros:
        if modelo == carro["modelo"]:
            carros.remove(carro)
    
    return render_template("index.html", cars=carros, motors=motores)

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
    
if __name__ == '__main__': 
    app.run(debug=True)