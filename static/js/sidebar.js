document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-btn");
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");

    toggleBtn.addEventListener("click", function () {
        // Detecta si estamos en vista móvil
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle("show"); // Muestra u oculta el sidebar móvil
        } else {
            // Comportamiento normal (modo escritorio)
            sidebar.classList.toggle("collapsed");
            main.classList.toggle("collapsed");
        }
    });
});
