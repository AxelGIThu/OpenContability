
  document.addEventListener("DOMContentLoaded", () => {
    // Si en localStorage está activado, aplicamos la clase EXACTA que usa tu CSS
    if (localStorage.getItem("modoOscuro") === "activado") {
      document.body.classList.add("modo-oscuro");
      // marcar el circulito como prendido si existe
      const circulo = document.querySelector('.circulo');
      if (circulo) circulo.classList.add('prendido');
    }
  });

  function toggleModoOscuro() {
    const esta = document.body.classList.toggle("modo-oscuro");
    // actualizamos el circulito visual
    const circulo = document.querySelector('.circulo');
    if (circulo) circulo.classList.toggle('prendido', esta);

    const estado = esta ? "activado" : "desactivado";
    localStorage.setItem("modoOscuro", estado);
  }



const contenedorBotones = document.getElementById('contenedor-botones');
const contenedorToast = document.getElementById('contenedor-toast');

// Event listener para detectar click en los botones
if (contenedorBotones) {
	contenedorBotones.addEventListener('click', (e) => {
		e.preventDefault();
		const tipo = e.target.dataset.tipo;
		if (tipo === 'exito') {
			agregarToast({ tipo: 'exito', titulo: 'Éxito!', descripcion: 'La operación fue exitosa.', autoCierre: true });
		}
		if (tipo === 'error') {
			agregarToast({ tipo: 'error', titulo: 'Error', descripcion: 'Hubo un error', autoCierre: true });
		}
		if (tipo === 'info') {
			agregarToast({ tipo: 'info', titulo: 'Info', descripcion: 'Esta es una notificación informativa.' });
		}
		if (tipo === 'warning') {
			agregarToast({ tipo: 'warning', titulo: 'Advertencia', descripcion: 'Ten cuidado' });
		}
	});
}

// Función para cerrar el toast (animación de salida)
function cerrarToastManual(botonCerrar) {
	const toast = botonCerrar.closest('.toast');
	toast.classList.add('cerrando');
	toast.addEventListener('animationend', () => toast.remove());
}

// Escucha para cierre por botón (delegación)
contenedorToast.addEventListener('click', (e) => {
	if (e.target.closest('.btn-cerrar')) {
		cerrarToastManual(e.target.closest('.btn-cerrar'));
	}
});

// Función para crear el toast
function agregarToast({ tipo, titulo, descripcion, autoCierre }) {
	const nuevoToast = document.createElement('div');
	const id = 'toast-' + Date.now();

	nuevoToast.classList.add('toast', tipo);
	if (autoCierre) nuevoToast.classList.add('autoCierre');
	nuevoToast.id = id;

	const icono = {
		exito: "✅", error: "❌", info: "ℹ️", warning: "⚠️"
	}[tipo] || "🔔";

	nuevoToast.innerHTML = `
		<div class="contenido">
			<div class="icono">${icono}</div>
			<div class="texto">
				<p class="titulo">${titulo}</p>
				<p class="descripcion">${descripcion}</p>
			</div>
		</div>
		<button class="btn-cerrar"><span class="icono">✖</span></button>
	`;

	contenedorToast.appendChild(nuevoToast);

	if (autoCierre) {
		setTimeout(() => {
			nuevoToast.classList.add('cerrando');
			nuevoToast.addEventListener('animationend', () => nuevoToast.remove());
		}, 5000);
	}
}
const contenedorBotones = document.getElementById('contenedor-botones');
const contenedorToast = document.getElementById('contenedor-toast');

// Event listener para detectar click en los botones
if (contenedorBotones) {
    contenedorBotones.addEventListener('click', (e) => {
        e.preventDefault();
        const tipo = e.target.dataset.tipo;
        if (tipo === 'exito') {
            agregarToast({ tipo: 'exito', titulo: 'Éxito!', descripcion: 'La operación fue exitosa.', autoCierre: true });
        }
        if (tipo === 'error') {
            agregarToast({ tipo: 'error', titulo: 'Error', descripcion: 'Hubo un error', autoCierre: true });
        }
        if (tipo === 'info') {
            agregarToast({ tipo: 'info', titulo: 'Info', descripcion: 'Esta es una notificación informativa.' });
        }
        if (tipo === 'warning') {
            agregarToast({ tipo: 'warning', titulo: 'Advertencia', descripcion: 'Ten cuidado' });
        }
    });
}

// Función para cerrar el toast (animación de salida)
function cerrarToastManual(botonCerrar) {
    const toast = botonCerrar.closest('.toast');
    toast.classList.add('cerrando');
    toast.addEventListener('animationend', () => toast.remove());
}