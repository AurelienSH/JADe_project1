# **SYNSEARCH**

---

- Code source : <https://github.com/AurelienSH/JADe_project1>
- Documentation : <https://aureliensh.github.io/JADe_project1/#/>
- Changelog : <https://hackmd.io/13aKsikiTVmVB0Kd4qSuYw?both>
---

## Présentation 

:clapper: *SynSearch* est le résultat d'un projet mené par l'équipe **JADe** dans le cadre de deux cours du Master TAL (UPN, Paris Sorbonne-Nouvelle, Inalco) :

- :spider_web: Interfaces web pour le TAL :spider_web:
- :brain: Réseaux de neurones :brain:

:clapper: *SynSearch* est une API qui suggère des films sur la base de requête d'utilisateurs. Si vous avez une :bulb: idée :bulb: de synopsis en tête, entrez là pour découvrir les films associés à vos envies. 

:clapper: *SynSearch* s'améliore continuellement grâce à vos avis, qu'il soit positif :+1: ou négatif :-1:, n'hésitez pas à nous le partager. On garde ces informations là pour nous :shushing_face:

## Quick start

```bash
git clone https://github.com/AurelienSH/JADe_project1
cd JADe_project1
pip install -U -r requirements.txt # Installation des dépendances

# Lancement de l'API
cd app/src
uvicorn main:app
```

Puis aller sur <http://127.0.0.1:8000/front/index.html> :rocket:

## Auteurs

SynSearch est possible grâce au travail de l'équipe **JADe**, composée de : 
- **J**ulie Halbout <julie.halbout@parisnanterre.fr>
- **A**urélien Said Housseini <aurelien.said-housseini@sorbonne-nouvelle.fr>
- **De**lphine Nguyen-Durandet <delphine.nguyen-durandet@sorbonne-nouvelle.fr>

Contactez nous si vous avez la moindre question ! 

## Versions

- V1 : Utilisation du modèle non-finetuné
- V2 : Utilisation du modèle finetuné

>[!note]
>L'interface graphique de l'API utilise la V2.