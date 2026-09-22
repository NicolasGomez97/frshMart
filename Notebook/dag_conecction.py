# Simular logs de Airflow como texto
logs = """
[2024-09-19 03:00:05] INFO - Starting task extract_orders
[2024-09-19 03:00:05] INFO - Execution date: 2024-09-18
[2024-09-19 03:00:06] INFO - Connecting to PostgreSQL at freshmart-prod.rds.amazonaws.com:5432
[2024-09-19 03:00:06] ERROR - Connection failed: psycopg2.OperationalError: FATAL: password authentication failed for user "data_readonly"
[2024-09-19 03:05:06] ERROR - Connection failed (retry 2/3): password authentication failed
[2024-09-19 03:10:06] ERROR - Connection failed (retry 3/3): password authentication failed
[2024-09-19 03:10:06] ERROR - Max retries reached. Task FAILED.
"""

# 1. Extraer solo las líneas de ERROR
errores = [line.strip() for line in logs.strip().split("\n") if "ERROR" in line]
print("Líneas de error:")
for e in errores:
    print(f"  {e}")

# 2. Identificar el tipo de error
tipo_error = "credenciales"
print(f"\nTipo de error: {tipo_error}")
print("Evidencia: 'password authentication failed' indica que el servidor")
print("  está accesible (no es red) pero la contraseña es incorrecta.")

# 3. ¿Qué preguntarías para verificar?
hipotesis = "Las credenciales del usuario data_readonly fueron rotadas/cambiadas"
print(f"Hipótesis: {hipotesis}")
print("Preguntaría a: equipo de infraestructura/DBA")
print("Pregunta: ¿Se rotaron las credenciales de RDS esta semana?")