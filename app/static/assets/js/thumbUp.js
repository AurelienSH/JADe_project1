function thumbUp(button_id) {

  // Sélection du bouton thumb-up cliqué
  thumb_up_button_clicked = document.getElementById(button_id)

  // Sélection du numéro de la ligne du tableau
  const row_number = thumb_up_button_clicked.getAttribute("row_number")

  // Sélection du bouton thumb-down sur la même ligne
  var row_thumb_down_button = document.getElementById(`thumb-down-button-result-${row_number}`);
  
  /*
  Changement des couleurs : 
  - thumb-up devient vert
  - thumb-down redevient gris s'il avait déjà été cliqué avant
  */
  row_thumb_down_button.classList.remove("active");
  thumb_up_button_clicked.classList.add("active");

  // Récupération des valeurs

  var data =  {
    "title": document.getElementById(`title-result-${row_number}`).innerText,
    "date_published": document.getElementById(`date-published-result-${row_number}`).innerText,
    "type": document.getElementById(`type-result-${row_number}`).innerText,
    "content": document.getElementById("input_user").innerText
  }

  // Requête POST pour ajouter la requête comme synopsis de l'oeuvre
  // à laquelle il a mis un thumb-up
  fetch(
    "http://127.0.0.1:8000/synopsis", // l'url de notre API
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "text/html"
        },
        body: JSON.stringify(data)
    }
    )


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

  // Récupération des valeurs
  var data =  {
    "title": document.getElementById(`title-result-${row_number}`).innerText,
    "date_published": document.getElementById(`date-published-result-${row_number}`).innerText,
    "type": document.getElementById(`type-result-${row_number}`).innerText,
    "content": document.getElementById("input_user").innerText
  }

  // Requête DELETE pour supprimer le synopsis écrit par l'utilisateur de la BDD
  // pour l'oeuvre sélectionné, si jamais il avait mis un thumb-up avant
  fetch(
    "http://127.0.0.1:8000/synopsis", // l'url de notre API
    {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }
    )
}