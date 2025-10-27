// Selección de elementos
const toggleBtn = document.getElementById('toggle-btn');
const barra = document.querySelector('.barra_lateral');
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");
const submenuItems = document.querySelectorAll('.menu-item-dropdown');
const iconoCalculadora = document.getElementById("cloud"); // NUEVO

// Submenús desplegables
const subMenus = document.querySelectorAll('.menu-item-dropdown');

subMenus.forEach((menuItem) => {
  const link = menuItem.querySelector('a');
  const subMenu = menuItem.querySelector('.sub-menu');

  link.addEventListener('click', (e) => {
    e.preventDefault(); 
    const isActive = menuItem.classList.toggle('sub-menu-toggle');

    if (isActive) {
      subMenu.style.height = subMenu.scrollHeight + "px";
      subMenu.style.padding = "0.2rem 0";
    } else {
      subMenu.style.height = "0";
      subMenu.style.padding = "0";
    }
  });
});

// Menú móvil - botón de las tres barritas
menu.addEventListener("click", () => {
  barra.classList.toggle("max-barra_lateral");

  if (barra.classList.contains("max-barra_lateral")) {
    menu.children[0].style.display = "none";
    menu.children[1].style.display = "block";
  } else {
    menu.children[0].style.display = "block";
    menu.children[1].style.display = "none";
  }

  if (window.innerWidth <= 320) {
    barra.classList.add("mini-barra-lateral");
    main.classList.add("min-main");
    spans.forEach((span) => {
      span.classList.add("oculto");
    });
  }
});

// NUEVO: Menú con el ícono de calculadora
iconoCalculadora.addEventListener("click", () => {
  barra.classList.toggle("mini-barra-lateral");
  toggleBtn.classList.toggle("rotado");
  main.classList.toggle("min-main");

  spans.forEach((span) => {
    span.classList.toggle("oculto");
  });
});
// Palanca de modo oscuro
palanca.addEventListener("click", () => {
  document.body.classList.toggle("modo-oscuro");
  circulo.classList.toggle("prendido");
});

// Minimizar barra lateral con el botón toggle
toggleBtn.addEventListener("click", () => {
  barra.classList.toggle("mini-barra-lateral");
  toggleBtn.classList.toggle("rotado");
  main.classList.toggle("min-main");

  spans.forEach((span) => {
    span.classList.toggle("oculto");
  });
});

// Cargar el estado del modo oscuro desde localStorage
  document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("modoOscuro") === "activado") {
      document.body.classList.add("dark");
    }
  });

  function toggleModoOscuro() {
    document.body.classList.toggle("dark");
    const estado = document.body.classList.contains("dark") ? "activado" : "desactivado";
    localStorage.setItem("modoOscuro", estado);
  }