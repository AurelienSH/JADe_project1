# **SYNSEARCH**

---

- Code source : <https://github.com/AurelienSH/JADe_project1>
- Documentation : <https://github.com/AurelienSH/JADe_project1/tree/main/docs>
- Changelog : <https://hackmd.io/13aKsikiTVmVB0Kd4qSuYw?both>
---

## Présentation 

:clapper: *SynSearch* est le résultat d'un projet mené par l'équipe **JADe** dans le cadre de deux cours du Master TAL (UPN, Paris Sorbonne-Nouvelle, Inalco) :

- :spider_web: Interfaces web pour le TAL :spider_web:
- :brain: Réseaux de neurones :brain:

:clapper: *SynSearch* est une API qui suggère des films sur la base de requête d'utilisateurs. Si vous avez une :bulb: idée :bulb: de synopsis en tête, entrez là pour découvrir les films associés à vos envies. 

:clapper: *SynSearch* s'améliore continuellement grâce à vos avis, qu'il soit positif :+1: ou négatif :-1:, n'hésitez pas à nous le partager. On garde ces informations là pour nous :shushing_face:

Ce document a pour but d'expliquer notre projet : 

- :notebook_with_decorative_cover: [Découvrir les données utilisées](01_data.md) :notebook_with_decorative_cover:
- :nerd_face: [Entrer dans le système mis en place](02_systeme.md) :nerd_face:
- :spider_web: [Appréhender l'interface de l'API](03_interface.md) :spider_web:
- :chart_with_upwards_trend: [Décortiquer les résultats de notre système](04_evaluation.md) :chart_with_upwards_trend:
- :male_detective: [En savoir plus sur notre manière de travailler](05_methodologie.md) :male_detective:

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