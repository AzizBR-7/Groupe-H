import streamlit as st 
import pandas as pd
from logic import splitprog, xercices, charger_donnees
from inference import generer_progression

st.set_page_config(page_title="FitGen Dashboard", layout="wide")


if 'current_split' not in st.session_state:
    st.session_state.current_split = None
if 'voir_exos' not in st.session_state:
    st.session_state.voir_exos = False

st.title("🤖 FitGen AI - Ton Coach Intelligent")


menu_programme, menu_progression, menu_option3 = st.tabs(["Programme", "Progression 6 Semaines ", "option 3"])


with st.sidebar:
    st.header("Profil Utilisateur")
    nom_user = st.text_input("Nom")
    niveau = st.selectbox("Niveau", ["Débutant", "Avancé"])
    objectif = st.radio("Objectif", ["Maintenir", "Gain de masse"])
    jours = st.slider("Disponibilité (jours/semaine)", 1, 7, 5)
    


    if niveau == "Avancé":
        st.warning("Accès Gym requis.")
        lieu = "Gym"
    else:
        lieu = st.radio("Lieu d'entraînement", ["Maison", "Gym"])
    

    if lieu == "Maison":
        matos = st.multiselect("Matériel à la maison", ["haltères", "élastique", "chaise", "tapis"])



with menu_programme:
    col_gauche, col_droite = st.columns([2, 1]) 

    with col_gauche:

        if st.button("Génerer le programme"):
            resultat = splitprog(jours, niveau, objectif, lieu)
            if resultat:
                st.session_state.current_split = resultat
                st.session_state.voir_exos = False  
            else:
                st.error("L'agent n'a pas trouvé de programme. Change les critères.")


        if st.session_state.current_split:
            split = st.session_state.current_split
            st.success(f"{split['nom']}")
            

            donnees_tableau = []
            for jour, muscles in split['structure'].items():
                if muscles == ["Repos"]:
                    exos_str = "😴 Repos"
                else:

                    liste_exos = xercices(muscles, niveau, matos, lieu)
                    exos_str = ", ".join(liste_exos) if liste_exos else "⚠️ Aucun exercice adapté"
                
                donnees_tableau.append({
                    "Jour": jour,
                    "Focus Musculaire": " & ".join(muscles) if isinstance(muscles, list) else muscles,
                    "Détails Exercices": exos_str
                })
            
            df = pd.DataFrame(donnees_tableau)

  
            st.table(df[["Jour", "Focus Musculaire"]])


            st.write("---")
            if st.button("Révéler les exercices"):
                st.session_state.voir_exos = True


            if st.session_state.voir_exos:
                st.subheader("Exercices personnalisé")
                st.table(df[["Jour", "Détails Exercices"]])


# CONTENU YANN

with menu_progression:
    st.write("Adapte ton programme pour 6 semaines.")

    if not st.session_state.current_split:
        st.warning("Genere d'abord un programme dans l'onglet Programme.")
    else:
        semaine = st.slider("Semaine", min_value=1, max_value=6, value=1, step=1)

        matos_safe = matos if lieu == "Maison" else []

        muscles = []
        for v in st.session_state.current_split["structure"].values():
            if isinstance(v, list) and v != ["Repos"]:
                muscles.extend(v)

        noms_exos = xercices(muscles, niveau, matos_safe, lieu)
        all_exos = charger_donnees("Exercice.json")
        variantes = {e.get("variante_progression") for e in all_exos if e.get("variante_progression")}
        exos_programme = [e for e in all_exos if e["nom"] in noms_exos and e["nom"] not in variantes]

        if not exos_programme:
            st.warning("Aucun exercice trouve pour ce profil.")
        else:
            progression = generer_progression(exos_programme, semaine, niveau, all_exos)

            st.subheader(f"Programme — Semaine {semaine} / 6")

            if semaine in (3, 6):
                st.info("Semaine de progression : variantes plus difficiles potentiellement introduites.")

            lignes = []
            for p in progression:
                unite = p.get("unite", "reps")
                volume = f"{p['sets']} x {p['reps']}{'s' if unite == 'secondes' else ' reps'}"
                ligne = {
                    "Exercice": p["nom"],
                    "Muscle": p["muscle"],
                    "Volume": volume,
                }
                if p["est_variante"]:
                    ligne["Exercice"] += "  *"
                lignes.append(ligne)

            import pandas as pd
            df = pd.DataFrame(lignes)
            st.dataframe(df, use_container_width=True, hide_index=True)

            if any(p["est_variante"] for p in progression):
                st.caption("* Variante introduite cette semaine")

# --- CONTENU : OPTION 3 ---
with menu_option3:
    st.title("Option 3")
    st.info("fonctions")