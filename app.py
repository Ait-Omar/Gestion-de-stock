# import streamlit as st
# import pandas as pd
# import os
# from PIL import Image
# import base64
# from io import BytesIO

# st.markdown(
#     """
#     <head>
#         <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">
#     </head>
#     """,
#     unsafe_allow_html=True
# )

# def image_to_base64(image_path):
#     img = Image.open(image_path)
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     img_str = base64.b64encode(buffer.getvalue()).decode()
#     return img_str

# # Charger le logo
# logo_path1 = "static/logo.png"  
# logo_base641 = image_to_base64(logo_path1)
# st.sidebar.markdown(
#     f"""
#       <div style="display: flex; justify-content: center; margin-bottom: 10px;">
#         <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="150">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# DATA_FILE = "stock.csv"

# # Charger ou créer le fichier de stock
# if os.path.exists(DATA_FILE):
#     df = pd.read_csv(DATA_FILE)
# else:
#     df = pd.DataFrame(columns=["Nom", "Référence", "Catégorie", "Quantité", "Seuil", "Statut", "Emplacement"])
# colonnes_obligatoires = ["Nom", "Référence", "Catégorie", "Quantité", "Seuil", "Statut", "Emplacement"]
# for col in colonnes_obligatoires:
#     if col not in df.columns:
#         df[col] = ""

# # Mettre à jour le statut automatiquement
# def mettre_a_jour_statut(df):
#     df["Statut"] = df.apply(lambda row: "Faible" if row["Quantité"] < row["Seuil"] else "En stock", axis=1)
#     return df

# df = mettre_a_jour_statut(df)

# # Badges HTML stylisés
# def badge(content, color):
#     return f'<span style="background-color:{color}; padding:4px 10px; border-radius:12px; color:white; font-size:0.8em;">{content}</span>'

# # Ligne HTML stylisée
# def ligne_html(row):
#     statut_color = "#28a745" if row["Statut"] == "En stock" else "#ffc107"
#     categorie_colors = {
#         "Bureautique": "#007bff",
#         "Mécanique": "#795548",
#         "EPI": "#f0ad4e"
#     }
#     categorie_color = categorie_colors.get(row["Catégorie"], "#6c757d")
#     emplacement_colors = {
#         "A": "#17a2b8",
#         "B": "#e83e8c"
#     }
#     emplacement_color = emplacement_colors.get(row["Emplacement"], "#6c757d")

#     return f"""
#     <tr>
#         <td>{row['Nom']}</td>
#         <td>{row['Référence']}</td>
#         <td>{badge(row['Catégorie'], categorie_color)}</td>
#         <td style="text-align:center;">{row['Quantité']}</td>
#         <td style="text-align:center;">{row['Seuil']}</td>
#         <td>{badge(row['Statut'], statut_color)}</td>
#         <td>{badge(row['Emplacement'], emplacement_color)}</td>
#     </tr>
#     """

# # Interface Streamlit
# st.set_page_config(page_title="Gestion de Stock", layout="wide")
# st.title("Gestion de Stock")

# menu = st.sidebar.radio("Menu", ["📋 Voir le stock", "➕ Ajouter un produit", "🔄 Mouvement de stock", "🗑️ Supprimer un article"])

# if menu == "📋 Voir le stock":
#     st.subheader("Stock actuel")

#     with st.expander("🔍 Filtres avancés", expanded=True):
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             statut_filtre = st.selectbox("Statut", ["Tous", "En stock", "Faible"])

#         with col2:
#             categories = ["Tous"] + sorted(df["Catégorie"].dropna().unique().tolist())
#             cat_filtre = st.selectbox("Catégorie", categories)

#         with col3:
#             emplacements = ["Tous"] + sorted(df["Emplacement"].dropna().unique().tolist())
#             emp_filtre = st.selectbox("Emplacement", emplacements)
   
#     # Appliquer les filtres
#     df_filtre = df.copy()
#     if statut_filtre != "Tous":
#         df_filtre = df_filtre[df_filtre["Statut"] == statut_filtre]
#     if cat_filtre != "Tous":
#         df_filtre = df_filtre[df_filtre["Catégorie"] == cat_filtre]
#     if emp_filtre != "Tous":
#         df_filtre = df_filtre[df_filtre["Emplacement"] == emp_filtre]

