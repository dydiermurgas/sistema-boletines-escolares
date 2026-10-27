import json
import os
from datetime import datetime
import random

# ========== V5.0 INTERNACIONAL - 4 IDIOMAS ==========
LANG = "es"
T = {
    "menu_title": {"es": "--- MENU V5.2 ---", "en": "--- MENU V5.2 INTERNATIONAL ---", "fr": "--- MENU V5.2 INTERNATIONAL ---", "de": "--- MENÜ V5.2 INTERNATIONAL ---"},
    "opt1": {"es": "1. Crear boletin", "en": "1. Create report card", "fr": "1. Créer bulletin", "de": "1. Zeugnis erstellen"},
    "opt2": {"es": "2. Ver boletin", "en": "2. View report card", "fr": "2. Voir bulletin", "de": "2. Zeugnis ansehen"},
    "opt3": {"es": "3. Agregar queja [PROFES]", "en": "3. Add complaint [TEACHERS]", "fr": "3. Ajouter plainte [PROFS]", "de": "3. Beschwerde hinzufügen [LEHRER]"},
    "opt4": {"es": "4. Ver mis quejas [ESTUDIANTES]", "en": "4. View my complaints [STUDENTS]", "fr": "4. Voir mes plaintes [ETUDIANTS]", "de": "4. Meine Beschwerden ansehen [SCHÜLER]"},
    "opt5": {"es": "5. Ver todos", "en": "5. View all", "fr": "5. Voir tout", "de": "5. Alle ansehen"},
    "opt6": {"es": "6. Gestion estudiantes [ADMIN]", "en": "6. Student management [ADMIN]", "fr": "6. Gestion étudiants [ADMIN]", "de": "6. Schülerverwaltung [ADMIN]"},
    "opt7": {"es": "7. Salir", "en": "7. Exit", "fr": "7. Quitter", "de": "7. Beenden"},
    "choose": {"es": "Elige 1-7: ", "en": "Choose 1-7: ", "fr": "Choisissez 1-7: ", "de": "Wählen 1-7: "},
    "pass_prompt": {"es": "Contrasena: ", "en": "Password: ", "fr": "Mot de passe: ", "de": "Passwort: "},
    "incorrect": {"es": "Incorrecta!", "en": "Incorrect!", "fr": "Incorrect!", "de": "Falsch!"},
    "guardado": {"es": "Guardado!", "en": "Saved!", "fr": "Enregistré!", "de": "Gespeichert!"},
    "chao": {"es": "Chao!", "en": "Bye!", "fr": "Au revoir!", "de": "Tschüss!"},
    "no_existe": {"es": "No existe boletin con ese codigo", "en": "Report not found", "fr": "Bulletin introuvable", "de": "Zeugnis nicht gefunden"},
}
def tr(k): return T.get(k, {}).get(LANG, k)

CA = "amiguito123"
CP = "Hola123"
CC = "hola amiguito 123"
DB_EST = "estudiantes.json"

def cargar_db():
    if os.path.exists(DB_EST):
        with open(DB_EST, "r") as f: return json.load(f)
    return {}
def guardar_db(db):
    with open(DB_EST, "w") as f: json.dump(db, f, indent=4)
def check(ok):
    c = input(tr("pass_prompt"))
    if c != ok:
        print(tr("incorrect"))
        return False
    return True

def mostrar_boletin_bonito(datos):
    print("\n=============================")
    print("       BOLETIN ESCOLAR / REPORT")
    print("=============================")
    print(f"Estudiante / Student: {datos['estudiante']}")
    print(f"Periodo / Term: {datos['periodo']}")
    print("-----------------------------")
    total = 0
    for materia, nota in datos["notas"].items():
        total += nota
        estado = "APROBADA/PASSED" if nota >= 3.0 else "REPROBADA/FAILED"
        print(f"{materia}: {nota} - {estado}")
    promedio = total / len(datos["notas"])
    print("-----------------------------")
    print(f"Promedio / Average: {round(promedio, 2)}")
    print(f"ESTADO / STATUS: {'APROBADO/PASSED' if promedio >=3.0 else 'REPROBADO/FAILED'}")
    print("=============================")

def gestion_estudiantes():
    print("\n--- ADMIN ---")
    if not check(CA): return
    db = cargar_db()
    cod = input("Codigo estudiante: ").strip()
    if cod in db:
        info = db[cod]
        print(f"\nNombre: {info['nombre']} | Clave: {info['contrasena']} | Grado: {info['grado']}")
        if input("Cambiar clave? s/n: ").lower() == "s":
            db[cod]["contrasena"] = input("Nueva clave: ")
            guardar_db(db)
            print("Actualizada!")
    else:
        db[cod] = {
            "nombre": input("Nombre completo: "), "documento": input("Documento: "),
            "grado": input("Grado: "), "edad": input("Edad: "), "telefono": input("Telefono: "),
            "direccion": input("Direccion: "), "acudiente": input("Acudiente: "),
            "contrasena": input("Crea clave: "), "fecha": datetime.now().strftime("%d/%m/%Y")
        }
        guardar_db(db)
        print(f"Registrado! Clave: {db[cod]['contrasena']}")

