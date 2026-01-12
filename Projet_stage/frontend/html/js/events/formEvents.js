import { constants } from "../configs/constants.js";
import { showLoader, hideLoader } from "../utils/loaderUtils.js";
import {
    readLoadedData,
    readDataAnalysis,
    readVisualization_2d} from "../api/apiHandlers.js";

export function initFormEvents() {
    /**
     * Ce évènement permet d'affichager le box-modal qui permet de recevoir
     * le chemin d'un fichier de données à lire.
     */
    function lireCheminData() {
        constants.box_modal.style.display = "flex";
    }
    // constants.btn_path_file.addEventListener("click", lireCheminData);
    constants.charge_data_message.addEventListener("click", lireCheminData);

    /**
     * Cette fonction permet de charger les données via la lecture d'un des
     * données.
     * 
     * @param {*} event 
     */
    async function chargement_data(event) {
        event.preventDefault();

        await showLoader();

        constants.box_modal.style.display = "none";

        try {
            const response = await fetch(constants.data_loading, {
                method: "POST",
                headers: constants.headers,
                body: JSON.stringify({
                    file_path: constants.url_or_filePath.value,
                }),
            });

            if (!response.ok)
                throw new Error(`HTTP error! Status: ${response.status}`);

            await response.json();

            await Promise.all([
                // Lire les données.
                readLoadedData(),
                // Lire l’analyse des données.
                readDataAnalysis(),
            ]);

            constants.infos_data.removeAttribute("disabled");
            constants.infos_data.style.cursor = "pointer";
            constants.infos_data.style.opacity = "1";
            constants.info_items.style.display = "flex";
            constants.info_items.style.width = "100%";
            constants.info_items.style.flexDirection = "column";
            constants.type_de_visualisation.removeAttribute("disabled");
            constants.type_de_visualisation.style.cursor = "pointer";
            constants.type_de_visualisation.style.opacity = "1";
        } catch (error) {
            console.error(error);
        } finally {
            hideLoader();
        }
            constants.url_or_filePath.value = "";
            event.stopPropagation();
    }

    constants.myPopUp.addEventListener("submit", chargement_data);

    /**
     * Fermetture du modal-box qui permet la reception du chemin
     * de chargement des données.
     */
    constants.closePopUp.addEventListener("click", () => {
        constants.box_modal.style.display = "none";
    });

    /**
     * 
     * @param {*} event 
     */
    function num_colonne(event) {
        event.preventDefault();
        const viz_col = new Object();
        const num_col_items = document.getElementsByClassName("num-col-items");
        for (let i = 0; i < num_col_items.length; i++) {
            const label = num_col_items[i].children[0].textContent;
            const selected = num_col_items[i].children[1].checked;
            if (selected) viz_col[label] = String(selected);
        }

        const objet_vide = Object.keys(viz_col).length === 0;
        const une_seule_colonne = Object.keys(viz_col).length === 1;

        if (objet_vide || une_seule_colonne) {
            if (une_seule_colonne) delete viz_col[Object.keys(viz_col)[0]];
            alert(`Veuillez sélectionné au moin deux colonnes.`);
        } else {
            Object.assign(constants.visualize_column, viz_col);
            constants.visualisation_box_modal.style.display = "flex";
        }
        event.stopPropagation();

    }

    constants.numerique_col.addEventListener("submit", num_colonne);

    /**
     * 
     * @param {*} event 
     */
    async function visualisation_num_colonne(event) {
        event.preventDefault();

        await showLoader();

        constants.visualisation_box_modal.style.display = "none";

        try {
            const response = await fetch(constants.visualisation2d, {
                method: "POST",
                headers: constants.headers,
                body: JSON.stringify({
                    folder_path: constants.filePath.value,
                    visualize_column: constants.visualize_column,
                }),
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const data = await response.json();

            console.log(data);

            // Lire la visualisation 2D

            await Promise.all([
            // Lire la vue graphique.
            readVisualization_2d(),
            ]);
        } catch (error) {
            console.error(`Error of graphic loading: ${error}`);
        } finally {
            hideLoader();
        }

        // fetch(visualisation3d, {
        //     method: "POST",
        //     headers: headers,
        //     body: JSON.stringify({
        //         folder_path: filePath.value,
        //         visualize_column: visualize_column,
        //     })
        // }).then((response) => {
        //     if (!response.ok) {
        //         throw new Error(`HTTP error! Status: ${response.status}`);
        //     }
        //     return response.json();
        // }).then(() => {
        //     console.log("Création OK");

        //     // Lire la visualisation 2D
        //     readVisualization_3d();

        //     visualisation_box_modal.style.display = "none";
        //     // event.stopPropagation();
        // }).catch(console.error);

        constants.filePath.value = "";
        event.stopPropagation();

        // visualisation_box_modal.style.display = "none";
    }

    constants.form_visualisation.addEventListener("submit", visualisation_num_colonne);
}