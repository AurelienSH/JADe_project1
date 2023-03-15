// Script pour ajouter une review à la BDD depuis l'interface graphique

function clickThumbButtons(button_id, isThumbUp) {

  // Sélection du bouton thumb-up/down cliqué
  const button_clicked = document.getElementById(button_id)

  // Sélection du numéro de la ligne du tableau pour pouvoir récupérer
  // les autres éléments de la même ligne
  const row_number = button_clicked.getAttribute("row_number")

  // Changement des couleurs des pouces
  updateThumbColor(isThumbUp, row_number);

  // Récupération de la valeur de "score" selon si c'est un thumb-up ou thumb-down
  let score;
  if (isThumbUp) { // Review positive
      score = "pos";
  }
  else { // Review négative
      score = "neg";
  }

  // Schéma Pydantic "ReviewAdd" pour l'ajout d'une review
  const review =  {
    "title": document.getElementById(`title-result-${row_number}`).innerText,
    "synopsis": document.getElementById(`content-result-${row_number}`).innerText,
    "query": document.getElementById("input_user").innerText,
    "score": score
  };
  
  fetch(
    "http://127.0.0.1:8000/api/v2/reviews", // l'url de notre API
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "text/html"
        },
        body: JSON.stringify(review)
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