# --- SELECTOR DE IDIOMA ---
print("==========================================")
print(" Seleccione idioma / Select language")
print(" [1] Español  [2] English  [3] Français  [4] Deutsch")
print("==========================================")
sel = input("Elige / Choose 1-4 [1]: ").strip()
if sel == "2": LANG = "en"
elif sel == "3": LANG = "fr"
elif sel == "4": LANG = "de"

while True:
    print(f"\n{tr('menu_title')}")
    print(tr("opt1")); print(tr("opt2")); print(tr("opt3")); print(tr("opt4")); print(tr("opt5")); print(tr("opt6")); print(tr("opt7"))
    op = input(tr("choose")).strip()
    if op == "1":
        if not check(CC): continue
        est = input("Nombre: "); per = input("Periodo: "); cant = int(input("Cuantas materias: "))
        notas = {input("Materia: "): float(input("Nota: ")) for _ in range(cant)}
        datos = {"estudiante": est, "periodo": per, "notas": notas}
        mostrar_boletin_bonito(datos)
        cod = input("\nCodigo para guardar: ")
        with open("boletin_" + cod + ".json", "w") as f: json.dump(datos, f, indent=4)
        print(tr("guardado"))
    elif op == "2":
        cod = input("Codigo boletin: ").strip()
        try:
            with open("boletin_" + cod + ".json", "r") as f: mostrar_boletin_bonito(json.load(f))
        except: print(tr("no_existe"))
    elif op == "3":
        if not check(CP): continue
        cod = input("Codigo: ").strip(); queja = input("Queja: "); fecha = datetime.now().strftime("%d/%m/%Y")
        arch = "quejas_" + cod + ".json"; lista = []
        if os.path.exists(arch):
            with open(arch, "r") as f: lista = json.load(f)
        lista.append({"fecha": fecha, "texto": queja})
        with open(arch, "w") as f: json.dump(lista, f, indent=4)
        print(tr("guardado"))
    elif op == "4":
        db = cargar_db(); cod = input("Tu codigo: ").strip()
        if cod not in db or input("Tu contrasena: ").strip() != db[cod]["contrasena"]:
            print(tr("incorrect")); continue
        arch = "quejas_" + cod + ".json"
        if not os.path.exists(arch): print("No tienes quejas!"); continue
        with open(arch, "r") as f:
            for i, q in enumerate(json.load(f), 1): print(f"{i}. [{q['fecha']}] {q['texto']}")
    elif op == "5":
        if not check(CA): continue
        for f in os.listdir():
            if f.startswith("boletin_"): print(f)
    elif op == "6": gestion_estudiantes()
    elif op == "7": print(tr("chao")); break
#Hola, el programa funciona como base de datos, generar boletines, agregar quejas y observar todo lo nombrado anteriormente 
#Primero genera un perfil para el estudiante llenando las preguntas, boletín o queja y registralo o guardalo con el código q te de o decidas crear, con ese código puedes ver cuando quieras lo que digan o publique los profesores además con la opción de código y clave crea un anillo de doble seguridad para q solo tu puedas ingresar 
#Pruebalo, deja tu like y reseña porfa
#Hello! This program functions as a database where you can generate report cards, add complaints, and keep track of all the information mentioned above.
#First, create a student profile by filling in the required details—such as report cards or complaints—and save it using a unique code (either one provided to you or one you choose to create). With this code, you can view any comments or posts made by teachers at any time. Plus, by using both a code and a password, you get an extra layer of security, ensuring that only you can access the information.
#Give it a try—please leave a like and a review!
#Bonjour ! Ce programme fonctionne comme une base de données : il permet de générer des bulletins, d'ajouter des signalements et de consulter toutes ces informations.
#Commencez par créer un profil pour l'élève en remplissant les champs requis (bulletins ou signalements), puis enregistrez-le à l'aide d'un code — généré automatiquement ou choisi par vos soins. Grâce à ce code, vous pouvez consulter à tout moment les commentaires ou publications des enseignants. De plus, le système combinant code et mot de passe offre une double sécurité, garantissant que vous seul puissiez accéder aux données.
#Essayez-le, et n'hésitez pas à laisser un « j'aime » ainsi qu'un avis !

#Hallo! Das Programm fungiert als Datenbank: Du kannst Zeugnisse erstellen, Beschwerden hinzufügen und all diese Informationen einsehen.
#Zuerst erstellst du ein Profil für den Schüler, indem du die entsprechenden Fragen beantwortest sowie Zeugnisse oder Beschwerden hinzufügst. Speichere das Profil unter einem Code – entweder einem automatisch generierten oder einem, den du selbst festlegst. Mit diesem Code kannst du jederzeit einsehen, was die Lehrkräfte eingetragen oder veröffentlicht haben. Dank der Kombination aus Code und Passwort ist dein Zugang zudem doppelt abgesichert, sodass nur du darauf zugreifen kannst.
#Probier es aus – lass bitte ein Like und eine Bewertung da!