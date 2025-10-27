// notificaciones.js

// Función para mostrar la notificación
function mostrarNotificacion(mensaje, tipo = "info") {
    // Crear contenedor si no existe
    let contenedor = document.getElementById("contenedor-notificaciones");
    if (!contenedor) {
        contenedor = document.createElement("div");
        contenedor.id = "contenedor-notificaciones";
        contenedor.style.position = "fixed";
        contenedor.style.top = "20px";
        contenedor.style.right = "20px";
        contenedor.style.zIndex = "9999";
        contenedor.style.display = "flex";
        contenedor.style.flexDirection = "column";
        contenedor.style.gap = "10px";
        document.body.appendChild(contenedor);
    }

    // Crear notificación
    const notificacion = document.createElement("div");
    notificacion.classList.add("notificacion", tipo);
    notificacion.style.padding = "12px 18px";
    notificacion.style.borderRadius = "8px";
    notificacion.style.boxShadow = "0 4px 6px rgba(0,0,0,0.2)";
    notificacion.style.color = "#fff";
    notificacion.style.display = "flex";
    notificacion.style.justifyContent = "space-between";
    notificacion.style.alignItems = "center";
    notificacion.style.minWidth = "250px";

    // Colores según tipo
    if (tipo === "success") notificacion.style.background = "#28a745";
    else if (tipo === "error") notificacion.style.background = "#dc3545";
    else if (tipo === "warning") notificacion.style.background = "#ffc107", notificacion.style.color = "#000";
    else notificacion.style.background = "#007bff";

    // Texto de la notificación
    const texto = document.createElement("span");
    texto.textContent = mensaje;

    // Botón de cerrar
    const btnCerrar = document.createElement("button");
    btnCerrar.innerHTML = "&times;";
    btnCerrar.style.background = "transparent";
    btnCerrar.style.border = "none";
    btnCerrar.style.color = "inherit";
    btnCerrar.style.fontSize = "18px";
    btnCerrar.style.cursor = "pointer";
    btnCerrar.style.marginLeft = "10px";

    // Evento para cerrar
    btnCerrar.addEventListener("click", () => {
        notificacion.remove();
    });

    // Agregar elementos
    notificacion.appendChild(texto);
    notificacion.appendChild(btnCerrar);
    contenedor.appendChild(notificacion);

    // Cierre automático a los 5 segundos
    setTimeout(() => {
        if (document.body.contains(notificacion)) {
            notificacion.remove();
        }
    }, 5000);
}

// Ejemplo de uso (lo podés borrar después):
// mostrarNotificacion("Bienvenido!", "success");
// mostrarNotificacion("Ocurrió un error!", "error");