#     # Générer le tableau HTML
#     table_html = """
#     <style>td, th { padding: 8px; }</style>
#     <table style="width:100%; border-collapse:collapse;">
#     <thead>
#     <tr style="text-align:left; background-color:#f8f9fa;">
#         <th>Nom</th>
#         <th>Référence</th>
#         <th>Catégorie</th>
#         <th>Qté</th>
#         <th>Seuil</th>
#         <th>Statut</th>
#         <th>Emplacement</th>
#     </tr>
#     </thead>
#     <tbody>
#     """ + "".join(ligne_html(row) for _, row in df_filtre.iterrows()) + """
#     </tbody>
#     </table>
#     """

#     st.markdown(table_html, unsafe_allow_html=True)

# elif menu == "➕ Ajouter un produit":
#     st.subheader("➕ Ajouter un nouveau produit")

#     with st.form("ajout_produit"):
#         col1, col2 = st.columns(2)
#         with col1:
#             nom = st.text_input("Nom du produit")
#             ref = st.text_input("Référence")
#             cat = st.selectbox("Catégorie", ["Bureautique", "Mécanique", "EPI"])
#         with col2:
#             qte = st.number_input("Quantité en stock", min_value=0, step=1)
#             seuil = st.number_input("Seuil d'alerte", min_value=0, step=1)
#             emp = st.selectbox("Emplacement", ["A", "B"])

#         submit = st.form_submit_button("Ajouter")
#         if submit:
#             nouveau = pd.DataFrame([{
#                 "Nom": nom,
#                 "Référence": ref,
#                 "Catégorie": cat,
#                 "Quantité": qte,
#                 "Seuil": seuil,
#                 "Emplacement": emp
#             }])
#             nouveau = mettre_a_jour_statut(nouveau)
#             df = pd.concat([df, nouveau], ignore_index=True)
#             df.to_csv(DATA_FILE, index=False)
#             st.success("✅ Produit ajouté avec succès !")
# elif menu == "🗑️ Supprimer un article":
#     st.subheader("🗑️ Suppression d'un produit")

#     if df.empty:
#         st.info("Aucun article à supprimer.")
#     else:
#         produit_sel = st.selectbox("Sélectionner un article à supprimer", df["Nom"].unique().tolist())

#         # Afficher les infos de l'article (facultatif)
#         st.write("🔎 Détails de l’article sélectionné :")
#         st.dataframe(df[df["Nom"] == produit_sel])

#         # Confirmation
#         confirm = st.checkbox("Je confirme la suppression définitive de cet article.")

#         if st.button("❌ Supprimer l'article") and confirm:
#             df = df[df["Nom"] != produit_sel]  # Supprimer toutes les lignes avec ce nom
#             df.to_csv(DATA_FILE, index=False)
#             st.success(f"✅ Article '{produit_sel}' supprimé définitivement.")

# elif menu == "🔄 Mouvement de stock":
#     st.subheader("🔄 Ajouter ou retirer de la quantité")

#     if df.empty:
#         st.info("Aucun produit enregistré.")
#     else:
#         produit_sel = st.selectbox("Choisir un article", df["Nom"].tolist())
#         mouvement = st.radio("Type de mouvement", ["➕ Ajouter", "➖ Retirer"])
#         quantite = st.number_input("Quantité", min_value=1, step=1)

#         if st.button("Valider le mouvement"):
#             idx = df[df["Nom"] == produit_sel].index[0]
#             if mouvement == "➕ Ajouter":
#                 df.at[idx, "Quantité"] += quantite
#             else:
#                 df.at[idx, "Quantité"] = max(0, df.at[idx, "Quantité"] - quantite)

#             df = mettre_a_jour_statut(df)
#             df.to_csv(DATA_FILE, index=False)
#             st.success(f"✅ Quantité mise à jour pour '{produit_sel}'")

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from st_aggrid import AgGrid, GridOptionsBuilder

