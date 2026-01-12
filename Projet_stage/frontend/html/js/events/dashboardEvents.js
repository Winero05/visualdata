import { constants } from "../configs/constants.js";

// --------------------- open_close_dashbord_contener ----------------

/**
 * Cette fonction permet d'ouvrir et de fermet le dashboard.
 */
export function initDashboardEvents() {
    if (constants.close_dashboard) {
        constants.dashboard.removeAttribute("class");
        constants.resize_dashboard.style.display = "none";
        constants.dashboard.classList.toggle("dashboard_close");
        constants.dashboard.style.width = "var(--width-dashboard-reduit)";
        constants.chargement_de_fichier_contener.style.display = "none";
        constants.type_de_visualisation.style.display = "none";
        constants.infos_data.style.display = "none";
        constants.infos_data.style.display = "none";
        constants.contener.style.width = "96.6%";
        constants.open_dashboard_contener.children[0].style.top = "0";
        constants.open_dashboard_contener.children[0].style.rotate = "0 0 0 0rad";
        constants.open_dashboard_contener.children[1].style.display = "block";
        constants.open_dashboard_contener.children[2].style.top = "0";
        constants.open_dashboard_contener.children[2].style.rotate = "0 0 0 0deg";
        constants.close_dashboard = false;
    } else {
        constants.dashboard.removeAttribute("class");
        constants.resize_dashboard.style.display = "flex";
        constants.dashboard.classList.toggle("dashboard_open");
        constants.dashboard.style.width = "var(--width-dashboard)";
        constants.chargement_de_fichier_contener.style.display = "flex";
        constants.type_de_visualisation.style.display = "flex";
        constants.infos_data.style.display = "flex";
        constants.infos_data.style.display = "flex";
        constants.contener.style.width = "80%";
        constants.open_dashboard_contener.children[0].style.top = "5px";
        constants.open_dashboard_contener.children[0].style.rotate = "4 0 4 63deg";
        constants.open_dashboard_contener.children[1].style.display = "none";
        constants.open_dashboard_contener.children[2].style.top = "-6.1px";
        constants.open_dashboard_contener.children[2].style.left = "1px";
        constants.open_dashboard_contener.children[2].style.rotate = "4 0 5 -56deg";
        constants.close_dashboard = true;
    }
}

// Contrôle de l'ouverture et de la fermetture du dashboard.
constants.open_dashboard_contener.addEventListener("click", initDashboardEvents);
