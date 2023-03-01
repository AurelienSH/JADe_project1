function clickThumbButtons(button_id, isThumbUp) {

  // Sélection du bouton thumb-up/down cliqué
  const button_clicked = document.getElementById(button_id)

  // Sélection du numéro de la ligne du tableau pour pouvoir récupérer
  // les autres éléments de la même ligne
  const row_number = button_clicked.getAttribute("row_number")

  // Changement des couleurs des pouces
  updateThumbColor(isThumbUp, row_number);

  // Récupération des valeurs pour la suppression ou l'ajout du synopsis à la BDD

  const data =  {
    "title": document.getElementById(`title-result-${row_number}`).innerText,
    "date_published": document.getElementById(`date-published-result-${row_number}`).innerText,
    "type": document.getElementById(`type-result-${row_number}`).innerText,
    "content": document.getElementById("input_user").innerText
  }

  let method;
  // Requête POST pour ajouter si on clique sur thumb-up
  if (isThumbUp) {
      method = "POST";
  }
  // Requête DELETE pour supprimer de la BDD si on clique sur thumb-down
  else {
      method = "DELETE";
  }
  
  fetch(
    "http://127.0.0.1:8000/api/v1/synopsis", // l'url de notre API
    {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Accept": "text/html"
        },
        body: JSON.stringify(data)
    }
    );  
}

function updateThumbColor(isThumbUp, row_number) {
  
  // Sélection des deux boutons thumb de la ligne row_number
  const row_thumb_up_button = document.getElementById(`thumb-up-button-result-${row_number}`);
  const row_thumb_down_button = document.getElementById(`thumb-down-button-result-${row_number}`);

  //Changement des couleurs

  /*
  * Si on clique sur thumb-up, il devient vert
  * Et le thumb-down de la même ligne devient gris s'il avait été cliqué avant.
  */
  if (isThumbUp) {
      row_thumb_down_button.classList.remove("active");
      row_thumb_up_button.classList.add("active");
  }

  /*
  * Si on clique sur le thumb-down, il devient rouge
  * Et le thumb-up de la ligne devient gris s'il avait été cliqué avant
  */
 else {
      row_thumb_up_button.classList.remove("active");
      row_thumb_down_button.classList.add("active");
 }
}