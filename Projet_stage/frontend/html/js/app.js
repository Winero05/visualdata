// document.querySelector("html").classList.add("js");

const main_index_html = document.getElementById("main_index_html");

const dashboard = document.getElementById("dashboard");

const open_dashboard_contener = document.getElementById("open_dashboard_contener");

const chargement_de_fichier_contener = document.getElementsByClassName("chargement_de_fichier_contener")[0];

const closePopUp = document.getElementsByClassName("closePopUp")[0];

const visuale_closePopUp = document.getElementsByClassName("visuale-closePopUp")[0];

const box_modal = document.getElementsByClassName("box_modal")[0];

const myPopUp = document.getElementsByClassName("myPopUp")[0];

const visualisation_box_modal = document.getElementsByClassName("visualisation-box-modal")[0];

const url_or_filePath = document.getElementById("url_or_filePath");

const filePath = document.getElementById("filePath");

const type_de_visualisation = document.getElementById("type_de_visualisation");

const infos_data = document.getElementsByClassName("infos_data")[0];

const infos_msg = document.getElementsByClassName("info-msg")[0];

const info_items = document.getElementsByClassName("info-items")[0];

const info_items_icon = document.getElementsByClassName("info-items-icon")[0];

const up_icon_svg = document.getElementById("up-icon-svg");

const contener = document.getElementById("contener");

const resumer_des_donnees = document.getElementsByClassName("resumer_des_donnees")[0];

const all_infos_on_data = document.getElementsByClassName("all-infos-on-data")[0];

const single_info_on_data = document.getElementsByClassName("single-info-on-data")[0];

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

open_dashboard_contener.addEventListener("click", (event) => {
    class_attributs_of_dashboard = dashboard.classList[0];
    if (close_dashboard) {
        if (class_attributs_of_dashboard === "open_dashboard") {
            dashboard.removeAttribute("class");
        }
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
        if (class_attributs_of_dashboard === "close_dashboard") {
            dashboard.removeAttribute("class");
        }
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

const visualisation2d = "http://127.0.0.1:8000/v_01/visualisation_2d/";

const visualisation3d = "http://127.0.0.1:8000/v_01/visualisation_3d/";

const headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
};

// -------------------------------------------------------------------

const lecteur = new FileReader();

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
    resumer_des_donnees.innerHTML = "";

    const table = document.createElement("table");

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
    resumer_des_donnees.appendChild(table);
}

function afficherGraphique2D(graphique) {
    
}

// ---------------------------------------------------------------------------------------------

function readLoadedData() {
    fetch(data_loading, {
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
        // Affichage dans le HTML
        afficherCSVDepuisObjet(data);
    })
    .catch((err) => console.error("Erreur GET /data :", err));
}

function readDataAnalysis() {
    fetch(data_analysis, {
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
        console.log("Résumé des données : ", data);

        afficherResumeDansTableau(data);
    })
    .catch((err) => console.error("Erreur GET /analyse :", err));
}

function readVisualization_2d() {
    fetch(visualisation2d, {
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
}

myPopUp.addEventListener('submit', (event) => {
    event.preventDefault();
    fetch(data_loading, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            file_path: url_or_filePath.value
        })
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    }).then((data) => {
        console.log("Création OK");
        
        // Lire les données
        readLoadedData();
        
        // Lire l’analyse
        readDataAnalysis();
        event.stopPropagation();
    }).catch(console.error);
    infos_data.removeAttribute("disabled");
    infos_data.style.cursor = "pointer";
    infos_data.style.opacity = "1";
    info_items.style.display = "flex";
    info_items.style.width = "100%";
    info_items.style.flexDirection = "column";
});

// ---------------- VISUALISATION -----------------------

type_de_visualisation.addEventListener("click", () => {
    visualisation_box_modal.style.display = "flex";
});

visualisation_box_modal.addEventListener("submit", (event) => {
    event.preventDefault();
    console.log(filePath.value);
    fetch(visualisation2d, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            file_path: filePath.value,
        })
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    }).then(() => {
        console.log("Création OK");

        // Lire la visualisation 2D
        readVisualization_2d();

        event.stopPropagation();
    }).catch(console.error);

});

// ----------- INFORMATIONS DES DONNEES CHARGEES ---------------

infos_msg.addEventListener("click", () => {
    const resumer_des_donnees = contener.children[1].classList[0];
    if (resumer_des_donnees === "resumer_des_donnees") {
        contener.children[1].removeAttribute("class");
        contener.children[0].style.height = "88vh";
    } else {
        contener.children[1].classList.toggle("resumer_des_donnees");
        contener.children[0].style.height = "61vh";
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

info_items.addEventListener("click", (event) => {
    const item = event.target.textContent.trim();
    switch (item) {
        case "Taille":
            
            break;
    
        case "Colonnes":
            
            break;
    
        case "Valeur dupliqué":
            
            break;
    
        case "Valeur manquante":
            
            break;
    
        case "Types des colonne":
            
            break;
    
        case "Taille":
            
            break;
    
        default:
            break;
    }
    console.log(item);
})

// ---------------------------------------------------------------------------
