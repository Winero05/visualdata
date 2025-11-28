const main_index_html = document.getElementById("main_index_html");

const dashboard = document.getElementById("dashboard");

const open_dashboard_contener = document.getElementById("open_dashboard_contener");

const chargement_de_fichier_contener = document.getElementsByClassName("chargement_de_fichier_contener")[0];

const box_modal = document.getElementsByClassName("box_modal")[0];

const myPopUp = document.getElementsByClassName("myPopUp")[0];

const closePopUp = document.getElementsByClassName("closePopUp")[0];

const type_de_visualisation = document.getElementById("type_de_visualisation");

const infos_data = document.getElementsByClassName("infos_data")[0];

const contener = document.getElementById("contener");

const endpoint = "http://127.0.0.1:8000/v_01/reduction";

const endpoint_data_loading = "http://127.0.0.1:8000/v_01/data_1";

headers = { "accept": "application/json" };

const btn_path_file = document.getElementsByClassName("btn_path_file")[0];

const plot = document.getElementById("plot");

const reduction_methode_options = document.getElementById(
    "reduction_methode_options"
);

const visual_contener = document.getElementsByClassName("visual_contener");

const visual_2d = document.getElementsByClassName("visual_2d");

const visual_3d = document.getElementsByClassName("visual_3d");

const lecteur = new FileReader();

// ------------------------------ open_close_dashbord_contener ---------------------------------

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

// ------------------------------ box_modal ---------------------------------

closePopUp.addEventListener("click", (event) => {
    box_modal.style.display = "none";
})

btn_path_file.addEventListener("click", () => {
    box_modal.style.display = "flex"; 
    // lecteur.onload = function (event) {
    //     plot.textContent = event.target.result;
    //     afficherCSV(event.target.result);
    // };
    // lecteur.readAsText(path_file.files[0]);
    infos_data.style.cursor = "pointer";
    infos_data.style.opacity = "1";
    infos_data.removeAttribute("disabled");
    // visual_contener[0].style.opacity = "1";
    reduction_methode_options.removeAttribute("disabled");
    // visual_2d[0].removeAttribute("disabled");
    // visual_3d[0].removeAttribute("disabled");
    reduction_methode_options.style.cursor = "pointer";
    // visual_2d[0].style.cursor = "pointer";
    // visual_3d[0].style.cursor = "pointer";
    reduction_methode_options.addEventListener('click', (event) => {
        console.log(event.target.value);
    })
})

// ---------------------------------------------------------------------------

// ------------------------------ infos_data ---------------------------------

infos_data.addEventListener("click", (event) => {
    const resumer_des_donnees = contener.children[1].classList[0];
    if (resumer_des_donnees === "resumer_des_donnees") {
        contener.children[1].removeAttribute("class");
        contener.children[0].style.height = "88vh";
    } else {
        contener.children[1].classList.toggle("resumer_des_donnees");
        contener.children[0].style.height = "61vh"
    }
});

// ---------------------------------------------------------------------------------------------

function afficherCSV(csvText) {
    const lignes = csvText.trim().split("\n");
    const tableau = document.createElement("table");

    lignes.forEach((ligne, index) => {
    const ligneHTML = document.createElement("tr");
    const cellules = ligne.split(",");

    cellules.forEach((cellule) => {
        const celluleHTML = document.createElement(index === 0 ? "th" : "td");
        celluleHTML.textContent = cellule.trim();
        ligneHTML.appendChild(celluleHTML);
    });

    tableau.appendChild(ligneHTML);
    });

    plot.innerHTML = ""; // Nettoyer si on recharge un fichier
    plot.appendChild(tableau);
}

// console.log(myPopUp[0]);

if (!myPopUp) {
    console.warn("Element with class 'myPopUp' not found.");
} else {
    myPopUp.addEventListener('submit', (event) => {
        event.preventDefault();
        const url_or_filePath = event.target[0].value;
        const ishttp = url_or_filePath.split(":")[0]
        if ((ishttp === "http") || (ishttp+"s" === "https")) {
            fetch(url_or_filePath)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    console.log(response.blob());
                    return response.blob();
            })
        } else {
            console.log("Le chemin entré est différent des options proposées.");
            url_or_filePath = "http://127.0.0.1:8000/" + url_or_filePath + ":path";
            fetch(url_or_filePath)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                console.log(response.blob());
                return response.blob();
        })
        }
        // console.log(http)
        // console.log(url_or_filePath)
    });
}


function afficherResumerDesDonnees(params) {
    const resumer_des_donnees = document.getElementsByClassName(
        "resumer_des_donnees"
    )[0];
    const tableau = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const tr_titre = document.createElement("tr");
    const tr_data = document.createElement("tr");
    const celluleHTML = document.createElement("td");
    ligneHTML.appendChild(celluleHTML); // tr(ligne) <- td(cellule)
    thead.appendChild(ligneHTML); // thead(en-tête de tableau) <- tr
    tbody.appendChild(ligneHTML); // tbody(corps de tableau)
    tableau.appendChild(thead);
    tableau.appendChild(tbody);
    const title = ["Taille", "Valeur manquante", "Valeur dupliqué", "Types des colonne", "Colonnes"]
    for (let index = 0; index < title.length; index++) {
        const th = document.createElement("th");
        const celluleHTML = document.createElement("td");
        th.textContent = title[index] // th(cellule en-tête) <- title[index]
        celluleHTML.textContent = 
        tr_titre.appendChild(th); // tr(ligne) <- th(en-tête)
        tr_data.appendChild(celluleHTML);
    }
    resumer_des_donnees.appendChild(tableau);
}