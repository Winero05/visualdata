/**
 * Cet objet contient toute les variables avec une portée globale à
 * la page active.
 */

export const constants = {

    open: false,

    main_index_html: document.getElementById("main_index_html"),

    dashboard: document.getElementById("dashboard"),

    open_dashboard: document.getElementsByClassName(
        "open_dashboard"
    )[0],

    open_dashboard_contener: document.getElementById(
        "open_dashboard_contener"
    ),

    close_dashboard: false,

    chargement_de_fichier_contener: document.getElementsByClassName(
        "chargement_de_fichier_contener"
    )[0],

    closePopUp: document.getElementsByClassName("closePopUp")[0],

    visuale_closePopUp:
        document.getElementsByClassName("visuale-closePopUp")[0],

    box_modal: document.getElementsByClassName("box_modal")[0],

    myPopUp: document.getElementsByClassName("myPopUp")[0],

    visualisation_box_modal: document.getElementsByClassName(
        "visualisation-box-modal"
    )[0],

    compte_box: document.getElementsByClassName("compte-box")[0],

    compte_info: document.getElementsByClassName("compte-info")[0],

    form_visualisation:
        document.getElementsByClassName("form-visualisation")[0],

    url_or_filePath: document.getElementById("url_or_filePath"),

    filePath: document.getElementById("filePath"),

    type_de_visualisation: document.getElementById("type_de_visualisation"),

    display: true,

    toggle: true,

    infos_data: document.getElementsByClassName("infos_data")[0],

    infos_msg: document.getElementsByClassName("info-msg")[0],

    info_items: document.getElementsByClassName("info-items")[0],

    info_items_icon: document.getElementsByClassName("info-items-icon")[0],

    up_icon_svg: document.getElementById("up-icon-svg"),

    resize_dashboard: document.getElementsByClassName("resize-dashboard")[0],

    contener: document.getElementById("contener"),

    resize_plot: document.getElementsByClassName("resize-plot")[0],

    resumer_des_donnees: document.getElementsByClassName(
        "resumer_des_donnees"
    )[0],

    all_infos_on_data:
        document.getElementsByClassName("all-infos-on-data")[0],

    single_info_on_data: document.getElementsByClassName(
        "single-info-on-data"
    )[0],

    numerique_col: document.getElementsByClassName("numerique_col")[0],

    charge_data_message: document.getElementsByClassName(
        "charge-data-message"
    )[0],

    iframe_contener: document.getElementsByClassName("iframe_contener")[0],

    btn_path_file: document.getElementsByClassName("btn_path_file")[0],

    plot: document.getElementById("plot"),

    reduction_methode_options: document.getElementById(
        "reduction_methode_options"
    ),

    visual_contener: document.getElementsByClassName("visual_contener"),

    visual_2d: document.getElementsByClassName("visual_2d"),

    visual_3d: document.getElementsByClassName("visual_3d"),


    data_analysis: "http://127.0.0.1:8000/v_01/analyse/",

    visualisation2d: "http://127.0.0.1:8000/v_01/visualisation/2d/",

    visualisation3d: "http://127.0.0.1:8000/v_01/visualisation/3d/",

    data_loading: "http://127.0.0.1:8000/v_01/data/",

    visualize_column: new Object(),


    analysis_data: new Object(),

    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
    },    
}
