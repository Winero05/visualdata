import { constants } from "../configs/constants.js";

export function initInfoEvents() {
    /**
     * Cette fonction permet d'afficher ou de cacher la fenêtre des
     * informations en bas des données chargées ou de la vu graphique
     * générée par les données chargées.
     */
    function voirLesInfos() {
        if (constants.display) {
            constants.resize_plot.style.display = "none";
            constants.contener.children[0].style.height = "88vh";
            constants.resumer_des_donnees.style.display = "none";
            constants.display = false;
        } else {
            constants.resize_plot.style.display = "flex";
            constants.contener.children[0].style.height = "61vh";
            constants.resumer_des_donnees.style.display = "flex";
            constants.display = true;
        }
    }

    constants.infos_msg.addEventListener("click", voirLesInfos);

    /**
     * Cette fonction permet d'afficher les différentes types d'analyse
     * possible à visualiser dans la fenêtre situer en bas des donnnées
     * chargées.
     */
    function selectionneDInfoSpecifique() {
        if (constants.info_items.style.display === "none") {
            constants.info_items.style.display = "flex";
            constants.info_items.style.width = "100%";
            constants.info_items.style.flexDirection = "column";
            constants.up_icon_svg.style.rotate = "0 0 0 0deg";
            constants.toggle = false;
        } else {
            constants.up_icon_svg.style.rotate = "5 0 1 180deg";
            constants.info_items.style.display = "none";
            constants.toggle = true;
        }
    }

    constants.info_items_icon.addEventListener(
        "click",
        selectionneDInfoSpecifique
    );

    /**
     * Cette fonction affiche un table contenant une information
     * pour une analyse spécifique.
     *
     * @param {Object} donneAnalyse - Ce paramètre reçoit un objet JS contenant
     * l'analyse des données chargées.
     */
    function afficherUnResumeEnParticulier(donneAnalyse) {
        constants.single_info_on_data.innerHTML = "";
        constants.single_info_on_data.style.display = "flex";

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
        constants.single_info_on_data.appendChild(table);
    }

    constants.info_items.addEventListener("click", (event) => {
        afficherUnResumeEnParticulier(constants.analysis_data);
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

    /**
     * Cette fonction permet de sélectionner les colonnes numérique à visualiser
     * sous forme graphique.
     */
    function type_de_visualisation() {
        if (constants.plot.children.length !== 2) {
            constants.numerique_col.innerHTML = "";
            constants.all_infos_on_data.style.display = "none";
            constants.single_info_on_data.style.display = "none";
            constants.numerique_col.style.display = "flex";
            const div = document.createElement("div");
            div.textContent = "Veuillez sélectionner les colonnes numérique à visualiser";
            constants.numerique_col.appendChild(div);
            constants.analysis_data["num_col"].forEach((Element) => {
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
                constants.numerique_col.appendChild(div);
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
            constants.numerique_col.appendChild(annulerOuContinuer);
        }
    }

    constants.type_de_visualisation.addEventListener("click", type_de_visualisation);
}
