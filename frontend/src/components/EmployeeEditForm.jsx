function EmployeeEditForm({
  empleadoId,
  nombreEditado,
  setNombreEditado,
  departamentoEditado,
  setDepartamentoEditado,
  salarioEditado,
  setSalarioEditado,
  actualizarEmpleado,
}) {
  return (
    <section>
      <h2>Actualizar empleado</h2>

      <p>
        Selecciona un empleado de la lista para cargar sus datos en este
        formulario.
      </p>

      <form onSubmit={actualizarEmpleado}>
        <div>
          <label htmlFor="empleadoId">ID del empleado</label>
          <input
            id="empleadoId"
            type="number"
            value={empleadoId}
            readOnly
            required
          />
        </div>

        <div>
          <label htmlFor="nombreEditado">Nombre</label>
          <input
            id="nombreEditado"
            value={nombreEditado}
            onChange={(evento) => setNombreEditado(evento.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="departamentoEditado">Departamento</label>
          <input
            id="departamentoEditado"
            value={departamentoEditado}
            onChange={(evento) => setDepartamentoEditado(evento.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="salarioEditado">Salario</label>
          <input
            id="salarioEditado"
            type="number"
            min="0"
            value={salarioEditado}
            onChange={(evento) => setSalarioEditado(evento.target.value)}
            required
          />
        </div>

        <button type="submit">Guardar cambios</button>
      </form>
    </section>
  );
}

export default EmployeeEditForm;
