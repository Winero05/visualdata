/**
 * Cette fonction permet d'afficher une animation d'un cercle montrant
 * le chargement d'une demande de la part de l'utilisateur.
 */
export async function showLoader() {
	const container = ensureLoaderContainer();

	if (!document.getElementById("loader")) {
		const response = await fetch(
			"http://127.0.0.1:5501/Projet_stage/frontend/html/modal-loading.html"
		);
		container.innerHTML = await response.text();
	}

	document.getElementById("loader").style.display = "flex";
}

/**
 * Cette fonction permet de cacher l'animation d'un cercle montrant le chargement
 * d'une demande de la part de l'utilisateur si les données demanant sont prête.
 */
export function hideLoader() {
	const container = document.getElementById("loader-container");
	const loader = document.getElementById("loader");
	container.removeChild(loader);
	container.style.display = "none";
}

/**
 * Cette fonction crée un élément HTML.
 *
 * @returns {HTMLElement} - Un élément HTML est retourné par cette fonction pour
 * permettre l'animation d'un cercle de chargement à l'utilisateur lors d'un
 * chargement de données.
 */
function ensureLoaderContainer() {
	let container = document.getElementById("loader-container");
	if (!container) {
		container = document.createElement("div");
		container.id = "loader-container";
		document.body.appendChild(container);
	}
	return container;
}
