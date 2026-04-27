# FitGen, Coach Intelligent

## L'idée de départ

Pendant le brainstorming, chacun a pitché une idée de projet. C'est celle d'un générateur de programme fitness qui a été retenue par le groupe. C'est un domaine où il y a beaucoup de logique à appliquer, beaucoup de règles à structurer, et un vrai besoin de personnalisation. Le problème qu'on voulait résoudre est simple. La plupart des gens qui commencent le fitness ne savent pas par où commencer, et les programmes génériques trouvés en ligne ne tiennent pas compte du matériel disponible, du niveau, ni de l'état physique du jour. FitGen est une application web construite avec Streamlit. L'utilisateur entre son profil, donc son niveau, son objectif, le matériel disponible et le nombre de jours par semaine qu'il peut consacrer aux sessions de fitness. À partir de ça, l'app génère un programme adapté qui évolue dans le temps et qui tient compte de son état physique.

## Les taches de chacun

Nous etions 3 sur ce projet. Mohamed Aziz a posé les bases du projet. Il a construit l'interface Streamlit, la logique de filtrage des exercices et des splits, ainsi que les données JSON de départ pour pouvoir generer un programme de fitness. Maelice a développé le module de récupération basé sur l'Indice de Hooper, un outil utilisé en sport de haut niveau pour mesurer la fatigue globale. L'utilisateur note son sommeil, sa fatigue, son stress et ses courbatures. Le programme du jour s'adapte ensuite automatiquement en fonction du score obtenu. De son côté, Yann a développé le moteur de progression. Vu qu'un programme fixe devient trop facile avec le temps, il a structuré une progression sur 6 semaines, ce qui est un standard en fitness avant de changer de cycle. Il a aussi enrichi la base de données d'exercices pour supporter cette progression en ajoutant les sets et reps de base pour chaque exercice, et une variante plus difficile pour certains exercices.

## Le parcours technique

Le développement s'est fait en parallèle, chacun sur sa propre partie. L'intégration a mis en évidence quelques problèmes. Le plus fréquent, c'était des variables non définies selon le contexte. Par exemple, le matériel disponible n'était défini dans l'interface que pour les utilisateurs à la maison, ce qui causait un crash pour les utilisateurs en gym. Une fois le problème identifié, le fix était simple, définir une valeur par défaut selon le contexte. On a aussi eu des cas où certaines règles ne s'activaient jamais parce que les champs qu'elles utilisaient n'existaient pas dans la base de données. Ça nous a forcés à enrichir le JSON avec les attributs manquants. Au final, les défis étaient surtout liés à la communication entre les modules et non à la logique interne de chacun.

## Le fonctionnement

L'application est divisée en 3 onglets. Le premier onglet génère le programme de base. En cliquant sur "Générer le programme", l'app sélectionne automatiquement un split d'entraînement adapté au profil. Le tableau affiche d'abord les jours et les groupes musculaires ciblés. Un bouton "Révéler les exercices" affiche ensuite les exercices concrets pour chaque jour, filtrés selon le niveau, le matériel disponible et le lieu d'entraînement. 

Le deuxième onglet c'est la progression sur 6 semaines. Le même programme évolue automatiquement chaque semaine. Les reps augmentent progressivement sur des paliers fixes, des variantes plus difficiles sont introduites aux semaines 3 et 6 pour certains exercices, et les sets augmentent en fin de cycle. Un slider permet de naviguer entre les semaines et de voir concrètement comment le programme change.

 Le troisième onglet est le module Recovery basé sur l'Indice de Hooper. L'utilisateur note 4 critères, la qualité du sommeil, la fatigue, le stress et les courbatures. Le score total s'affiche en temps réel. Selon ce score, le programme du jour est automatiquement allégé. Programme complet si tout va bien, exercices réduits si la fatigue est modérée, repos complet si le score dépasse le seuil critique. L'utilisateur peut aussi générer un programme complet calibré sur son score Hooper du jour.

## Les trois concepts du cours

Le projet a intégré trois technologies issues de trois cours différents. 

Premièrement, la représentation des connaissances se voit dans la structure des données. Les exercices ne sont pas de simples entrées JSON. Chaque exercice a ses attributs et ses relations avec d'autres exercices, notamment via les variantes. Les splits représentent des structures connues du domaine. Les règles de progression sont aussi définies comme des objets qu'on peut lire et modifier indépendamment du reste.

Ensuite, la logique et l'inférence apparaissent dans les deux modules intelligents. Le moteur de progression fonctionne avec du chaînage avant. Les règles sont évaluées dans un certain ordre, et chacune peut modifier le contexte avant que la suivante s'applique. Le module Recovery utilise une logique basée sur des seuils à partir du score Hooper pour ajuster le programme du jour.

Dernièrement les agents intelligents correspondent à l'architecture globalee. Chaque module observe une partie de l'environnement, comme le profil utilisateur, la semaine ou l'état physique du jour. Ensuite, il applique ses règles et produit une action, donc un programme adapté.

## Preuve de concept

FitGen montre qu'on peut construire un système de recommandation personnalisé sans machine learning. En combinant une base de connaissances structurée, des règles d'inférence explicites et une architecture extensive, on obtient un système qui s'adapte au profil de l'utilisateur, fait évoluer les recommandations dans le temps et réagit à son état physique.