// document.querySelector("html").classList.add("js");
// import { initDashboardEvents } from "./events/dashboardEvents.js";
// import { initFormEvents } from "./events/formEvents.js";
// import { initInfoEvents } from "./config/infoEvents.js";
// import { constants } from "./configs/constants.js";

// // Initialisation
// document.addEventListener("DOMContentLoaded", () => {
//     initDashboardEvents();
//     initFormEvents();
//     initInfoEvents();
//     constants()
// });

const main_index_html = document.getElementById("main_index_html");

const dashboard = document.getElementById("dashboard");

const open_dashboard_contener = document.getElementById("open_dashboard_contener");

const chargement_de_fichier_contener = document.getElementsByClassName("chargement_de_fichier_contener")[0];

const closePopUp = document.getElementsByClassName("closePopUp")[0];

const visuale_closePopUp = document.getElementsByClassName("visuale-closePopUp")[0];

const box_modal = document.getElementsByClassName("box_modal")[0];

const myPopUp = document.getElementsByClassName("myPopUp")[0];

const visualisation_box_modal = document.getElementsByClassName("visualisation-box-modal")[0];

const form_visualisation = document.getElementsByClassName("form-visualisation")[0];

const url_or_filePath = document.getElementById("url_or_filePath");

const filePath = document.getElementById("filePath");

const type_de_visualisation = document.getElementById("type_de_visualisation");

const infos_data = document.getElementsByClassName("infos_data")[0];

const infos_msg = document.getElementsByClassName("info-msg")[0];

const info_items = document.getElementsByClassName("info-items")[0];

const info_items_icon = document.getElementsByClassName("info-items-icon")[0];

const up_icon_svg = document.getElementById("up-icon-svg");

const resize_dashboard = document.getElementsByClassName("resize-dashboard")[0];

const contener = document.getElementById("contener");

const resize_plot = document.getElementsByClassName("resize-plot")[0];

const resumer_des_donnees = document.getElementsByClassName("resumer_des_donnees")[0];

const all_infos_on_data = document.getElementsByClassName("all-infos-on-data")[0];

const single_info_on_data = document.getElementsByClassName("single-info-on-data")[0];

const numerique_col = document.getElementsByClassName("numerique_col")[0];

const charge_data_message = document.getElementsByClassName("charge-data-message")[0];

const iframe_contener = document.getElementsByClassName("iframe_contener")[0];

const btn_path_file = document.getElementsByClassName("btn_path_file")[0];

const plot = document.getElementById("plot");

const reduction_methode_options = document.getElementById(
    "reduction_methode_options"
);

const visual_contener = document.getElementsByClassName("visual_contener");

const visual_2d = document.getElementsByClassName("visual_2d");

const visual_3d = document.getElementsByClassName("visual_3d");

// --------------------- open_close_dashbord_contener ----------------

let close_dashboard = true;

open_dashboard_contener.addEventListener("click", () => {
    class_attributs_of_dashboard = dashboard.classList[0];
    if (close_dashboard) {
        if (class_attributs_of_dashboard === "open_dashboard")
            dashboard.removeAttribute("class");

        resize_dashboard.style.display = "none";
        dashboard.classList.toggle("close_dashboard");
        dashboard.style.width = "var(--width-dashboard-reduit)";
        chargement_de_fichier_contener.style.display = "none";
        type_de_visualisation.style.display = "none";
        infos_data.style.display = "none";
        infos_data.style.display = "none";
        contener.style.width="96.6%";
        open_dashboard_contener.children[0].style.top="0";
        open_dashboard_contener.children[0].style.rotate="0 0 0 0rad";
        open_dashboard_contener.children[1].style.display="block";
        open_dashboard_contener.children[2].style.top="0";
        open_dashboard_contener.children[2].style.rotate="0 0 0 0deg";
        close_dashboard = false;
    } else {
        if (class_attributs_of_dashboard === "close_dashboard")
            dashboard.removeAttribute("class");

        resize_dashboard.style.display = "flex";
        dashboard.classList.toggle("open_dashboard");
        dashboard.style.width="var(--width-dashboard)";
        chargement_de_fichier_contener.style.display="flex";
        type_de_visualisation.style.display="flex";
        infos_data.style.display="flex";
        infos_data.style.display="flex";
        contener.style.width="80%";
        open_dashboard_contener.children[0].style.top="5px";
        open_dashboard_contener.children[0].style.rotate="4 0 4 63deg";
        open_dashboard_contener.children[1].style.display="none";
        open_dashboard_contener.children[2].style.top="-6.1px";
        open_dashboard_contener.children[2].style.left="1px";
        open_dashboard_contener.children[2].style.rotate="4 0 5 -56deg";
        close_dashboard = true;
    }
});
// ---------------------------------------------------------------------------------------------

