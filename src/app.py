import streamlit as st 
import pandas as pd
from logic import splitprog, xercices


st.set_page_config(page_title="FitGen Dashboard", layout="wide")


if 'current_split' not in st.session_state:
    st.session_state.current_split = None
if 'voir_exos' not in st.session_state:
    st.session_state.voir_exos = False

st.title("🤖 FitGen AI - Ton Coach Intelligent")


menu_programme, menu_option2, menu_option3 = st.tabs(["Programme", "option 2 ", "option 3"])


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



# --- CONTENU : OPTION 2 ---
with menu_option2:
    st.title("Option 2")
    st.info("fonctions")

# --- CONTENU : OPTION 3 ---
with menu_option3:
    st.title("Option 3")
    st.info("fonctions")