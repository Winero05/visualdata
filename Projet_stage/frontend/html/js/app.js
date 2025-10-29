const endpoint = "http://127.0.0.1:8000/v_01/reduction";

const endpoint_data_loading = "http://127.0.0.1:8000/v_01/data_1";

headers = { "accept": "application/json" };

const btn_path_file = document.getElementsByClassName("btn_path_file")[0];

const box_modal = document.getElementsByClassName("box_modal")[0];

const plot = document.getElementById("plot");

const reduction_methode_options = document.getElementById(
  "reduction_methode_options"
);

const visual_contener = document.getElementsByClassName("visual_contener");

const visual_2d = document.getElementsByClassName("visual_2d");

const visual_3d = document.getElementsByClassName("visual_3d");

const lecteur = new FileReader();

btn_path_file.addEventListener("click", () => {
    box_modal.style.display = "flex"; 
    // lecteur.onload = function (event) {
    //     plot.textContent = event.target.result;
    //     afficherCSV(event.target.result);
    // };
    // lecteur.readAsText(path_file.files[0]);
    visual_contener[0].style.opacity = 1;
    reduction_methode_options.removeAttribute("disabled");
    visual_2d[0].removeAttribute("disabled");
    visual_3d[0].removeAttribute("disabled");
    reduction_methode_options.style.cursor = "pointer";
    visual_2d[0].style.cursor = "pointer";
    visual_3d[0].style.cursor = "pointer";
    reduction_methode_options.addEventListener('click', (event) => {
        console.log(event.target.value);
    })
})

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

const myPopUp = document.getElementsByClassName("myPopUp")[0];

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