// -------- ANIMATION DE CHARGEMENT -------------

async function showLoader() {
    const container = ensureLoaderContainer();

    if (!document.getElementById("loader")) {
        const response = await fetch(
            "http://127.0.0.1:5501/Projet_stage/frontend/html/modal-loading.html"
        );
        container.innerHTML = await response.text();
    } else console.log("Bigo...");

    document.getElementById("loader").style.display = "flex";
}

function hideLoader() {
    const container = document.getElementById("loader-container");
    // if (container) {
    //     container.innerHTML = "";
    // }
    const loader = document.getElementById("loader");
    container.removeChild(loader);
    container.style.display = "none";
}

function ensureLoaderContainer() {
    let container = document.getElementById("loader-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "loader-container";
        document.body.appendChild(container);
    }
    return container;
}


// ---------------------------------------------------------------------------------------------

// ----------------- AFFICHAGE DE BOX_MODAL ---------------------

closePopUp.addEventListener("click", () => {
    box_modal.style.display = "none";
});

visuale_closePopUp.addEventListener("click", () => {
    visualisation_box_modal.style.display = "none";
});

btn_path_file.addEventListener("click", () => {
    box_modal.style.display = "flex";
});

charge_data_message.addEventListener("click", () => {
    box_modal.style.display = "flex";
});

// Interaction avec l'API
const data_loading = "http://127.0.0.1:8000/v_01/data/";

const data_analysis = "http://127.0.0.1:8000/v_01/analyse/";

const visualisation2d = "http://127.0.0.1:8000/v_01/visualisation/2d/";

const visualisation3d = "http://127.0.0.1:8000/v_01/visualisation/3d/";

const headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
};

// -------------------------------------------------------------------

