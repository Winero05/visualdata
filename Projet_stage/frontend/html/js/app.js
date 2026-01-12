import { initDashboardEvents } from "./events/dashboardEvents.js";
import { initFormEvents } from "./events/formEvents.js";
import { initUserCompteIcon } from "./events/userCompteEvents.js";
import { initInfoEvents } from "./events/infoEvents.js";

// Initialisation

function init() {
    initDashboardEvents();
    initFormEvents();
    initUserCompteIcon();
    initInfoEvents();
}
document.addEventListener("DOMContentLoaded", init);
