document.addEventListener('DOMContentLoaded', function () {
    const url = window.location.href;
    const sidebar = document.querySelector('#nav-sidebar');
    if (sidebar) {
        sidebar.style.display = 'none'; // Oculta el menú lateral
    }

    const sidebar_row = document.querySelector('#toggle-nav-sidebar');
    if (sidebar_row) {
        sidebar_row.style.display = 'none'; // Oculta el menú lateral
    }

    const mainElement = document.querySelector('#main');
    if (mainElement) {
        mainElement.classList.remove('shifted');
    }
});
