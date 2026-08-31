/* =========================================================
   NAIJACART — ADMIN DASHBOARD
========================================================= */

function toggleSidebar() {

    const sidebar =
        document.getElementById("sidebar");

    if (!sidebar) {
        return;
    }

    sidebar.classList.toggle("open");

}