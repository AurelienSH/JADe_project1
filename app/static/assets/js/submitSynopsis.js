// Javascript pour récupérer le résultat de l'API et l'écrire au bon endroit

document.querySelector("#inputForm").onsubmit = async (event) => {
    event.preventDefault() // empêche la page de reload
    const form = event.target
    
    // Récupération de ce qu'on a écrit dans le formulaire
    const data = {
        content: form.querySelector("#synopsis").value,
    }
    
    // Définition de la requête POST
    const response = await fetch(
        form.action, // l'url de notre API
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

    // écriture du résultat dans la div avec l'ID "result"
    document.querySelector("#result").innerHTML = result
}