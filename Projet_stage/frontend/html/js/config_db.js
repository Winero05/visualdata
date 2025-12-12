"use strict"
document.querySelector("html").classList.add("js");
// Les toutes de directions(< ... >).
const move_box = document.getElementsByClassName("move-box")[0];
const left = document.getElementsByClassName("left")[0];
const right = document.getElementsByClassName("right")[0];
let slides = document.getElementsByClassName("mySlides");
let cercle = document.getElementsByClassName("cercle");

// Les différentes types de modèle à afficher.
const form = document.getElementsByClassName("form")[0];
const modal = document.getElementsByClassName("modal")[0];
const model = document.getElementsByClassName("model")[0];
const msg = document.getElementsByClassName("msg")[0];
const local = document.getElementById("local");
const distant = document.getElementById("distant");
const base_de_donnees = document.getElementsByClassName("choix")[0];
const boite_des_db = document.getElementsByClassName("des-db")[0];
const configuration = document.getElementsByClassName("configuration")[0];
const submit_reset_btn = document.getElementsByClassName("submit-reset-btn")[0];

// Interaction avec le CSS

move_box.addEventListener("click", (event) => {
    const elementClique = event.target;
    const pageCorrespondante = event.target.offsetParent.children;
    const longueur = elementClique.classList.length;
    const className = elementClique.className;

    if (longueur === 1 && className === "cercle") {
        // Suppression de la couleur blanche dans le cercle précédente.
        for (let i = 0; i < cercle.length; i++) {
            if (left.style.cursor === "not-allowed") {
                left.style.cursor = "pointer";
                left.style.opacity = "1";
                left.removeAttribute("disabled");
            }
            if (right.style.cursor === "not-allowed") {
                right.style.cursor = "pointer";
                right.style.opacity = "1";
                right.removeAttribute("disabled");
            }
            if (cercle[i].classList.length > 1) {
                cercle[i].classList.remove("fond-blanc");
                slides[i].style.display = "none";
                break;
            }
        }
        // Ajoute de la couleur blanche dans le cercle cliqué.
        elementClique.classList.add("fond-blanc");
        // Affichage de la page correspondante au cercle cliqué.
        for (let i = 0; i < pageCorrespondante.length - 1; i++) {
            if (pageCorrespondante[i].classList.length > 1) {
                slides[i-1].style.display = "flex";
                break;
            }
        }
    } else if (longueur === 1 && className === "left") {
        if (cercle[0].classList.length > 1) {
            left.style.cursor = "not-allowed";
            left.style.opacity = ".6";
            left.desabled = true;
        } else {
            for (let i = 0; i < cercle.length; i++) {
                if (cercle[3].classList.length > 1) {
                    cercle[3].classList.remove("fond-blanc");
                    slides[3].style.display = "none";
                    cercle[2].classList.add("fond-blanc");
                    slides[2].style.display = "flex";
    
                    right.style.cursor = "pointer";
                    right.style.opacity = "1";
                    right.removeAttribute("disabled");
                    break;
                }
                if (cercle[i].classList.length > 1) {
                    cercle[i].classList.remove("fond-blanc");
                    slides[i].style.display = "none";
                    cercle[i-1].classList.add("fond-blanc");
                    slides[i-1].style.display = "flex";
                    break;
                }
            }
        }
    } else if (longueur === 1 && className === "right") {
        if (cercle[3].classList.length > 1) {
            right.style.cursor = "not-allowed";
            right.style.opacity = ".6";
            right.desabled = true;            
        } else {
            for (let i = 0; i < cercle.length; i++) {
                if (cercle[0].classList.length > 1) {
                    cercle[0].classList.remove("fond-blanc");
                    slides[0].style.display = "none";
                    cercle[1].classList.add("fond-blanc");
                    slides[1].style.display = "flex";
    
                    left.style.cursor = "pointer";
                    left.style.opacity = "1";
                    left.removeAttribute("disabled");
                    break;
                }
                if (cercle[i].classList.length > 1) {
                    cercle[i].classList.remove("fond-blanc");
                    slides[i].style.display = "none";
                    cercle[i + 1].classList.add("fond-blanc");
                    slides[i + 1].style.display = "flex";
                    break;
                }
            }
        }
    } else console.log("Il y a une erreur quelque part...");


    event.stopImmediatePropagation();
});

modal.addEventListener("click", () => {
    modal.style.display = "none";
    model.style.display = "flex";

    for (let i = 0; i < cercle.length; i++) {
        if (cercle[i].classList.length > 1) {
            cercle[i].classList.remove("fond-blanc");
            cercle[i+1].classList.add("fond-blanc");
            break;
        }
    }
});

model.addEventListener("click", () => {
    model.style.display = "none";
    base_de_donnees.style.display = "flex";

    for (let i = 0; i < cercle.length; i++) {
        if (cercle[i].classList.length > 1) {
            cercle[i].classList.remove("fond-blanc");
            cercle[i + 1].classList.add("fond-blanc");
            break;
        }
    }
})


base_de_donnees.addEventListener("click", (event) => {
    console.log(event);
    let text = "";
    const icon_est_cliquee = event.target.children.length;
    if (icon_est_cliquee) text = event.target.textContent.trim();
    else text = event.target.nextSibling.textContent.trim();
    if (text === "PostgreSQL") {
        base_de_donnees.style.display = "none";
        configuration.style.display = "flex";
        submit_reset_btn.style.display = "flex";
    } else if (text === "MySQL") {
        const schema = configuration.children[1].children[3];
        base_de_donnees.style.display = "none";
        schema.style.display = "none";
        configuration.style.display = "flex";
        submit_reset_btn.style.display = "flex";
    }
    for (let i = 0; i < cercle.length; i++) {
        if (cercle[i].classList.length > 1) {
            cercle[i].classList.remove("fond-blanc");
            cercle[i + 1].classList.add("fond-blanc");
            break;
        }
    }

});
