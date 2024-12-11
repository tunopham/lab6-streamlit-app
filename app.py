import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Threads vs Temps d'exécution",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Threads vs Temps d'exécution")
st.markdown(
    """
    Cette application permet de visualiser les relations entre le nombre de threads et le temps d'exécution.
    """
)

# Sidebar for navigation
st.sidebar.title("🔧 Options")
sheet_selection = st.sidebar.radio("📋 Sélectionnez OS-CPU :", ["MACOS-M1PRO", "UBUNTU-I7"])
comparison = st.sidebar.checkbox("🔄 Comparer les deux OS-CPU")
st.sidebar.markdown(
    """
    **Astuce :** They are interactive graphs 😍
    """
)

# Load the data
EXCEL_FILE_PATH = "./execution_time.xlsx"

def load_data():
    excel_data = pd.ExcelFile(EXCEL_FILE_PATH)
    sheet1 = excel_data.parse(sheet_name="MACOS-M1PRO")
    sheet2 = excel_data.parse(sheet_name="UBUNTU-I7")
    return sheet1, sheet2

sheet1, sheet2 = load_data()

# Determine selected data
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

# Add annotation for the minimum value
fig_single.add_annotation(
    x=min_time_row["Number of threads"],
    y=min_time_row["Real time used"],
    text=f"Minimum Temps<br>{min_time_row['Number of threads']} Threads<br>{min_time_row['Real time used']} sec",
    showarrow=True,
    arrowhead=2,
    ax=70,
    ay=-50,
    font=dict(size=14, color="black"),
    arrowcolor=color_map[selected_sheet_name]
)

fig_single.update_layout(
    title=dict(
        text=f"📈 Temps d'exécution pour {selected_sheet_name}",
        font=dict(size=20, color="darkblue"),
        x=0.3
    ),
    xaxis=dict(
        title="Nombre de threads",
        titlefont=dict(size=16),
        tickfont=dict(size=12),
        gridcolor='lightgrey'
    ),
    yaxis=dict(
        title="Temps d'exécution (secondes)",
        titlefont=dict(size=16),
        tickfont=dict(size=12),
        gridcolor='lightgrey'
    ),
    template="plotly_white",
    height=600,
    width=900,
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

    fig_comparison.update_layout(
        title=dict(
            text="📊 Comparaison : Temps d'exécution pour les deux OS-CPU",
            font=dict(size=20, color="darkblue"),
            x=0.2
        ),
        xaxis=dict(
            title="Nombre de threads",
            titlefont=dict(size=16),
            tickfont=dict(size=12),
            gridcolor='lightgrey'
        ),
        yaxis=dict(
            title="Temps d'exécution (secondes)",
            titlefont=dict(size=16),
            tickfont=dict(size=12),
            gridcolor='lightgrey'
        ),
        legend=dict(
            title=dict(text="OS-CPU"),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1
        ),
        template="plotly_white",
        height=600,
        width=900,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    st.plotly_chart(fig_comparison, use_container_width=True)
