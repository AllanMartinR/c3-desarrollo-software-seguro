# C3. Desarrollo de software seguro

Aplicación web CRUD de usuarios creada para demostrar prácticas básicas de desarrollo de software seguro.

## Características

- Alta, consulta, edición y eliminación de usuarios.
- Validación de entradas en el servidor.
- Restricciones de longitud y formato.
- Manejo controlado de errores.
- Consultas SQL parametrizadas.
- No se concatena la entrada del usuario directamente en SQL.
- Uso de plantillas de Jinja para representar los datos.
- `debug=False` en ejecución.

## Ejecutar localmente

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000`.

## Prueba de seguridad

En los campos de entrada se pueden probar valores con caracteres especiales. La aplicación debe rechazarlos si no cumplen las reglas de validación.

Para SQL Injection, por ejemplo, una entrada como:

`' OR 1=1 --`

no se incorpora como parte de una sentencia SQL porque las operaciones de base de datos utilizan parámetros (`?`).

## Para publicar

Esta aplicación puede desplegarse en un servicio compatible con Python/Flask. Configura una clave secreta real mediante una variable de entorno antes de un despliegue público.

## Nota

La base SQLite incluida es adecuada para una demostración académica. Para producción se recomienda una base de datos administrada y configuración segura de secretos, HTTPS y controles adicionales.
