import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
from io import BytesIO

st.markdown(
    """
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap" rel="stylesheet">
    </head>
    """,
    unsafe_allow_html=True
)

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Charger le logo
logo_path1 = "static/logo.png"  
logo_base641 = image_to_base64(logo_path1)
st.sidebar.markdown(
    f"""
      <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <img src="data:image/png;base64,{logo_base641}" alt="Logo" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "stock.csv"

# Charger ou créer le fichier de stock
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Nom", "Référence", "Catégorie", "Quantité", "Seuil", "Statut", "Emplacement"])
colonnes_obligatoires = ["Nom", "Référence", "Catégorie", "Quantité", "Seuil", "Statut", "Emplacement"]
for col in colonnes_obligatoires:
    if col not in df.columns:
        df[col] = ""

# Mettre à jour le statut automatiquement
def mettre_a_jour_statut(df):
    df["Statut"] = df.apply(lambda row: "Faible" if row["Quantité"] < row["Seuil"] else "En stock", axis=1)
    return df

df = mettre_a_jour_statut(df)

# Badges HTML stylisés
def badge(content, color):
    return f'<span style="background-color:{color}; padding:4px 10px; border-radius:12px; color:white; font-size:0.8em;">{content}</span>'

# Ligne HTML stylisée
def ligne_html(row):
    statut_color = "#28a745" if row["Statut"] == "En stock" else "#ffc107"
    categorie_colors = {
        "Informatique": "#007bff",
        "Mécanique": "#795548",
        "Informatique": "#f0ad4e"
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
        <td style="text-align:center;">{row['Quantité']}</td>
        <td style="text-align:center;">{row['Seuil']}</td>
        <td>{badge(row['Statut'], statut_color)}</td>
        <td>{badge(row['Emplacement'], emplacement_color)}</td>
    </tr>
    """

# Interface Streamlit
st.set_page_config(page_title="Gestion de Stock", layout="wide")
st.title("Gestion de Stock")

menu = st.sidebar.radio("Menu", ["📋 Voir le stock", "➕ Ajouter un produit","🗑️ Supprimer un article"])

if menu == "📋 Voir le stock":
    st.subheader("Stock actuel")

    with st.expander("🔍 Filtres avancés", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            statut_filtre = st.selectbox("Statut", ["Tous", "En stock", "Faible"])

        with col2:
            categories = ["Tous"] + sorted(df["Catégorie"].dropna().unique().tolist())
            cat_filtre = st.selectbox("Catégorie", categories)

        with col3:
            emplacements = ["Tous"] + sorted(df["Emplacement"].dropna().unique().tolist())
            emp_filtre = st.selectbox("Emplacement", emplacements)
   
    # Appliquer les filtres
    df_filtre = df.copy()
    if statut_filtre != "Tous":
        df_filtre = df_filtre[df_filtre["Statut"] == statut_filtre]
    if cat_filtre != "Tous":
        df_filtre = df_filtre[df_filtre["Catégorie"] == cat_filtre]
    if emp_filtre != "Tous":
        df_filtre = df_filtre[df_filtre["Emplacement"] == emp_filtre]

    # Générer le tableau HTML
    table_html = """
    <style>td, th { padding: 8px; }</style>
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
    </tr>
    </thead>
    <tbody>
    """ + "".join(ligne_html(row) for _, row in df_filtre.iterrows()) + """
    </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)

elif menu == "➕ Ajouter un produit":
    st.subheader("➕ Ajouter un nouveau produit")

    with st.form("ajout_produit"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom du produit")
            ref = st.text_input("Référence")
            cat = st.selectbox("Catégorie", ["Informatique", "Mécanique", "EPI"])
        with col2:
            qte = st.number_input("Quantité en stock", min_value=0, step=1)
            seuil = st.number_input("Seuil d'alerte", min_value=0, step=1)
            emp = st.selectbox("Emplacement", ["A", "B"])

        submit = st.form_submit_button("Ajouter")
        if submit:
            nouveau = pd.DataFrame([{
                "Nom": nom,
                "Référence": ref,
                "Catégorie": cat,
                "Quantité": qte,
                "Seuil": seuil,
                "Emplacement": emp
            }])
            nouveau = mettre_a_jour_statut(nouveau)
            df = pd.concat([df, nouveau], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Produit ajouté avec succès !")
elif menu == "🗑️ Supprimer un article":
    st.subheader("🗑️ Supprimer un produit du stock")

    if df.empty:
        st.info("Aucun produit à supprimer.")
    else:
        produit_sel = st.selectbox("Sélectionner un produit", df["Nom"].tolist())
        action = st.radio("Type de suppression", ["Réduire la quantité", "Supprimer complètement l'article"])

        if action == "Réduire la quantité":
            quantite_retrait = st.number_input("Quantité à retirer", min_value=1, step=1)
            if st.button("Retirer"):
                idx = df[df["Nom"] == produit_sel].index[0]
                df.at[idx, "Quantité"] = max(0, df.at[idx, "Quantité"] - quantite_retrait)
                df = mettre_a_jour_statut(df)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ Quantité réduite avec succès.")

        elif action == "Supprimer complètement l'article":
            if st.button("Supprimer définitivement"):
                df = df[df["Nom"] != produit_sel]
                df.to_csv(DATA_FILE, index=False)
                st.success(f"❌ L'article '{produit_sel}' a été supprimé.")
