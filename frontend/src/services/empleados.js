import { API_URL } from "../config/api";
// Función común para enviar solicitudes HTTP
async function solicitar(endpoint, token, opciones = {}) {
  const respuesta = await fetch(`${API_URL}${endpoint}`, {
    ...opciones,
    headers: {
      ...(opciones.body ? { "Content-Type": "application/json" } : {}),
      ...(opciones.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  // Algunas respuestas HTTP no tienen contenido
  const texto = await respuesta.text();
  let datos = null;

  if (texto) {
    try {
      datos = JSON.parse(texto);
    } catch {
      datos = texto;
    }
  }

  if (!respuesta.ok) {
    const mensaje =
      typeof datos === "object" && datos !== null
        ? datos.detail || `Error HTTP ${respuesta.status}`
        : datos || `Error HTTP ${respuesta.status}`;

    throw new Error(mensaje);
  }

  return datos;
}

// GET: consultar empleados
export function obtenerEmpleados(token) {
  return solicitar("/empleados", token);
}

// POST: registrar empleado
export function crearEmpleado(token, empleado) {
  return solicitar("/empleados", token, {
    method: "POST",
    body: JSON.stringify(empleado),
  });
}

// PUT: actualizar empleado
export function actualizarEmpleadoAPI(token, id, empleado) {
  return solicitar(`/empleados/${id}`, token, {
    method: "PUT",
    body: JSON.stringify(empleado),
  });
}

// DELETE: eliminar empleado
export function eliminarEmpleadoAPI(token, id) {
  return solicitar(`/empleados/${id}`, token, {
    method: "DELETE",
  });
}
