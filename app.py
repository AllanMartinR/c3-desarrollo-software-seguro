from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave-en-produccion"
DB = Path(__file__).with_name("app.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            edad INTEGER NOT NULL CHECK (edad BETWEEN 1 AND 120)
        )
    """)
    conn.commit()
    conn.close()

def validar_usuario(nombre, correo, edad):
    errores = []
    nombre = nombre.strip()
    correo = correo.strip().lower()

    if not nombre or len(nombre) > 80:
        errores.append("El nombre es obligatorio y debe tener máximo 80 caracteres.")
    elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .'-]+", nombre):
        errores.append("El nombre contiene caracteres no permitidos.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        errores.append("El correo no tiene un formato válido.")

    try:
        edad = int(edad)
        if not 1 <= edad <= 120:
            errores.append("La edad debe estar entre 1 y 120.")
    except (TypeError, ValueError):
        errores.append("La edad debe ser un número entero.")

    return errores, nombre, correo, edad

@app.route("/")
def index():
    conn = get_db()
    usuarios = conn.execute("SELECT id, nombre, correo, edad FROM usuarios ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", usuarios=usuarios)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        errores, nombre, correo, edad = validar_usuario(
            request.form.get("nombre", ""),
            request.form.get("correo", ""),
            request.form.get("edad", "")
        )
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("form.html", titulo="Agregar usuario",
                                   usuario={"nombre": nombre, "correo": correo, "edad": request.form.get("edad", "")})

        try:
            conn = get_db()
            # Consulta parametrizada: evita concatenar directamente datos del usuario.
            conn.execute(
                "INSERT INTO usuarios (nombre, correo, edad) VALUES (?, ?, ?)",
                (nombre, correo, edad)
            )
            conn.commit()
            conn.close()
            flash("Usuario agregado correctamente.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Ese correo ya está registrado.", "error")

    return render_template("form.html", titulo="Agregar usuario", usuario={})

@app.route("/editar/<int:user_id>", methods=["GET", "POST"])
def editar(user_id):
    conn = get_db()
    usuario = conn.execute(
        "SELECT id, nombre, correo, edad FROM usuarios WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    if usuario is None:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        errores, nombre, correo, edad = validar_usuario(
            request.form.get("nombre", ""),
            request.form.get("correo", ""),
            request.form.get("edad", "")
        )
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("form.html", titulo="Editar usuario",
                                   usuario={"id": user_id, "nombre": nombre, "correo": correo, "edad": request.form.get("edad", "")})

        try:
            conn = get_db()
            conn.execute(
                "UPDATE usuarios SET nombre = ?, correo = ?, edad = ? WHERE id = ?",
                (nombre, correo, edad, user_id)
            )
            conn.commit()
            conn.close()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Ese correo ya está registrado.", "error")

    return render_template("form.html", titulo="Editar usuario", usuario=dict(usuario))

@app.post("/eliminar/<int:user_id>")
def eliminar(user_id):
    conn = get_db()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
