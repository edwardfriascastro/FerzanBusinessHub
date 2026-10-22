import { useState, useEffect } from "react";
import "./App.css";

import EmployeeTable from "./components/EmployeeTable";
import EmployeeForm from "./components/EmployeeForm";
import EmployeeEditForm from "./components/EmployeeEditForm";
import { iniciarSesionAPI } from "./services/auth";

import {
  obtenerEmpleados,
  crearEmpleado,
  actualizarEmpleadoAPI,
  eliminarEmpleadoAPI,
} from "./services/empleados";

function App() {
  // Autenticación
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const [logueado, setLogueado] = useState(
    Boolean(localStorage.getItem("token")),
  );

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Lista de empleados
  const [empleados, setEmpleados] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  // Formulario de registro
  const [nuevoId, setNuevoId] = useState("");
  const [nuevoNombre, setNuevoNombre] = useState("");
  const [nuevoDepartamento, setNuevoDepartamento] = useState("");
  const [nuevoSalario, setNuevoSalario] = useState("");
  const [mensajeRegistro, setMensajeRegistro] = useState("");

  // Formulario de edición
  const [empleadoId, setEmpleadoId] = useState("");
  const [nombreEditado, setNombreEditado] = useState("");
  const [departamentoEditado, setDepartamentoEditado] = useState("");
  const [salarioEditado, setSalarioEditado] = useState("");
  const [mensajeEdicion, setMensajeEdicion] = useState("");

  // Mensaje de eliminación
  const [mensajeEliminacion, setMensajeEliminacion] = useState("");

  // GET: consultar empleados
  async function cargarEmpleados(tokenActual) {
    setCargando(true);
    setError("");

    try {
      const datos = await obtenerEmpleados(tokenActual);
      setEmpleados(datos);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }

  // Cargar empleados cuando ya existe una sesión
  useEffect(() => {
    const tokenGuardado = localStorage.getItem("token");

    if (tokenGuardado) {
      cargarEmpleados(tokenGuardado);
    }
  }, []);

  // LOGIN: iniciar sesión

  async function iniciarSesion(evento) {
    evento.preventDefault();
    setError("");

    try {
      const datos = await iniciarSesionAPI(email, password);

      localStorage.setItem("token", datos.access_token);

      setToken(datos.access_token);
      setLogueado(true);

      await cargarEmpleados(datos.access_token);
    } catch (err) {
      setError(err.message);
    }
  }

  // POST: registrar empleado
  async function registrarEmpleado(evento) {
    evento.preventDefault();

    setMensajeRegistro("");
    setError("");

    try {
      const empleado = {
        empleado_id: Number(nuevoId),
        nombre: nuevoNombre,
        departamento: nuevoDepartamento,
        salario: Number(nuevoSalario),
      };

      await crearEmpleado(token, empleado);

      setMensajeRegistro("Empleado registrado correctamente.");

      setNuevoId("");
      setNuevoNombre("");
      setNuevoDepartamento("");
      setNuevoSalario("");

      await cargarEmpleados(token);
    } catch (err) {
      setMensajeRegistro(`Error: ${err.message}`);
    }
  }

  // Seleccionar empleado para editar
  function seleccionarEmpleado(empleado) {
    setEmpleadoId(String(empleado.empleado_id));
    setNombreEditado(empleado.nombre);
    setDepartamentoEditado(empleado.departamento);
    setSalarioEditado(String(empleado.salario));
    setMensajeEdicion("");
  }

  // PUT: actualizar empleado
  async function actualizarEmpleado(evento) {
    evento.preventDefault();

    setMensajeEdicion("");
    setError("");

    try {
      const empleado = {
        nombre: nombreEditado,
        departamento: departamentoEditado,
        salario: Number(salarioEditado),
      };

      await actualizarEmpleadoAPI(token, empleadoId, empleado);

      setMensajeEdicion("Empleado actualizado correctamente.");

      await cargarEmpleados(token);
    } catch (err) {
      setMensajeEdicion(`Error: ${err.message}`);
    }
  }

  // DELETE: eliminar empleado
  async function eliminarEmpleado(id) {
    const confirmar = window.confirm(
      `¿Seguro que deseas eliminar al empleado con ID ${id}?`,
    );

    if (!confirmar) {
      return;
    }

    setMensajeEliminacion("");
    setError("");

    try {
      await eliminarEmpleadoAPI(token, id);

      setMensajeEliminacion("Empleado eliminado correctamente.");

      await cargarEmpleados(token);
    } catch (err) {
      setMensajeEliminacion(`No se pudo eliminar el empleado: ${err.message}`);
    }
  }

  // LOGOUT: cerrar sesión
  function cerrarSesion() {
    localStorage.removeItem("token");

    setToken("");
    setLogueado(false);
    setEmpleados([]);
    setError("");

    setEmail("");
    setPassword("");

    setMensajeRegistro("");
    setMensajeEdicion("");
    setMensajeEliminacion("");
  }

  // Pantalla de inicio de sesión
  if (!logueado) {
    return (
      <main>
        <h1>FerzanBusinessHub</h1>
        <h2>Iniciar sesión</h2>

        <form onSubmit={iniciarSesion}>
          <div>
            <label htmlFor="email">Correo electrónico</label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(evento) => setEmail(evento.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="password">Contraseña</label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(evento) => setPassword(evento.target.value)}
              required
            />
          </div>

          <button type="submit">Entrar</button>
        </form>

        {error && <p role="alert">{error}</p>}
      </main>
    );
  }

  // Pantalla principal
  return (
    <main>
      <h1>FerzanBusinessHub</h1>

      <button type="button" onClick={cerrarSesion}>
        Cerrar sesión
      </button>

      <hr />

      <EmployeeForm
        nuevoId={nuevoId}
        setNuevoId={setNuevoId}
        nuevoNombre={nuevoNombre}
        setNuevoNombre={setNuevoNombre}
        nuevoDepartamento={nuevoDepartamento}
        setNuevoDepartamento={setNuevoDepartamento}
        nuevoSalario={nuevoSalario}
        setNuevoSalario={setNuevoSalario}
        registrarEmpleado={registrarEmpleado}
      />

      {mensajeRegistro && <p role="status">{mensajeRegistro}</p>}

      <EmployeeEditForm
        empleadoId={empleadoId}
        nombreEditado={nombreEditado}
        setNombreEditado={setNombreEditado}
        departamentoEditado={departamentoEditado}
        setDepartamentoEditado={setDepartamentoEditado}
        salarioEditado={salarioEditado}
        setSalarioEditado={setSalarioEditado}
        actualizarEmpleado={actualizarEmpleado}
      />

      {mensajeEdicion && <p role="status">{mensajeEdicion}</p>}

      <EmployeeTable
        empleados={empleados}
        cargando={cargando}
        error={error}
        mensajeEliminacion={mensajeEliminacion}
        seleccionarEmpleado={seleccionarEmpleado}
        eliminarEmpleado={eliminarEmpleado}
      />
    </main>
  );
}

export default App;