function afficherCSVDepuisObjet(dataArray) {
    const table = document.createElement("table");

    // Création de l'en-tête
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    const colonnes = Object.keys(dataArray[0]);
    colonnes.forEach((col) => {
        const th = document.createElement("th");
        th.textContent = col;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Corps du tableau
    const tbody = document.createElement("tbody");

    dataArray.forEach((rowData) => {
        const tr = document.createElement("tr");
        colonnes.forEach((col) => {
            const td = document.createElement("td");
            td.textContent = rowData[col];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);

    // Affichage
    plot.innerHTML = "";
    plot.appendChild(table);
}

function afficherResumeDansTableau(resume) {
    all_infos_on_data.style.display = "flex";
    all_infos_on_data.innerHTML = "";

    const table = document.createElement("table");
    table.setAttribute("class", "table-infos-data");

    const tbody = document.createElement("tbody");

    let index = 0;
    for (const key in resume) {
        const tr = document.createElement("tr");

        const tdKey = document.createElement("td");
        tdKey.textContent = key;

        const tdValue = document.createElement("td");
        tdValue.textContent = JSON.stringify(resume[key], null, 2);

        info_items.children[index].children[0].textContent = resume[key].length;

        if (resume[key].length)
            info_items.children[index].children[0].textContent = resume[key].length;
        else if(typeof resume[key] === "number")
            info_items.children[index].children[0].textContent = resume[key];
        else
            info_items.children[index].children[0].textContent = Object.keys(resume[key]).length;

        tr.appendChild(tdKey);
        tr.appendChild(tdValue);
        tbody.appendChild(tr);
        index += 1;
    }

    table.appendChild(tbody);
    all_infos_on_data.appendChild(table);
}

async function afficherGraphique2D(graphique_path) {
    plot.innerHTML = "";
    // iframe_contener.innerHTML = "";
    iframe_contener.style.display = "flex";
    // iframe_contener.removeAttribute("src");
    console.log(graphique_path);
    console.log(iframe_contener);
    // iframe_contener.classList[0].setAttribute("src", graphique_path)
}

// ---------------------------------------------------------------------------------------------

async function readLoadedData() {
    const response = await fetch(data_loading, {
        method: "GET",
        headers: headers,
    });

    if (!response.ok) {
        throw new Error("Erreur HTTP " + response.status);
    }

    const data = await response.json();

    // Affichage dans le HTML
    afficherCSVDepuisObjet(data);

    return data;
}

let analysis_data = new Object();

async function readDataAnalysis() {
    const response = await fetch(data_analysis, {
        method: "GET",
        headers: {
            Accept: "application/json",
        },
    });

    if (!response.ok) {
        throw new Error("Erreur HTTP " + response.status);
    }

    const data = await response.json();

    analysis_data = data;

    afficherResumeDansTableau(data);

    return data;
}

async function readVisualization_2d() {

    const response = await fetch(visualisation2d, {
        method: "GET",
        headers: headers,
    })
    if (!response.ok) {
        throw new Error("Erreur HTTP " + response.status);
    }
    const data = await response.json();
    console.log(data);
    if (data["html_file"]) afficherGraphique2D(data["html_file"]);
    else afficherGraphique2D(data["html_files"][0]);
}

function readVisualization_3d() {

    const data = afficherGraphique3D(data);
    fetch(visualisation3d, {
        method: "GET",
        headers: {
            Accept: "application/json",
        },
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error("Erreur HTTP " + response.status);
        }
        return response.json();
    })
    .then((data) => {
        afficherGraphique2D(data);
    })
}

myPopUp.addEventListener('submit', async (event) => {
    event.preventDefault();

    await showLoader();

    box_modal.style.display = "none";

    try {

        const response = await fetch(data_loading, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                file_path: url_or_filePath.value
            })
        });

        if (!response.ok)
            throw new Error(`HTTP error! Status: ${response.status}`);

        await response.json();

        await Promise.all([
            // Lire les données.
            readLoadedData(),
            // Lire l’analyse des données.
            readDataAnalysis()
        ]);

        infos_data.removeAttribute("disabled");
        infos_data.style.cursor = "pointer";
        infos_data.style.opacity = "1";
        info_items.style.display = "flex";
        info_items.style.width = "100%";
        info_items.style.flexDirection = "column";
        type_de_visualisation.removeAttribute("disabled");
        type_de_visualisation.style.cursor = "pointer";
        type_de_visualisation.style.opacity = "1";

    } catch (error) {
        console.error(error);
    } finally {
        hideLoader();
    }

    url_or_filePath.value = "";
});

// ---------------- VISUALISATION -----------------------

type_de_visualisation.addEventListener("click", () => {
    if (plot.children.length !== 2) {
        numerique_col.innerHTML = "";
        all_infos_on_data.style.display = "none";
        single_info_on_data.style.display = "none";
        numerique_col.style.display = "flex";
        const div = document.createElement("div");
        div.textContent = "Veuillez sélectionner les colonnes numérique à visualiser";
        numerique_col.appendChild(div);
        analysis_data["num_col"].forEach((Element) => {
            const div = document.createElement("div");
            div.setAttribute("class", "num-col-items")
            const label = document.createElement("label");
            const input = document.createElement("input");
            label.setAttribute("for", Element);
            label.textContent = Element
            input.setAttribute("id", Element);
            input.setAttribute("type", "checkbox");
            div.appendChild(label);
            div.appendChild(input);
            numerique_col.appendChild(div);
        });

        // Creation de la boîte d'annulation et d'envoie des
        // colonnes numérique sélectionnées.
        const annulerOuContinuer = document.createElement("div");
        annulerOuContinuer.setAttribute("class", "annuler-continuer");

        // Créer les boutons d'interaction d'annulation
        // et d'envoi.
        const annuler = document.createElement("input");
        const continuer = document.createElement("input");
        const tout_selectionner = document.createElement("input");

        // Fixer les types de chaque input.
        annuler.setAttribute("type", "reset");
        continuer.setAttribute("type", "submit");
        tout_selectionner.setAttribute("type", "button");

        // Fixer les valeurs de chaque input.
        annuler.value = "Rénitialiser";
        continuer.value = "Envoyer";
        tout_selectionner.value = "Tout";

        // Fixer le message à afficher par les lecteurs d'écran.
        annuler.setAttribute("title", "Annuler");
        continuer.setAttribute("title", "Envoyer");
        tout_selectionner.setAttribute("title", "Tout sélectionné");

        // Fixer l'action que doit faire le bouton 'tout_selectioner'.
        // tout_selectionner.setAttribute("onclick", "tout_selectionner()");

        // Ajout de chaque bouton à la boîte d'annulation
        // et d'envoie des colonnes numériques sélectionnées.
        annulerOuContinuer.appendChild(annuler);
        annulerOuContinuer.appendChild(tout_selectionner);
        annulerOuContinuer.appendChild(continuer);

        // Ajout au conteneur d'info des colonnes numériques.
        numerique_col.appendChild(annulerOuContinuer);
        console.log(annulerOuContinuer.childNodes);
    }
});

// Cocher toutes les cases si l'utilisateur sélectionne tout.

// function tout_selectionner() {
    
//     // event.preventDefault();
//     const annulerOuContinuer = document.getElementsByClassName("annuler-continuer");
//     console.log(annulerOuContinuer.childNodes[1]);
    
// }


const tout_selectionner = numerique_col;

const visualize_column = new Object();

numerique_col.addEventListener("submit", (event) => {
    event.preventDefault();
    const viz_col = new Object();
    const num_col_items = document.getElementsByClassName("num-col-items");
    for (let i = 0; i < num_col_items.length; i++) {
        const label = num_col_items[i].children[0].textContent;
        const selected = num_col_items[i].children[1].checked;
        if (selected)
            viz_col[label] = String(selected);
    }

    const objet_vide = Object.keys(viz_col).length === 0;
    const une_seule_colonne = Object.keys(viz_col).length === 1;

    if (objet_vide || une_seule_colonne){
        if (une_seule_colonne)
            delete viz_col[Object.keys(viz_col)[0]];
        alert(`Veuillez sélectionné au moin deux colonnes.`);
    }
    else {
        Object.assign(visualize_column, viz_col);
        visualisation_box_modal.style.display = "flex";
    }
    event.stopPropagation();
});

form_visualisation.addEventListener("submit", async (event) => {
    event.preventDefault();

    await showLoader();

    // visualisation_box_modal.style.display = "none";

    try {
        const response = await fetch(visualisation2d, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                folder_path: filePath.value,
                visualize_column: visualize_column,
            })
        });
    
        if (!response.ok)
            throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();

        console.log(data);

        // Lire la visualisation 2D

        await Promise.all([
            // Lire la vue graphique.
            readVisualization_2d()
        ]);
    } catch (error) {
        console.error(`Error of graphic loading: ${error}`);
    } finally {hideLoader();}

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

    //     // event.stopPropagation();
    // }).catch(console.error);
    
    // visualisation_box_modal.style.display = "none";
    filePath.value = "";
    event.stopPropagation();
    visualisation_box_modal.style.display = "none";

});

