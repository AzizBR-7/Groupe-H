# FitGen AI 

Ce projet est une application interactive conçue pour automatiser la création de programmes de musculation personnalisés en utilisant un système expert qui analyse le profil de l'utilisateur pour générer un planning optimisé, une sélection d'exercices adaptée à l'équipement disponible ainsi qu'une logique de décision intelligente permettant d'atteindre vos objectifs de progression.

### ------Membres de l'équipe-------
- Mohamed Aziz Ben Rhouma (@AzizBR-7)
-
-

1. **Prérequis:**
Assurez-vous d'avoir Python 3.8+ installé sur votre machine.

2. **Cloner le projet:**
```bash
git clone [https://github.com/AzizBR-7/Groupe-H.git](https://github.com/AzizBR-7/Groupe-H.git)
cd Groupe-H

Installation:
pip install streamlit pandas

Exécution:
streamlit run src/app.py

Structure du Dépôt:
├── data/                  # Base de connaissances
│   ├── Exercice.json      # Exercices et équipements requis
│   └── Splits.json        # Structures d'entraînement
├── src/                   # Code source
│   ├── app.py             # Interface utilisateur
│   └── logic.py           # Logique de filtrage et algorithmes
├── Blog.md                # Documentation détaillée
└── README.md              # Guide de démarrage
