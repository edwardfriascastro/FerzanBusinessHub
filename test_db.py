import psycopg

conexion = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ferzan_db",
    user="ferzan_user",
    password="ferzan_password"
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM empleados")

empleados = cursor.fetchall()

for empleado in empleados:
    print(empleado)

cursor.close()
conexion.close()