// ----------- INFORMATIONS DES DONNEES CHARGEES ---------------

let display = 1;

infos_msg.addEventListener("click", () => {
    if (display) {
        resize_plot.style.display = "none";
        contener.children[0].style.height = "88vh";
        resumer_des_donnees.style.display = "none";
        display = 0;
    } else {
        resize_plot.style.display = "flex";
        contener.children[0].style.height = "61vh";
        resumer_des_donnees.style.display = "flex";
        display = 1;
    }
});

let toggle = 1;

info_items_icon.addEventListener("click", () => {
    if (info_items.style.display === "none") {
        info_items.style.display = "flex";
        info_items.style.width = "100%";
        info_items.style.flexDirection = "column";
        up_icon_svg.style.rotate = "0 0 0 0deg";
        toggle = 0;
    } else {
        up_icon_svg.style.rotate = "5 0 1 180deg";
        info_items.style.display = "none";
        toggle = 1;
    }
});

function afficherUnResumeEnParticulier(donneAnalyse) {
    single_info_on_data.innerHTML = "";
    single_info_on_data.style.display = "flex";

    const table = document.createElement("table");

    // Création de l'en-tête
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    // Corps du tableau
    const tbody = document.createElement("tbody");

    const colonnes = Object.keys(donneAnalyse);
    colonnes.forEach((Element) => {
        const notArray = !donneAnalyse[Element].length;
        const notNumerique = typeof donneAnalyse[Element] !== "number";
        if (notArray) {
            if (notNumerique) {
                const th = document.createElement("th");
                th.textContent = Element;
                headerRow.appendChild(th);
                thead.appendChild(headerRow);
                let newKeys = Object.keys(colonnes);
                newKeys.forEach((Element) => {
                    const tr = document.createElement("tr");
                    const tdValue = document.createElement("td");
                    tdValue.textContent = newKeys[Element];
                    tr.appendChild(tdValue);
                    tbody.appendChild(tr);
                });
            }
        }
    });


    table.appendChild(thead);
    table.appendChild(tbody);
    single_info_on_data.appendChild(table);
}

info_items.addEventListener("click", (event) => {
    afficherUnResumeEnParticulier(analysis_data);
    // const table_infos_data = document.getElementsByClassName("table-infos-data")[0];
    // const tbody = table_infos_data.children[0].children;
    // const item = event.target.className;
    // switch (item) {
    //     case "items-1":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[0].innerHTML;
    //     break;

    //     case "items-2":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[1].innerHTML;
    //     break;

    //     case "items-3":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[2].innerHTML;
    //     break;

    //     case "items-4":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[3].innerHTML;
    //     break;

    //     case "items-5":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[4].innerHTML;
    //     break;

    //     case "items-6":
    //         all_infos_on_data.style.display = "none";
    //         single_info_on_data.style.display = "flex";
    //         single_info_on_data.innerHTML = tbody[5].innerHTML;
    //     break;

    //     case "items-7":
    //         all_infos_on_data.style.display = "flex";
    //         single_info_on_data.style.display = "none";

    //     break;

    //     default:
    //     break;
    // }
});

// ---------------------------------------------------------------------------