# --- Config ---
st.set_page_config("📦 Gestion de Stock", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Fonctions de chargement/sauvegarde ---
def charger_donnees(nom_fichier):
    chemin = os.path.join(DATA_DIR, nom_fichier)
    colonnes_par_defaut = {
        "stock.csv": ["Nom", "Référence", "Catégorie", "Qté", "Seuil", "Statut", "Emplacement", "Date"],
        "entrees.csv": ["Nom","Référence", "Qté Entrée", "Date"],
        "sorties.csv": ["Nom", "Qté Sortie", "Date"]
    }
    if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
        return pd.read_csv(chemin)
    return pd.DataFrame(columns=colonnes_par_defaut.get(nom_fichier, []))

def sauvegarder_donnees(df, nom_fichier):
    df.to_csv(os.path.join(DATA_DIR, nom_fichier), index=False)

# --- Utilitaires ---
def set_statut(qte, seuil):
    return "✅ En stock" if qte > seuil else "⚠️ Critique"

def badge(content, color):
    return f'<span style="background-color:{color}; padding:4px 10px; border-radius:12px; color:white; font-size:0.8em;">{content}</span>'

def ligne_html(row):
    statut_color = "#28a745" if row["Statut"] == "✅ En stock" else "#ffc107"
    categorie_colors = {
        "Bureautique": "#007bff",
        "RPI": "#6f42c1",
        "Mécanique": "#795548"
    }
    categorie_color = categorie_colors.get(row["Catégorie"], "#6c757d")
    emplacement_colors = {
        "A": "#17a2b8",
        "B": "#e83e8c"
    }
    emplacement_color = emplacement_colors.get(row["Emplacement"], "#6c757d")

    return f"""
    <tr>
        <td>{row['Nom']}</td>
        <td>{row['Référence']}</td>
        <td>{badge(row['Catégorie'], categorie_color)}</td>
        <td style=\"text-align:center;\">{row['Qté']}</td>
        <td style=\"text-align:center;\">{row['Seuil']}</td>
        <td>{badge(row['Statut'], statut_color)}</td>
        <td>{badge(row['Emplacement'], emplacement_color)}</td>
        <td>{row['Date']}</td>
    </tr>
    """

def afficher_tableau_html(df):
    table_html = """
    <style>td, th { padding: 8px; font-size: 0.9em; }</style>
    <table style="width:100%; border-collapse:collapse;">
    <thead>
    <tr style="text-align:left; background-color:#f8f9fa;">
        <th>Nom</th>
        <th>Référence</th>
        <th>Catégorie</th>
        <th>Qté</th>
        <th>Seuil</th>
        <th>Statut</th>
        <th>Emplacement</th>
        <th>Date</th>
    </tr>
    </thead>
    <tbody>
    """ + "".join(ligne_html(row) for _, row in df.iterrows()) + """
    </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

# --- Initialisation ---
if "page" not in st.session_state:
    st.session_state.page = "Stock disponible"

if "stock" not in st.session_state:
    st.session_state.stock = charger_donnees("stock.csv")
if "entrees" not in st.session_state:
    st.session_state.entrees = charger_donnees("entrees.csv")
if "sorties" not in st.session_state:
    st.session_state.sorties = charger_donnees("sorties.csv")

# --- Barre latérale ---
with st.sidebar:
    # st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/DIPS_logo.svg/512px-DIPS_logo.svg.png", width=150)
    menu = st.selectbox("📂 Menu", [
        "Stock disponible",
        "Entrées de stock",
        "Sorties de stock",
        "Ajouter une entrée",
        "Enregistrer une sortie"])
    st.session_state.page = menu

st.title("📦 Gestion de Stock")

# === PAGE : STOCK DISPONIBLE ===
if st.session_state.page == "Stock disponible":
    st.subheader("🧾 Stock Actuel")
    if st.session_state.stock.empty:
        st.info("Aucun stock disponible.")
    else:
        df = st.session_state.stock.copy()
        df = df.sort_values(by="Nom")
        df["Statut"] = df.apply(lambda row: set_statut(row["Qté"], row["Seuil"]), axis=1)
        st.session_state.stock = df
        afficher_tableau_html(df)

# === PAGE : ENTRÉES ===
elif st.session_state.page == "Entrées de stock":
    st.subheader("📥 Historique des Entrées")
    if st.session_state.entrees.empty:
        st.info("Aucune entrée enregistrée.")
    else:
        st.dataframe(st.session_state.entrees, use_container_width=True)

# === PAGE : SORTIES ===
elif st.session_state.page == "Sorties de stock":
    st.subheader("📤 Historique des Sorties")
    if st.session_state.sorties.empty:
        st.info("Aucune sortie enregistrée.")
    else:
        st.dataframe(st.session_state.sorties, use_container_width=True)

# === PAGE : AJOUTER UNE ENTRÉE ===
elif st.session_state.page == "Ajouter une entrée":
    st.subheader("➕ Ajouter une entrée")
    with st.form("form_entree"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            ref = st.text_input("Référence")
            cat = st.selectbox("Catégorie", ["Bureautique", "EPI", "Mécanique"])
        with col2:
            emp = st.selectbox("Emplacement", ["A", "B"])
            qte = st.number_input("Quantité", min_value=1)
            seuil = st.number_input("Seuil", min_value=0)
            date = st.date_input("Date", value=datetime.today())
            remarque = st.text_input("Remarque")
        submit = st.form_submit_button("Ajouter")

    if submit:
        exists = st.session_state.stock["Référence"] == ref
        if exists.any():
            idx = st.session_state.stock[exists].index[0]
            st.session_state.stock.at[idx, "Qté"] += qte
            st.session_state.stock.at[idx, "Date"] = date
        else:
            st.session_state.stock = pd.concat([st.session_state.stock, pd.DataFrame([{
                "Nom": nom, "Référence": ref, "Catégorie": cat,
                "Qté": qte, "Seuil": seuil, "Statut": set_statut(qte, seuil),
                "Emplacement": emp, "Date": date
            }])], ignore_index=True)

        st.session_state.entrees = pd.concat([st.session_state.entrees, pd.DataFrame([{
            "Nom":nom,"Référence": ref, "Qté Entrée": qte, "Date": date
        }])], ignore_index=True)

        sauvegarder_donnees(st.session_state.stock, "stock.csv")
        sauvegarder_donnees(st.session_state.entrees, "entrees.csv")

        st.success("Entrée enregistrée avec succès ✅")

# === PAGE : SORTIE ===
elif st.session_state.page == "Enregistrer une sortie":
    st.subheader("➖ Sortie de stock")
    if st.session_state.stock.empty:
        st.warning("Aucun article en stock.")
    else:
        with st.form("form_sortie"):
            nom = st.selectbox("Nom", st.session_state.stock["Nom"].unique())
            qte_sortie = st.number_input("Quantité à sortir", min_value=1)
            remarque = st.text_input("Remarque")
            date = st.date_input("Date", value=datetime.today())
            submit_sortie = st.form_submit_button("Valider sortie")

        if submit_sortie:
            idx = st.session_state.stock[st.session_state.stock["Nom"] == nom].index[0]
            qte_dispo = st.session_state.stock.at[idx, "Qté"]
            if qte_sortie > qte_dispo:
                st.error("Quantité insuffisante ❌")
            else:
                st.session_state.stock.at[idx, "Qté"] -= qte_sortie
                st.session_state.stock.at[idx, "Date"] = date
                st.session_state.stock.at[idx, "Statut"] = set_statut(
                st.session_state.stock.at[idx, "Qté"], st.session_state.stock.at[idx, "Seuil"])

                st.session_state.sorties = pd.concat([st.session_state.sorties, pd.DataFrame([{
                    "Nom":nom,"Qté Sortie": qte_sortie, "Date": date
                }])], ignore_index=True)

                sauvegarder_donnees(st.session_state.stock, "stock.csv")
                sauvegarder_donnees(st.session_state.sorties, "sorties.csv")

                st.success("Sortie enregistrée ✅")
