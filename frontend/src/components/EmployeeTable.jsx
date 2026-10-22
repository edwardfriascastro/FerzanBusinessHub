function EmployeeTable({
  empleados,
  cargando,
  error,
  mensajeEliminacion,
  seleccionarEmpleado,
  eliminarEmpleado,
}) {
  return (
    <section>
      <h2>Lista de empleados</h2>

      {cargando && <p>Cargando empleados...</p>}

      {error && <p role="alert">{error}</p>}

      {mensajeEliminacion && <p role="status">{mensajeEliminacion}</p>}

      {!cargando && empleados.length === 0 && (
        <p>No hay empleados para mostrar.</p>
      )}

      {empleados.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Departamento</th>
              <th>Salario</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {empleados.map((empleado) => (
              <tr key={empleado.empleado_id}>
                <td>{empleado.empleado_id}</td>
                <td>{empleado.nombre}</td>
                <td>{empleado.departamento}</td>
                <td>
                  RD$
                  {Number(empleado.salario).toLocaleString("es-DO")}
                </td>
                <td>
                  <button
                    type="button"
                    onClick={() => seleccionarEmpleado(empleado)}
                  >
                    Editar
                  </button>

                  <button
                    type="button"
                    onClick={() => eliminarEmpleado(empleado.empleado_id)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default EmployeeTable;
