FitGen AI 
Ce projet est une application interactive conçue pour automatiser la création de programmes de musculation personnalisés en utilisant un système expert qui analyse le profil de l'utilisateur pour générer un planning optimisé, une sélection d'exercices adaptée à l'équipement disponible ainsi que... (PARTIE À COMPLÉTER)

------Membres de l'équipe-------
- Mohamed Aziz Ben Rhouma (@AzizBR-7)
- 


1. Prérequis:
Assurez-vous d'avoir Python 3.8+ installé sur votre machine.

2. Cloner le projet:
git clone https://github.com/AzizBR-7/Groupe-H.git
cd Groupe-H

3.Installation:
pip install streamlit pandas

4.Exécution:
streamlit run src/app.py


Structure du Dépôt:
├── data/                  # Base de connaissances
│   ├── Exercice.json      # exercices et équipements requis
│   └── Splits.json        # Structures d'entraînement
├── src/                   # Code source
│   ├── app.py             # Interface utilisateur
│   └── logic.py           # Logique de filtrage et algorithmes de l'agent
├── Blog.md                # Documentation détaillée 
└── README.md              # Guide de démarrage
