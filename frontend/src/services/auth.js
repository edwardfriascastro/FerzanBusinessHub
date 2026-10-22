import { API_URL } from "../config/api";
// Iniciar sesión mediante el backend
export async function iniciarSesionAPI(email, password) {
  const respuesta = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

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

  if (!datos?.access_token) {
    throw new Error("El backend no devolvió un token de acceso.");
  }

  return datos;
}
