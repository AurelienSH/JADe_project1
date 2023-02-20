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

  // Ajout du synopsis à la BDD

  var data =  {
    "title": document.getElementById(`title-result-${row_number}`),
    "date_published": document.getElementById(`date_published-result-${row_number}`),
    "type": document.getElementById(`type-result-${row_number}`),
    "content": 
  }
  

  // Définition de la requête POST
  const response = fetch(
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

  // récupération du résultat de la requête
  const result = await response.text() // read response body as text
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