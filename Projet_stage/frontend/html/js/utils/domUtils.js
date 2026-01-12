import { constants } from "../configs/constants.js";

/**
 * Cette fonction permet d'afficher les données chargées par l'utilsateur
 * dans un tableau.
 * 
 * @param {String} dataArray - Ce paramètre un objet JSON represantant les données
 * chargées par l'utilisateur.
 */
export function afficherCSVDepuisObjet(dataArray) {
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
  constants.plot.innerHTML = "";
  constants.plot.appendChild(table);
}

/**
 * Cette fonction permet d'afficher les informations des données chargées
 * dans un tableau.
 * @param {JSON} resume - Ce paramètre est un objet JSON.
 */
export function afficherResumeDansTableau(resume) {
  constants.all_infos_on_data.style.display = "flex";
  constants.all_infos_on_data.innerHTML = "";

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

    constants.info_items.children[index].children[0].textContent = resume[key].length;

    if (resume[key].length)
      constants.info_items.children[index].children[0].textContent = resume[key].length;
    else if (typeof resume[key] === "number")
      constants.info_items.children[index].children[0].textContent = resume[key];
    else
      constants.info_items.children[index].children[0].textContent = Object.keys(
        resume[key]
      ).length;

    tr.appendChild(tdKey);
    tr.appendChild(tdValue);
    tbody.appendChild(tr);
    index += 1;
  }

  table.appendChild(tbody);
  constants.all_infos_on_data.appendChild(table);
}

/**
 * Cette fonction permet d'affichier un graphique en 2D des données chargées.
 * @param {String} graphique_path - Ce paramètre une chaîne de caractère du
 * fichier du graphique crée après chargement des données. 
 */
export async function afficherGraphique2D(graphique_path) {
  constants.plot.innerHTML = "";
  // iframe_contener.innerHTML = "";
  constants.iframe_contener.style.display = "flex";
  // iframe_contener.removeAttribute("src");
  console.log(graphique_path);
  console.log(constants.iframe_contener);
  // iframe_contener.classList[0].setAttribute("src", graphique_path)
}
