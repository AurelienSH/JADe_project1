function thumbUp(button_id) {

  thumb_up_button_clicked = document.getElementById(button_id)
  const row_number = thumb_up_button_clicked.getAttribute("row_number")

  var row_thumb_down_button = document.getElementById(`thumb-down-button-result-${row_number}`);
  
  /*
  Changement des couleurs : 
  - thumb-up devient vert
  - thumb-down redevient gris s'il avait déjà été cliqué avant
  */
  row_thumb_down_button.classList.remove("active");
  thumb_up_button_clicked.classList.add("active");
}

function thumbDown(button_id){
  
  // Sélection du bouton thumb-down cliqué
  thumb_down_button_clicked = document.getElementById(button_id)

  // Sélection du numéro de la ligne du tableau
  const row_number = thumb_down_button_clicked.getAttribute("row_number")

  // Sélection du bouton thumb-up sur la même ligne
  var row_thumb_up_button = document.getElementById(`thumb-up-button-result-${row_number}`);
  
  /*
  Changement des couleurs : 
  - thumb-down devient rouge
  - thumb-down redevient gris s'il avait déjà été cliqué avant
  */
  row_thumb_up_button.classList.remove("active");
  thumb_down_button_clicked.classList.add("active");
}