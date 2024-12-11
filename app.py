import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Streamlit app title and layout
st.set_page_config(
    page_title="Threads vs Temps d'exécution",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Threads vs Temps d'exécution")
st.markdown(
    """
    Cette application permet de visualiser les relations entre le nombre de threads et le temps d'exécution. 
    Les tests ont été réalisés sur deux configurations : un MacBook Pro sous macOS équipé d’un CPU Apple M1 Pro (8 cœurs, 8 threads) 
    et un ThinkPad sous Ubuntu avec un CPU Intel i7-10610 (4 cœurs, 8 threads). 
    L’objectif est de comparer les performances des deux systèmes afin de soutenir mon rapport du laboratoire LAB6 en programmation système, 
    enseigné par M. Alexandre BRIERE à l’école ESIEA.
    """
)

# Sidebar
st.sidebar.title("🔧 Options")
sheet_selection = st.sidebar.radio("📋 Sélectionnez OS-CPU :", ["MACOS-M1PRO", "UBUNTU-I7"])
comparison = st.sidebar.checkbox("🔄 Comparer les deux OS-CPU")
st.sidebar.markdown(
    """
    **Astuce** : Les graphiques sont interactifs 😍 !
    Vous pouvez survoler avec la souris pour afficher les détails des valeurs, zoomer sur une partie spécifique du graphique, et bien plus encore.
    """
)

EXCEL_FILE_PATH = "./execution_time.xlsx"

def load_data():
    excel_data = pd.ExcelFile(EXCEL_FILE_PATH)
    sheet1 = excel_data.parse(sheet_name="MACOS-M1PRO")
    sheet2 = excel_data.parse(sheet_name="UBUNTU-I7")
    return sheet1, sheet2

sheet1, sheet2 = load_data()

selected_data = sheet1 if sheet_selection == "MACOS-M1PRO" else sheet2
selected_sheet_name = "MACOS-M1PRO" if sheet_selection == "MACOS-M1PRO" else "UBUNTU-I7"

# Dataframe display
with st.expander(f"📂 Afficher les données de : {selected_sheet_name}"):
    st.dataframe(selected_data)

# Single graph
min_time_row = selected_data.loc[selected_data["Real time used"].idxmin()]
fig_single = go.Figure()

color_map = {
    "MACOS-M1PRO": "mediumseagreen",
    "UBUNTU-I7": "royalblue",
}

# Add trace for the selected sheet
fig_single.add_trace(
    go.Scatter(
        x=selected_data["Number of threads"],
        y=selected_data["Real time used"],
        mode='markers+lines',
        name=f'{selected_sheet_name} Temps vs Threads',
        marker=dict(size=10, color=color_map[selected_sheet_name]),
        line=dict(width=3, color=color_map[selected_sheet_name]),
    )
)

# Ajouter une annotation pour la valeur minimale
fig_single.add_annotation(
    x=min_time_row["Number of threads"],
    y=min_time_row["Real time used"],
    text=f"Minimum temps<br>{min_time_row['Number of threads'].astype(int)} Threads<br>{min_time_row['Real time used']} sec",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    ax=50,
    ay=-200,
    font=dict(size=14, color="black"),
    arrowcolor="red"
)

# Configuration du layout
fig_single.update_layout(
    title=dict(
        text=f"📈 Temps d'exécution pour {selected_sheet_name}",
        font=dict(size=20, color="black"),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        title="Nombre de threads",
        titlefont=dict(size=16, color="black"),
        tickfont=dict(size=12, color="black"),
        gridcolor='lightgrey'
    ),
    yaxis=dict(
        title="Temps d'exécution (secondes)",
        titlefont=dict(size=16, color="black"),
        tickfont=dict(size=12, color="black"),
        gridcolor='lightgrey'
    ),
    legend=dict(
        title=dict(text="OS-CPU", font=dict(color="black")),
        font=dict(color="black")
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=1080,
    width=1920,
    margin=dict(l=50, r=50, t=50, b=50)
)


st.plotly_chart(fig_single, use_container_width=True)

# Comparison graph
if comparison:
    st.subheader("🔄 Comparaison entre les deux OS-CPU")
    fig_comparison = go.Figure()

    fig_comparison.add_trace(
        go.Scatter(
            x=sheet1["Number of threads"],
            y=sheet1["Real time used"],
            mode='markers+lines',
            name="MACOS-M1PRO",
            marker=dict(size=8, color=color_map["MACOS-M1PRO"]),
            line=dict(width=2, color=color_map["MACOS-M1PRO"])
        )
    )
    fig_comparison.add_trace(
        go.Scatter(
            x=sheet2["Number of threads"],
            y=sheet2["Real time used"],
            mode='markers+lines',
            name="UBUNTU-I7",
            marker=dict(size=8, color=color_map["UBUNTU-I7"]),
            line=dict(width=2, color=color_map["UBUNTU-I7"])
        )
    )

    # Configuration du layout pour la comparaison
    fig_comparison.update_layout(
        title=dict(
            text="📊 Comparaison : Temps d'exécution pour les deux OS-CPU",
            font=dict(size=20, color="black"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title="Nombre de threads",
            titlefont=dict(size=16, color="black"),
            tickfont=dict(size=12, color="black"),
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            title="Temps d'exécution (secondes)",
            titlefont=dict(size=16, color="black"),
            tickfont=dict(size=12, color="black"),
            gridcolor='lightgrey'
        ),
        legend=dict(
            title=dict(text="OS-CPU", font=dict(color="black")),
            font=dict(color="black")
        ),
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=1080,
        width=1920,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    st.plotly_chart(fig_comparison, use_container_width=True)
