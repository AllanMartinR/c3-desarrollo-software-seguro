# Medidas de desarrollo seguro aplicadas

## 1. Validación de entradas
- Nombre obligatorio, longitud máxima y caracteres permitidos.
- Correo validado mediante formato.
- Edad convertida a entero y limitada entre 1 y 120.
- La validación se realiza en el servidor.

## 2. Normalización
- Se eliminan espacios externos con `strip()`.
- El correo se normaliza a minúsculas.

## 3. Protección contra SQL Injection
Todas las consultas que reciben valores externos usan parámetros:

`WHERE id = ?`

`VALUES (?, ?, ?)`

Nunca se construye SQL mediante concatenación de datos introducidos por el usuario.

## 4. Manejo de errores
- Se controlan errores de datos inválidos.
- Se controla el intento de registrar un correo duplicado.
- La aplicación se ejecuta con `debug=False` para no exponer trazas internas al usuario.

## 5. Código seguro
- Se utiliza Flask y SQLite con interfaces estándar.
- La lógica de validación está separada de las rutas.
- No se incluyen consultas SQL construidas dinámicamente con entrada directa.

## 6. Código muerto o inalcanzable
Se mantuvo únicamente la funcionalidad necesaria para la demostración y se evitó agregar código sin uso.
