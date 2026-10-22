function EmployeeForm({
  nuevoId,
  setNuevoId,
  nuevoNombre,
  setNuevoNombre,
  nuevoDepartamento,
  setNuevoDepartamento,
  nuevoSalario,
  setNuevoSalario,
  registrarEmpleado,
}) {
  return (
    <section>
      <h2>Registrar empleado</h2>

      <form onSubmit={registrarEmpleado}>
        <div>
          <label htmlFor="nuevoId">ID del empleado</label>
          <input
            id="nuevoId"
            type="number"
            value={nuevoId}
            onChange={(evento) => setNuevoId(evento.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="nuevoNombre">Nombre</label>
          <input
            id="nuevoNombre"
            value={nuevoNombre}
            onChange={(evento) => setNuevoNombre(evento.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="nuevoDepartamento">Departamento</label>
          <input
            id="nuevoDepartamento"
            value={nuevoDepartamento}
            onChange={(evento) => setNuevoDepartamento(evento.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="nuevoSalario">Salario</label>
          <input
            id="nuevoSalario"
            type="number"
            min="0"
            value={nuevoSalario}
            onChange={(evento) => setNuevoSalario(evento.target.value)}
            required
          />
        </div>

        <button type="submit">Registrar empleado</button>
      </form>
    </section>
  );
}

export default EmployeeForm;
