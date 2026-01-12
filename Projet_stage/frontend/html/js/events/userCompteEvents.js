import { constants } from "../configs/constants.js";

/**
 * Cette fonction permet d'ouvrir et de fermer un menu
 * déroulant listant les actions possibles à faire comme
 * voir son profil, paramétrage, changement de thème etc.
 */
export function initUserCompteIcon(event) {
    if (constants.open){
        constants.compte_info.style.display = "flex";
        constants.open = false;
    }
    else {
        constants.compte_info.style.display = "none";
        constants.open = true;
    }
}

// Contrôle de l'ouverture et de la fermetture de l'icône duprofile
// utilisateur.
constants.compte_box.addEventListener("click", initUserCompteIcon);
