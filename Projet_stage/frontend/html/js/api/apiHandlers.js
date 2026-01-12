import { constants } from "../configs/constants.js";
import {
    afficherCSVDepuisObjet,
    afficherResumeDansTableau,
    afficherGraphique2D } from "../utils/domUtils.js";

// Interaction avec l'API

/**
 * Cette fonction cherche à lire des données chargé par l'utilisateur.
 * @returns {JSON} Un objet JSON est retournée à la fin de cette fonction.
 */
export async function readLoadedData() {
    const response = await fetch(constants.data_loading, {
        method: "GET",
        headers: constants.headers,
    });
    if (!response.ok) throw new Error("Erreur HTTP " + response.status);
    const data = await response.json();
    // Affichage dans le HTML
    afficherCSVDepuisObjet(data);
    return data;
}

/**
 * Cette fonction permet de lire l'analyse des données chargées par l'utilisateur.
 * @returns {JSON} Un objet JSON est retournée par cette fonction.
 */
export async function readDataAnalysis() {
    const response = await fetch(constants.data_analysis, {
        method: "GET",
        headers: constants.headers,
    });
    if (!response.ok) throw new Error("Erreur HTTP " + response.status);
    const data = await response.json();
    constants.analysis_data = data;
    afficherResumeDansTableau(data);
    return data;
}

/**
 * Cette fonction permet de lire le chemin d'un fichier graphique 2D généré après
 * chargement des données.
 */
export async function readVisualization_2d() {
    const response = await fetch(constants.visualisation2d, {
        method: "GET",
        headers: constants.headers,
    })
    if (!response.ok) throw new Error("Erreur HTTP " + response.status);
    const data = await response.json();
    console.log(data);
    if (data["html_file"]) afficherGraphique2D(data["html_file"]);
    else afficherGraphique2D(data["html_files"][0]);
}

/**
 * Cette fonction permet de lire le chemin d'un fichier graphique 3D généré après
 * chargement des données.
 */
export async function readVisualization_3d() {
    // const data = afficherGraphique3D(data);
    // fetch(visualisation3d, {
    //     method: "GET",
    //     constants.headers: {
    //         Accept: "application/json",
    //     },
    // })
    // .then((response) => {
    //     if (!response.ok) {
    //         throw new Error("Erreur HTTP " + response.status);
    //     }
    //     return response.json();
    // })
    // .then((data) => {
    //     afficherGraphique3D(data);
    // })
}
