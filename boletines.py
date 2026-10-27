import json
import os
from datetime import datetime
import random

CA = "amiguito123"
CP = "Hola123"
CC = "hola amiguito 123"
DB_EST = "estudiantes.json"

def cargar_db():
    if os.path.exists(DB_EST):
        with open(DB_EST, "r") as f:
            return json.load(f)
    return {}

def guardar_db(db):
    with open(DB_EST, "w") as f:
        json.dump(db, f, indent=4)

def check(ok):
    c = input("Contrasena: ")
    if c != ok:
        print("Incorrecta!")
        return False
    return True

def mostrar_boletin_bonito(datos):
    print("\n=============================")
    print("       BOLETIN ESCOLAR")
    print("=============================")
    print("Estudiante:", datos["estudiante"])
    print("Periodo:", datos["periodo"])
    print("-----------------------------")
    notas = datos["notas"]
    total = 0
    for materia, nota in notas.items():
        total += nota
        if nota >= 3.0:
            estado = "APROBADA"
        else:
            estado = "REPROBADA"
        print(materia + ":", nota, "-", estado)
    promedio = total / len(notas)
    print("-----------------------------")
    print("Promedio:", round(promedio, 2))
    if promedio >= 3.0:
        print("ESTADO: APROBADO")
    else:
        print("ESTADO: REPROBADO")
    print("=============================")

def gestion_estudiantes():
    print("\n--- ADMIN - DATOS PERSONALES ---")
    if not check(CA):
        return
    db = cargar_db()
    cod = input("Codigo estudiante: ").strip()
    if cod in db:
        info = db[cod]
        print("\n=============================")
        print(" ESTUDIANTE YA REGISTRADO")
        print("=============================")
        print("Codigo:", cod)
        print("Nombre:", info["nombre"])
        print("Documento:", info["documento"])
        print("Grado:", info["grado"])
        print("Edad:", info["edad"])
        print("Telefono:", info["telefono"])
        print("Direccion:", info["direccion"])
        print("Acudiente:", info["acudiente"])
        print("-----------------------------")
        print("CONTRASENA:", info["contrasena"])
        print("Fecha:", info["fecha"])
        print("=============================")
        op = input("Cambiar clave? s/n: ").lower()
        if op == "s":
            nueva = input("Nueva clave: ")
            db[cod]["contrasena"] = nueva
            guardar_db(db)
            print("Actualizada!")
    else:
        print("\n--- NUEVO ---")
        nombre = input("Nombre completo: ")
        doc = input("Documento: ")
        grado = input("Grado: ")
        edad = input("Edad: ")
        tel = input("Telefono: ")
        direccion = input("Direccion: ")
        acudiente = input("Acudiente: ")
        clave = input("Crea clave: ")
        db[cod] = {}
        db[cod]["nombre"] = nombre
        db[cod]["documento"] = doc
        db[cod]["grado"] = grado
        db[cod]["edad"] = edad
        db[cod]["telefono"] = tel
        db[cod]["direccion"] = direccion
        db[cod]["acudiente"] = acudiente
        db[cod]["contrasena"] = clave
        db[cod]["fecha"] = datetime.now().strftime("%d/%m/%Y")
        guardar_db(db)
        print("Registrado! Clave:", clave)

while True:
    print("\n--- MENU V4.2 ---")
    print("1. Crear boletin")
    print("2. Ver boletin")
    print("3. Agregar queja [PROFES]")
    print("4. Ver mis quejas [ESTUDIANTES]")
    print("5. Ver todos")
    print("6. Gestion estudiantes [ADMIN]")
    print("7. Salir")
    op = input("Elige 1-7: ").strip()

    if op == "1":
        print("\nRESTRINGIDO")
        if not check(CC):
            continue
        est = input("Nombre: ")
        per = input("Periodo: ")
        cant = int(input("Cuantas materias: "))
        notas = {}
        for i in range(cant):
            nom = input("Materia: ")
            nota = float(input("Nota: "))
            notas[nom] = nota
        datos = {}
        datos["estudiante"] = est
        datos["periodo"] = per
        datos["notas"] = notas
        mostrar_boletin_bonito(datos)
        cod = input("\nCodigo para guardar: ")
        with open("boletin_" + cod + ".json", "w") as f:
            json.dump(datos, f, indent=4)
        print("Guardado!")

    elif op == "2":
        cod = input("Codigo boletin: ").strip()
        try:
            with open("boletin_" + cod + ".json", "r") as f:
                datos = json.load(f)
            mostrar_boletin_bonito(datos)
        except:
            print("No existe boletin con ese codigo")

    elif op == "3":
        print("\nZONA PROFES")
        if not check(CP):
            continue
        cod = input("Codigo: ").strip()
        queja = input("Queja: ")
        fecha = datetime.now().strftime("%d/%m/%Y")
        arch = "quejas_" + cod + ".json"
        lista = []
        if os.path.exists(arch):
            with open(arch, "r") as f:
                lista = json.load(f)
        lista.append({"fecha": fecha, "texto": queja})
        with open(arch, "w") as f:
            json.dump(lista, f, indent=4)
        print("Guardada")

    elif op == "4":
        print("\n--- MIS QUEJAS ---")
        db = cargar_db()
        cod = input("Tu codigo: ").strip()
        if cod not in db:
            print("No existe")
            continue
        clave = input("Tu contrasena: ").strip()
        if clave != db[cod]["contrasena"]:
            print("Incorrecta!")
            continue
        print("\nHola", db[cod]["nombre"])
        arch = "quejas_" + cod + ".json"
        if not os.path.exists(arch):
            print("No tienes quejas!")
            continue
        with open(arch, "r") as f:
            lista = json.load(f)
        for i, q in enumerate(lista, 1):
            print(str(i) + ". [" + q["fecha"] + "] " + q["texto"])

    elif op == "5":
        print("\nADMIN")
        if not check(CA):
            continue
        for f in os.listdir():
            if f.startswith("boletin_"):
                print(f)

    elif op == "6":
        gestion_estudiantes()

    elif op == "7":
        print("Chao!")
        break
#Hola, el programa funciona como base de datos, generar boletines, agregar quejas y observar todo lo nombrado anteriormente 
#Primero genera un perfil para el estudiante llenando las preguntas, boletín o queja y registralo o guardalo con el código q te de o decidas crear, con ese código puedes ver cuando quieras lo que digan o publique los profesores además con la opción de código y clave crea un anillo de doble seguridad para q solo tu puedas ingresar 
#Pruebalo, deja tu like y reseña porfa