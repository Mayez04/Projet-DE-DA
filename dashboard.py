import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration de la page avec un thème personnalisé
st.set_page_config(
    page_title="📚 Dashboard Éducation Mondiale",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
    <style>
    .main {
        padding: 0.5rem;
        background-color: #f8f9fa;
    }
    div[data-testid="stHeader"] {
        background-color: transparent;
        display: none;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 2.5rem !important;
        padding: 1rem 0;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
        background: linear-gradient(45deg, #1f77b4, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: rgba(248, 249, 250, 0.95);
    }
    .stSidebar {
        background-color: #2c3e50;
        padding: 1.5rem;
    }
    .stRadio > label {
        background-color: #34495e;
        padding: 1rem;
        border-radius: 5px;
        color: white !important;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .stRadio > label:hover {
        background-color: #3498db;
    }    /* Styles pour les graphiques */
    .stPlotlyChart {
        background-color: white;
        border-radius: 8px;
        padding: 0.3rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 0.8rem 0;
        width: 100% !important;
        height: auto !important;
        transition: transform 0.2s ease;
    }
    .stPlotlyChart:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    /* Section titres pour les graphiques */
    .section-title {
        color: #2c3e50;
        font-size: 1.5rem !important;
        margin: 1.5rem 0 0.8rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #3498db;
    }
    /* Ajustement de la mise en page */
    .row-widget.stRadio > div {
        flex-direction: column;
        width: 100%;
    }
    /* Style pour les colonnes */
    div.row-widget.stHorizontal {
        gap: 0.8rem;
    }
    /* Correction pour les conteneurs de graphiques */
    .js-plotly-plot, .plot-container {
        width: 100% !important;
        max-height: 450px !important;
    }
    /* Style pour le conteneur principal */
    .block-container {
        padding: 1rem 1rem 3rem 1rem;
        max-width: 1400px !important;
        margin: 0 auto;
    }
    /* Style pour les markdown headers */
    .css-10trblm {
        margin: 0;
        font-size: 1.1rem;
        color: #34495e;
    }
    /* Animation pour le chargement des graphiques */
    .element-container {
        opacity: 0;
        animation: fadeIn 0.5s ease-in forwards;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        width: 300px;
        margin: 20px auto;
        display: block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/combined_data.csv')
    return df

df = load_data()

# En-tête du dashboard
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🌍 Analyse de l'Éducation Mondiale</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Une exploration interactive des tendances éducatives globales</p>", unsafe_allow_html=True)

# Filtres globaux dans la barre latérale
st.sidebar.markdown("## 🎯 Filtres")

# Filtre des régions
all_regions = sorted(df['region'].unique())
selected_regions = st.sidebar.multiselect(
    "Sélectionner les régions",
    options=all_regions,
    default=all_regions,
    help="Filtrer les données par région"
)

# Filtre des années
years = sorted(df['year'].unique())
min_year, max_year = st.sidebar.select_slider(
    "Sélectionner la période",
    options=years,
    value=(min(years), max(years)),
    help="Filtrer les données par période"
)

# Appliquer les filtres au dataframe
filtered_df = df[
    (df['region'].isin(selected_regions)) &
    (df['year'].between(min_year, max_year))
]

# Sidebar améliorée avec des icônes et un style personnalisé
st.sidebar.markdown("<h2 style='text-align: center; color: blue;'>🎯 Navigation</h2>", unsafe_allow_html=True)

hypotheses = {
    "Hypothèse 1: Impact de l'investissement": "💰",
    "Hypothèse 2: Impact de la richesse": "📈",
    "Hypothèse 3: Inégalités de genre": "⚖️",
    "Hypothèse 4: Bénéfices démographiques": "👥",
    "Hypothèse 5: Mobilité internationale": "🌏",
    "Analyse de la Tunisie": "🇹🇳",
    "Recommandations": "🎯"
}

selected_hypothesis = st.sidebar.radio(
    "",
    list(hypotheses.keys()),
    format_func=lambda x: f"{hypotheses[x]} {x}"
)

# Ajout d'une description de l'hypothèse sélectionnée
descriptions = {
    "Hypothèse 1: Impact de l'investissement": "Analyse de l'influence des investissements éducatifs sur la qualité de l'enseignement",
    "Hypothèse 2: Impact de la richesse": "Étude de la relation entre la richesse nationale et les résultats éducatifs",
    "Hypothèse 3: Inégalités de genre": "Examen des disparités de genre dans l'accès à l'éducation",
    "Hypothèse 4: Bénéfices démographiques": "Impact de l'éducation sur les indicateurs démographiques",
    "Hypothèse 5: Mobilité internationale": "Analyse des flux d'étudiants internationaux",
    "Analyse de la Tunisie": "Analyse détaillée des indicateurs éducatifs de la Tunisie",
    "Recommandations": "Propositions pour améliorer les systèmes éducatifs mondiaux"
}

st.sidebar.markdown(f"""
    <div style='background-color: #34495e; padding: 1rem; border-radius: 5px; margin-top: 2rem;'>
        <h4 style='color: #3498db;'>Description</h4>
        <p style='color: white;'>{descriptions[selected_hypothesis]}</p>
    </div>
""", unsafe_allow_html=True)

# Palette de couleurs personnalisée
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Configuration des graphiques
PLOT_CONFIG = {
    'template': 'plotly_white',
    'font': dict(family="Roboto, sans-serif", size=12),
    'showlegend': True,
    'height': 450,  # Hauteur réduite
    'width': 450,
    'margin': dict(l=40, r=40, t=60, b=40),  # Marges réduites
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'autosize': False
}

def create_bar_plot(data, x, y, title, color=None):
    fig = px.bar(data, x=x, y=y, color=color if color else None,
                 title=title,
                 color_discrete_sequence=COLORS,
                 height=450)  # Hauteur réduite
    
    fig.update_layout(
        **PLOT_CONFIG,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        xaxis_title=dict(text=x.replace('_', ' ').title(), font=dict(size=16)),
        yaxis_title=dict(text=y.replace('_', ' ').title(), font=dict(size=16)),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )
    return fig

import plotly.graph_objects as go

def create_scatter_plot(data, x, y, title, color=None):
    fig = go.Figure()

    # Tracer les lignes et les points, regroupés par couleur si spécifié
    if color:
        for val in data[color].unique():
            sub_data = data[data[color] == val].sort_values(by=x)
            fig.add_trace(go.Scatter(
                x=sub_data[x],
                y=sub_data[y],
                mode='lines+markers',
                name=str(val),
                line=dict(width=2),
                marker=dict(size=8, opacity=0.8),
            ))
    else:
        sorted_data = data.sort_values(by=x)
        fig.add_trace(go.Scatter(
            x=sorted_data[x],
            y=sorted_data[y],
            mode='lines+markers',
            name='',
            line=dict(width=2),
            marker=dict(size=8, opacity=0.8),
        ))

    fig.update_layout(
        **PLOT_CONFIG,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        xaxis_title=dict(text=x.replace('_', ' ').title(), font=dict(size=16)),
        yaxis_title=dict(text=y.replace('_', ' ').title(), font=dict(size=16)),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )

    # Marges
    fig.update_layout(
        xaxis_range=[
            data[x].min() - (data[x].max() - data[x].min()) * 0.05,
            data[x].max() + (data[x].max() - data[x].min()) * 0.05
        ],
        yaxis_range=[
            data[y].min() - (data[y].max() - data[y].min()) * 0.05,
            data[y].max() + (data[y].max() - data[y].min()) * 0.05
        ]
    )

    return fig


def create_scatter_plot_no_line(data, x, y, title, color=None):
    fig = px.scatter(data, x=x, y=y, color=color if color else None,
                    title=title,
                    color_discrete_sequence=COLORS,
                    opacity=0.8,
                    size_max=15,
                    height=450,
                    render_mode='webgl',
                    trendline="ols")  # Ajout de la ligne d'ajustement
    
    fig.update_layout(
        **PLOT_CONFIG,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        xaxis_title=dict(text=x.replace('_', ' ').title(), font=dict(size=16)),
        yaxis_title=dict(text=y.replace('_', ' ').title(), font=dict(size=16)),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )
    
    # Ajouter des marges pour éviter le chevauchement des points
    fig.update_layout(
        xaxis_range=[
            data[x].min() - (data[x].max() - data[x].min()) * 0.05,
            data[x].max() + (data[x].max() - data[x].min()) * 0.05
        ],
        yaxis_range=[
            data[y].min() - (data[y].max() - data[y].min()) * 0.05,
            data[y].max() + (data[y].max() - data[y].min()) * 0.05
        ]
    )
    
    return fig

def create_scatter_plot_no_line_no_trendline(data, x, y, title, color=None):
    fig = px.scatter(data, x=x, y=y, color=color if color else None,
                    title=title,
                    color_discrete_sequence=COLORS,
                    opacity=0.8,
                    size_max=15,
                    height=450,
                    render_mode='webgl')
    
    fig.update_layout(
        **PLOT_CONFIG,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        xaxis_title=dict(text=x.replace('_', ' ').title(), font=dict(size=16)),
        yaxis_title=dict(text=y.replace('_', ' ').title(), font=dict(size=16)),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )
    
    # Ajouter des marges pour éviter le chevauchement des points
    fig.update_layout(
        xaxis_range=[
            data[x].min() - (data[x].max() - data[x].min()) * 0.05,
            data[x].max() + (data[x].max() - data[x].min()) * 0.05
        ],
        yaxis_range=[
            data[y].min() - (data[y].max() - data[y].min()) * 0.05,
            data[y].max() + (data[y].max() - data[y].min()) * 0.05
        ]
    )
    
    return fig

def create_log_scatter_plot(data, x, y, title, color=None):
    """
    Crée un graphique de dispersion avec l'axe x en échelle logarithmique,
    similaire au graphique de l'EDA.ipynb.
    """
    # Créer une copie des données pour éviter de modifier l'original
    plot_data = data.copy()
    
    # Appliquer le log sur la variable x
    plot_data['log_x'] = np.log(plot_data[x])
    
    # Créer le graphique
    fig = px.scatter(plot_data, 
                    x='log_x', 
                    y=y, 
                    color=color if color else None,
                    title=title,
                    color_discrete_sequence=COLORS,
                    opacity=0.8,
                    size_max=15,
                    height=450,
                    render_mode='webgl',
                    trendline="ols")
    
    fig.update_layout(
        **PLOT_CONFIG,
        title=dict(
            text=f"<b>{title}</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        xaxis_title=dict(text=f"Log({x.replace('_', ' ').title()})", font=dict(size=16)),
        yaxis_title=dict(text=y.replace('_', ' ').title(), font=dict(size=16)),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )
    
    # Ajouter des marges pour éviter le chevauchement des points
    fig.update_layout(
        xaxis_range=[
            plot_data['log_x'].min() - (plot_data['log_x'].max() - plot_data['log_x'].min()) * 0.05,
            plot_data['log_x'].max() + (plot_data['log_x'].max() - plot_data['log_x'].min()) * 0.05
        ],
        yaxis_range=[
            plot_data[y].min() - (plot_data[y].max() - plot_data[y].min()) * 0.05,
            plot_data[y].max() + (plot_data[y].max() - plot_data[y].min()) * 0.05
        ]
    )
    
    return fig

# Hypothèse 1: Impact de l'investissement dans l'éducation
if selected_hypothesis == "Hypothèse 1: Impact de l'investissement":
    st.title("Impact de l'investissement dans l'éducation")
    
    # Évolution temporelle des dépenses en éducation
    st.markdown("### 📈 Évolution temporelle des dépenses en éducation")
    evolution_data = filtered_df.groupby(['year', 'region'])['education_expenditure_gdp'].mean().reset_index()
    fig1 = create_scatter_plot(evolution_data, 'year', 'education_expenditure_gdp', 'Évolution des dépenses en éducation par région', 'region')
    st.plotly_chart(fig1, use_container_width=True)

    # Dépenses vs taux d'achèvement
    st.markdown("### 🎯 Dépenses en éducation vs Taux d'achèvement du primaire")
    fig2 = create_scatter_plot_no_line(
        filtered_df,
        'education_expenditure_gdp',
        'primary_completion_rate',
        "Dépenses en éducation vs Taux d'achèvement du primaire",
        'region'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_expenditure_completion"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Corrélation positive entre dépenses et réussite scolaire</li>
                        <li style='margin-bottom: 10px;'>• Le niveau d'investissement impacte directement les résultats éducatifs</li>
                        <li style='margin-bottom: 10px;'>• Les pays qui investissent plus obtiennent généralement de meilleurs résultats</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Années d'éducation gratuite vs Espérance de vie scolaire
    st.markdown("### 📚 Années d'éducation gratuite vs Espérance de vie scolaire")
    fig3 = create_scatter_plot_no_line(
        filtered_df,
        'free_education_years',
        'school_life_expectancy',
        "Années d'éducation gratuite vs Espérance de vie scolaire",
        'region'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_free_education"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• L'éducation gratuite prolongée favorise une scolarité plus longue</li>
                        <li style='margin-bottom: 10px;'>• Impact direct des politiques de gratuité sur la durée des études</li>
                        <li style='margin-bottom: 10px;'>• Les régions avec plus d'années gratuites ont une meilleure rétention scolaire</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Hypothèse 2: Impact de la richesse
elif selected_hypothesis == "Hypothèse 2: Impact de la richesse":
    st.title("Impact de la richesse sur l'éducation")
    
    # GNI vs espérance de vie scolaire (échelle logarithmique)
    st.markdown("### 📚 GNI par habitant vs Espérance de vie scolaire")
    fig1 = create_log_scatter_plot(
        filtered_df,
        'gni_per_capita',
        'school_life_expectancy',
        'GNI par habitant vs Espérance de vie scolaire',
        'region'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bouton d'interprétation pour la première visualisation
    if st.button("📊 Interprétations", key="interpretation_gni_life"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Corrélation positive forte entre richesse et durée de scolarisation</li>
                        <li style='margin-bottom: 10px;'>• Les pays riches maintiennent leurs élèves plus longtemps dans le système éducatif</li>
                        <li style='margin-bottom: 10px;'>• Effet de plateau visible pour les pays à haut revenu</li>
                        <li style='margin-bottom: 10px;'>• Différences marquées entre régions, même à niveau de GNI comparable</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # GNI vs taux d'achèvement (échelle logarithmique)
    st.markdown("### 🎯 GNI par habitant vs Taux d'achèvement du primaire")
    fig2 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'gni_per_capita',
        'primary_completion_rate',
        'GNI par habitant vs Taux d\'achèvement du primaire',
        'region'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_gni_completion"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Relation positive entre richesse nationale et réussite scolaire</li>
                        <li style='margin-bottom: 10px;'>• Les pays riches atteignent presque tous 100% d'achèvement</li>
                        <li style='margin-bottom: 10px;'>• Grande dispersion pour les pays à faible revenu</li>
                        <li style='margin-bottom: 10px;'>• Les ressources financières influencent la capacité à maintenir les élèves jusqu'à la fin du primaire</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### GNI par habitant vs Ratio élèves/enseignant")
    fig3 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'gni_per_capita',
        'student_teacher_ratio_primary',
        'GNI par habitant vs Ratio élèves/enseignant',
        'region'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_gni_ratio"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Corrélation négative claire : plus le pays est riche, plus le ratio est faible</li>
                        <li style='margin-bottom: 10px;'>• Les pays riches peuvent investir dans plus d'enseignants</li>
                        <li style='margin-bottom: 10px;'>• Meilleure qualité d'encadrement dans les pays à haut revenu</li>
                        <li style='margin-bottom: 10px;'>• Surcharge des classes dans les pays à faible revenu</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Hypothèse 3: Inégalités de genre
elif selected_hypothesis == "Hypothèse 3: Inégalités de genre":
    st.title("Inégalités de genre dans l'éducation")
    
    # Évolution des ratios filles/garçons
    st.markdown("### 📈 Évolution des ratios filles/garçons selon le niveau d'enseignement")
    
    # Préparer les données pour le boxplot
    ratios_data = pd.melt(filtered_df, 
                         value_vars=['gender_ratio_primary', 
                                   'gender_ratio_secondary',
                                   'gender_ratio_tertiary'],
                         var_name='education_level',
                         value_name='ratio')
    
    # Créer le boxplot avec Plotly
    fig = go.Figure()
    
    # Ajouter les boxplots pour chaque niveau d'éducation
    education_levels = {
        'gender_ratio_primary': 'Primaire',
        'gender_ratio_secondary': 'Secondaire',
        'gender_ratio_tertiary': 'Tertiaire'
    }
    
    for level, name in education_levels.items():
        fig.add_trace(go.Box(
            y=filtered_df[level],
            name=name,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(
                color=COLORS[list(education_levels.keys()).index(level) % len(COLORS)],
                size=4,
                opacity=0.7
            ),
            boxmean=True
        ))
    
    # Ajouter une ligne horizontale à y=1 pour indiquer la parité
    fig.add_hline(y=1, line_dash="dash", line_color="red", 
                 annotation_text="Parité", 
                 annotation_position="right")
    
    # Mettre à jour la mise en page
    fig.update_layout(
        template='plotly_white',
        font=dict(family="Roboto, sans-serif", size=12),
        height=450,
        width=450,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        title=dict(
            text="<b>Évolution des ratios filles/garçons selon le niveau d'enseignement</b>",
            x=0,
            y=0.95,
            font=dict(size=24, family="Roboto, sans-serif")
        ),
        yaxis_title="Ratio filles/garçons",
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto"
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Bouton d'interprétation pour la première visualisation
    if st.button("📊 Interprétations", key="interpretation_gender_evolution"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Les inégalités de genre augmentent avec le niveau d'enseignement (primaire → secondaire → tertiaire)</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Distribution des ratios par région et niveau
    st.markdown("### 📊 Distribution des ratios par région et niveau")
    ratios_data = pd.melt(filtered_df, 
                         value_vars=['gender_ratio_primary', 
                                   'gender_ratio_secondary',
                                   'gender_ratio_tertiary'],
                         var_name='education_level',
                         value_name='ratio')
    
    fig = px.box(ratios_data, 
                 x='education_level', 
                 y='ratio',
                 color='education_level',
                 title="Distribution des ratios filles/garçons par niveau d'éducation")
    fig.add_hline(y=1, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_gender_distribution"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Les disparités augmentent avec le niveau d'éducation</li>
                        <li style='margin-bottom: 10px;'>• Le primaire présente généralement moins d'inégalités</li>
                        <li style='margin-bottom: 10px;'>• L'enseignement supérieur montre les écarts les plus importants</li>
                        <li style='margin-bottom: 10px;'>• Les différences régionales sont plus marquées dans le secondaire et le tertiaire</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Relation entre parité et taux d'achèvement
    st.markdown("### 🎯 Relation entre parité et taux d'achèvement")
    fig = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'gender_ratio_primary',
        'primary_completion_rate',
        'Parité de genre vs Taux d\'achèvement du primaire',
        'region'
    )
    fig.add_vline(x=1, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_gender_completion"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Les pays atteignant la parité ont de meilleurs taux d'achèvement</li>
                        <li style='margin-bottom: 10px;'>• L'égalité de genre va de pair avec la performance éducative</li>
                        <li style='margin-bottom: 10px;'>• La discrimination de genre impacte négativement les résultats scolaires</li>
                        <li style='margin-bottom: 10px;'>• L'inclusion favorise la réussite éducative</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Hypothèse 4: Bénéfices démographiques
elif selected_hypothesis == "Hypothèse 4: Bénéfices démographiques":
    st.title("Bénéfices démographiques de l'éducation")
    
    # Espérance de vie scolaire vs taux de fécondité
    st.markdown("### 👶 Espérance de vie scolaire vs Taux de fécondité")
    fig1 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'school_life_expectancy',
        'fertility_rate',
        'Espérance de vie scolaire vs Taux de fécondité',
        'region'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bouton d'interprétation pour la première visualisation
    if st.button("📊 Interprétations", key="interpretation_fertility"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Forte corrélation négative entre durée de scolarisation et fécondité</li>
                        <li style='margin-bottom: 10px;'>• Plus l'éducation est longue, moins le taux de fécondité est élevé</li>
                        <li style='margin-bottom: 10px;'>• Relation constante à travers toutes les régions</li>
                        <li style='margin-bottom: 10px;'>• Impact significatif de l'éducation sur le contrôle des naissances</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Population vs dépenses par étudiant
    st.markdown("### 💰 Population vs Dépenses publiques par étudiant")
    filtered_df['log_population'] = np.log(filtered_df['total_population'])
    fig2 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'log_population',
        'public_expenditure_per_student',
        'Population vs Dépenses publiques par étudiant',
        'region'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_population_expenditure"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Corrélation négative entre taille de la population et dépenses par étudiant</li>
                        <li style='margin-bottom: 10px;'>• Les grands pays peinent à maintenir des niveaux élevés d'investissement par élève</li>
                        <li style='margin-bottom: 10px;'>• Défi particulier pour les pays très peuplés</li>
                        <li style='margin-bottom: 10px;'>• Les petits pays peuvent souvent investir davantage par étudiant</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Top 10 pays qui dépensent le moins par étudiant
    st.markdown("### 📉 Top 7 pays qui dépensent le moins par étudiant")
    top_low_spending = filtered_df.nsmallest(10, 'public_expenditure_per_student')
    fig3 = px.scatter(top_low_spending,
                     x='country_code',
                     y='public_expenditure_per_student',
                     size='total_population',
                     color='region',
                     title="Top 7 pays qui dépensent le moins par étudiant",
                     size_max=50)
    fig3.update_layout(**PLOT_CONFIG)
    st.plotly_chart(fig3, use_container_width=True)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_low_spending"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Concentration dans les régions en développement</li>
                        <li style='margin-bottom: 10px;'>• Présence marquée de pays à forte population</li>
                        <li style='margin-bottom: 10px;'>• Difficultés structurelles à financer l'éducation</li>
                        <li style='margin-bottom: 10px;'>• Impact sur la qualité de l'enseignement</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Hypothèse 5: Mobilité internationale
elif selected_hypothesis == "Hypothèse 5: Mobilité internationale":
    st.title("Mobilité internationale des étudiants")
    
    # Matrice de corrélation
    st.markdown("### 📊 Corrélations entre mobilité et indicateurs")
    mobility_vars = ["inbound_mobility_rate", "outbound_mobility_rate", 
                    "gni_per_capita", "education_expenditure_gdp", 
                    "school_life_expectancy", "primary_completion_rate"]
    
    corr_matrix = filtered_df[mobility_vars].corr()
    
    var_names = {
        "inbound_mobility_rate": "Mobilité entrante",
        "outbound_mobility_rate": "Mobilité sortante",
        "gni_per_capita": "GNI par habitant",
        "education_expenditure_gdp": "Dépenses éducation",
        "school_life_expectancy": "Durée scolarité",
        "primary_completion_rate": "Achèvement primaire"
    }
    
    corr_matrix.index = [var_names[col] for col in corr_matrix.index]
    corr_matrix.columns = [var_names[col] for col in corr_matrix.columns]
    
    fig1 = px.imshow(corr_matrix,
                    labels=dict(color="Correlation"),
                    title="Corrélations entre mobilité et indicateurs éducatifs/économiques",
                    color_continuous_scale="RdBu",
                    aspect="auto")
    fig1.update_layout(**PLOT_CONFIG)
    st.plotly_chart(fig1, use_container_width=True)

    # Bouton d'interprétation pour la première visualisation
    if st.button("📊 Interprétations", key="interpretation_correlation"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Forte corrélation positive entre la mobilité entrante et le GNI per capita</li>
                        <li style='margin-bottom: 10px;'>• Lien significatif avec les dépenses en éducation</li>
                        <li style='margin-bottom: 10px;'>• Les pays développés attirent plus d'étudiants internationaux</li>
                        <li style='margin-bottom: 10px;'>• La qualité de l'éducation influence l'attractivité internationale</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Inbound mobility vs GNI
    st.markdown("### 💰 Mobilité entrante vs GNI par habitant")
    fig2 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'gni_per_capita',
        'inbound_mobility_rate',
        'GNI par habitant vs Taux de mobilité entrante',
        'region'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_mobility_gni"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Les pays riches attirent plus d'étudiants internationaux</li>
                        <li style='margin-bottom: 10px;'>• Concentration des flux dans les pays à haut revenu</li>
                        <li style='margin-bottom: 10px;'>• Relation directe entre richesse nationale et attractivité éducative</li>
                        <li style='margin-bottom: 10px;'>• Les moyens financiers permettent de meilleures conditions d'accueil</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Inbound mobility vs dépenses par étudiant
    st.markdown("### 📚 Mobilité entrante vs Dépenses par étudiant")
    fig3 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'public_expenditure_per_student',
        'inbound_mobility_rate',
        'Dépenses par étudiant vs Taux de mobilité entrante',
        'region'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_mobility_expenditure"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Corrélation positive entre investissement et attractivité</li>
                        <li style='margin-bottom: 10px;'>• Les pays investissant plus attirent plus d'étudiants</li>
                        <li style='margin-bottom: 10px;'>• Importance des moyens alloués par étudiant</li>
                        <li style='margin-bottom: 10px;'>• La qualité des conditions d'études comme facteur d'attractivité</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Inbound mobility vs ratio filles/garçons tertiaire
    st.markdown("### ⚖️ Mobilité entrante vs Parité de genre (Tertiaire)")
    fig4 = create_scatter_plot_no_line_no_trendline(
        filtered_df,
        'gender_ratio_tertiary',
        'inbound_mobility_rate',
        'Parité de genre (Tertiaire) vs Taux de mobilité entrante',
        'region'
    )
    fig4.add_vline(x=1, line_dash="dash", line_color="red")
    st.plotly_chart(fig4, use_container_width=True)

    # Bouton d'interprétation pour la quatrième visualisation
    if st.button("📊 Interprétations", key="interpretation_mobility_gender"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Meilleure parité dans les pays attractifs</li>
                        <li style='margin-bottom: 10px;'>• L'égalité des genres comme indicateur de développement</li>
                        <li style='margin-bottom: 10px;'>• Environnement éducatif plus inclusif</li>
                        <li style='margin-bottom: 10px;'>• Attrait des systèmes éducatifs équitables</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Ajouter la nouvelle section pour la Tunisie
elif selected_hypothesis == "Analyse de la Tunisie":
    st.title("🇹🇳 Analyse de l'Éducation en Tunisie")
    
    # Filtrer les données pour la Tunisie
    tunisia_df = filtered_df[filtered_df['country_code'] == 'TUN'].copy()
    
    import matplotlib.pyplot as plt

# Création d'une figure avec 4 sous-graphiques
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1. Dépenses en éducation (% du PIB)
    countries = df[df['country_code'] == 'TN']['education_expenditure_gdp'].mean()
    regional = df[df['region'] == 'Africa']['education_expenditure_gdp'].mean()
    bars1 = ax1.bar(['Tunisie', 'Afrique'], [countries, regional], color=['#1f77b4', '#ff7f0e'])
    ax1.set_title('📊 Dépenses en éducation (% du PIB)')
    ax1.set_ylabel('% du PIB')
    for bar in bars1:
     height = bar.get_height()
     ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}%', ha='center', va='bottom')

# 2. Taux d'achèvement du primaire
    tn_completion = df[df['country_code'] == 'TN']['primary_completion_rate'].mean()
    africa_completion = df[df['region'] == 'Africa']['primary_completion_rate'].mean()
    bars2 = ax2.bar(['Tunisie', 'Afrique'], [tn_completion, africa_completion], color=['#2ca02c', '#d62728'])
    ax2.set_title("🎓 Taux d'achèvement du primaire")
    ax2.set_ylabel('Taux (%)')
    for bar in bars2:
     height = bar.get_height()
     ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom')

# 3. Espérance de vie scolaire
    tn_life = df[df['country_code'] == 'TN']['school_life_expectancy'].mean()
    africa_life = df[df['region'] == 'Africa']['school_life_expectancy'].mean()
    bars3 = ax3.bar(['Tunisie', 'Afrique'], [tn_life, africa_life], color=['#9467bd', '#8c564b'])
    ax3.set_title('📚 Espérance de vie scolaire')
    ax3.set_ylabel('Années')
    for bar in bars3:
     height = bar.get_height()
     ax3.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# 4. Ratio élèves/enseignant (primaire)
    tn_ratio = df[df['country_code'] == 'TN']['student_teacher_ratio_primary'].mean()
    africa_ratio = df[df['region'] == 'Africa']['student_teacher_ratio_primary'].mean()
    bars4 = ax4.bar(['Tunisie', 'Afrique'], [tn_ratio, africa_ratio], color=['#17becf', '#e377c2'])
    ax4.set_title('👨‍🏫 Ratio élèves/enseignant (primaire)')
    ax4.set_ylabel("Nombre d'élèves par enseignant")
    for bar in bars4:
     height = bar.get_height()
     ax4.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# Affichage propre
    plt.tight_layout()

# ➤ Affichage avec Streamlit
    st.markdown("### 📊 Comparaison de l'éducation : Tunisie vs Afrique")
    st.pyplot(fig)

    # Bouton d'interprétation pour la première visualisation
    if st.button("📊 Interprétations", key="interpretation_education"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• La Tunisie investit plus que la moyenne africaine dans l'éducation</li>
                        <li style='margin-bottom: 10px;'>• Meilleurs résultats en termes de taux d'achèvement et d'espérance de vie scolaire</li>
                        <li style='margin-bottom: 10px;'>• Ratio élèves/enseignant plus favorable que la moyenne régionale</li>
                        <li style='margin-bottom: 10px;'>• Position relativement avantageuse dans le contexte africain</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

#VIZ 2
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

# --- Titre ---
    st.markdown("### 💰 GNI par habitant : Tunisie vs Afrique")

# --- Calcul des moyennes ---
    tn_gni = df[df['country_code'] == 'TN']['gni_per_capita'].mean()
    africa_gni = df[df['region'] == 'Africa']['gni_per_capita'].mean()

# --- Création de la figure ---
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(['Tunisie', 'Afrique'], [tn_gni, africa_gni], color=['#1f77b4', '#ff7f0e'])

# --- Titre et étiquettes ---
    ax.set_title('GNI par habitant', fontsize=16)
    ax.set_ylabel('USD', fontsize=12)

# --- Ajout des valeurs au-dessus des barres ---
    for bar in bars:
     height = bar.get_height()
     ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', 
            ha='center', va='bottom', fontsize=11)

# --- Apparence ---
    ax.grid(True, axis='y', alpha=0.3)

# --- Affichage avec Streamlit ---
    st.pyplot(fig)

    # Bouton d'interprétation pour la deuxième visualisation
    if st.button("📊 Interprétations", key="interpretation_gni"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• GNI par habitant supérieur à la moyenne africaine</li>
                        <li style='margin-bottom: 10px;'>• Position intermédiaire dans le contexte régional</li>
                        <li style='margin-bottom: 10px;'>• Meilleurs indicateurs éducatifs que la moyenne régionale</li>
                        <li style='margin-bottom: 10px;'>• Potentiel de développement encore important par rapport aux standards internationaux</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    #VIZ 3 
    st.markdown("### 👧👦 Comparaison des ratios filles/garçons par niveau d'éducation")

# --- Calcul des moyennes Tunisie ---
    tn_primary = df[df['country_code'] == 'TN']['gender_ratio_primary'].mean()
    tn_secondary = df[df['country_code'] == 'TN']['gender_ratio_secondary'].mean()
    tn_tertiary = df[df['country_code'] == 'TN']['gender_ratio_tertiary'].mean()

# --- Calcul des moyennes Afrique ---
    africa_primary = df[df['region'] == 'Africa']['gender_ratio_primary'].mean()
    africa_secondary = df[df['region'] == 'Africa']['gender_ratio_secondary'].mean()
    africa_tertiary = df[df['region'] == 'Africa']['gender_ratio_tertiary'].mean()

# --- Préparation des données ---
    x = np.arange(3)
    width = 0.35

# --- Création du graphique ---
    fig, ax = plt.subplots(figsize=(12, 6))

# Barres
    bars1 = ax.bar(x - width/2, [tn_primary, tn_secondary, tn_tertiary], width, label='Tunisie', color='skyblue')
    bars2 = ax.bar(x + width/2, [africa_primary, africa_secondary, africa_tertiary], width, label='Afrique', color='lightcoral')

# Ligne de parité
    ax.axhline(y=1, color='gray', linestyle='--', label='Parité parfaite')

# Titre et étiquettes
    ax.set_title("Comparaison des ratios filles/garçons par niveau d'éducation", fontsize=16)
    ax.set_xlabel("Niveau d'éducation", fontsize=12)
    ax.set_ylabel("Ratio filles/garçons", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(['Primaire', 'Secondaire', 'Tertiaire'])
    ax.legend()

# Valeurs au-dessus des barres
    for i in x:
        ax.text(i - width/2, [tn_primary, tn_secondary, tn_tertiary][i], 
            f'{[tn_primary, tn_secondary, tn_tertiary][i]:.2f}', ha='center', va='bottom', fontsize=10)
        ax.text(i + width/2, [africa_primary, africa_secondary, africa_tertiary][i], 
            f'{[africa_primary, africa_secondary, africa_tertiary][i]:.2f}', ha='center', va='bottom', fontsize=10)

# Apparence
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

# --- Affichage Streamlit ---
    st.pyplot(fig)

    # Bouton d'interprétation pour la troisième visualisation
    if st.button("📊 Interprétations", key="interpretation_gender"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Meilleure parité que la moyenne africaine à tous les niveaux</li>
                        <li style='margin-bottom: 10px;'>• Performance particulièrement bonne dans le tertiaire</li>
                        <li style='margin-bottom: 10px;'>• Résultats proches des standards internationaux</li>
                        <li style='margin-bottom: 10px;'>• Politique éducative favorable à l'égalité des genres</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

#VIZ 4
    st.markdown("### 📊 Indicateurs éducatifs et démographiques : Tunisie vs Afrique")

# Création de la figure avec 4 sous-graphes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# --- 1. Espérance de vie scolaire ---
    school_life_tn = df[df['country_code'] == 'TN']['school_life_expectancy'].mean()
    school_life_af = df[df['region'] == 'Africa']['school_life_expectancy'].mean()
    bars1 = ax1.bar(['Tunisie', 'Afrique'], [school_life_tn, school_life_af], color=['#3498db', '#e74c3c'])
    ax1.set_title("Espérance de vie scolaire (années)")
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# --- 2. Taux de fécondité ---
    fertility_tn = df[df['country_code'] == 'TN']['fertility_rate'].mean()
    fertility_af = df[df['region'] == 'Africa']['fertility_rate'].mean()
    bars2 = ax2.bar(['Tunisie', 'Afrique'], [fertility_tn, fertility_af], color=['#3498db', '#e74c3c'])
    ax2.set_title("Taux de fécondité (enfants par femme)")
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# --- 3. Espérance de vie ---
    life_exp_tn = df[df['country_code'] == 'TN']['life_expectancy'].mean()
    life_exp_af = df[df['region'] == 'Africa']['life_expectancy'].mean()
    bars3 = ax3.bar(['Tunisie', 'Afrique'], [life_exp_tn, life_exp_af], color=['#3498db', '#e74c3c'])
    ax3.set_title("Espérance de vie (années)")
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# --- 4. Taux d'achèvement du primaire ---
    completion_tn = df[df['country_code'] == 'TN']['primary_completion_rate'].mean()
    completion_af = df[df['region'] == 'Africa']['primary_completion_rate'].mean()
    bars4 = ax4.bar(['Tunisie', 'Afrique'], [completion_tn, completion_af], color=['#3498db', '#e74c3c'])
    ax4.set_title("Taux d'achèvement du primaire (%)")
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')

# Mise en page générale
    plt.suptitle("Indicateurs éducatifs et démographiques : Tunisie vs Afrique", y=1.02, fontsize=16)
    plt.tight_layout()

# Affichage dans Streamlit
    st.pyplot(fig)

    # Bouton d'interprétation pour la quatrième visualisation
    if st.button("📊 Interprétations", key="interpretation_indicators"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Meilleurs indicateurs que la moyenne africaine :</li>
                        <li style='margin-bottom: 10px;'>  • Espérance de vie scolaire plus élevée</li>
                        <li style='margin-bottom: 10px;'>  • Taux de fécondité plus faible</li>
                        <li style='margin-bottom: 10px;'>  • Meilleure espérance de vie</li>
                        <li style='margin-bottom: 10px;'>  • Taux d'achèvement du primaire supérieur</li>
                        <li style='margin-bottom: 10px;'>• Position intermédiaire favorable dans le contexte régional</li>
                        <li style='margin-bottom: 10px;'>• Impact positif des politiques éducatives sur les indicateurs démographiques</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

#VIZ 5


    st.markdown("### 🌍 Taux de mobilité étudiante : Tunisie vs Afrique")

# Création de la figure avec 2 sous-graphes horizontaux
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- 1. Taux de mobilité entrante ---
    tn_inbound = df[df['country_code'] == 'TN']['inbound_mobility_rate'].mean()
    africa_inbound = df[df['region'] == 'Africa']['inbound_mobility_rate'].mean()
    bars1 = ax1.bar(['Tunisie', 'Afrique'], [tn_inbound, africa_inbound], color=['#2980b9', '#e67e22'])
    ax1.set_title("Taux de mobilité entrante")
    ax1.set_ylabel("Pourcentage")
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}%', ha='center', va='bottom')

# --- 2. Taux de mobilité sortante ---
    tn_outbound = df[df['country_code'] == 'TN']['outbound_mobility_rate'].mean()
    africa_outbound = df[df['region'] == 'Africa']['outbound_mobility_rate'].mean()
    bars2 = ax2.bar(['Tunisie', 'Afrique'], [tn_outbound, africa_outbound], color=['#2980b9', '#e67e22'])
    ax2.set_title("Taux de mobilité sortante")
    ax2.set_ylabel("Pourcentage")
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}%', ha='center', va='bottom')

# Mise en page
    plt.tight_layout()

# Affichage dans Streamlit
    st.pyplot(fig)

    # Bouton d'interprétation pour la cinquième visualisation
    if st.button("📊 Interprétations", key="interpretation_mobility"):
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 5px solid #FF6B6B;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2c3e50; margin-bottom: 15px;'>📊 Interprétation des Résultats</h3>
                <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <ul style='color: #34495e; line-height: 1.8; font-size: 16px; list-style-type: none; padding-left: 0;'>
                        <li style='margin-bottom: 10px;'>• Taux de mobilité entrante supérieur à la moyenne africaine</li>
                        <li style='margin-bottom: 10px;'>• Position relativement attractive dans le contexte régional</li>
                        <li style='margin-bottom: 10px;'>• Équilibre entre mobilité entrante et sortante</li>
                        <li style='margin-bottom: 10px;'>• Potentiel de développement comme hub éducatif régional</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Ajouter la nouvelle section pour les recommandations
elif selected_hypothesis == "Recommandations":
    st.title("🎯 Recommandations pour l'Amélioration des Systèmes Éducatifs")
    
    # Style CSS pour les cartes de recommandations
    st.markdown("""
        <style>
        .recommendation-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }
        .recommendation-card:hover {
            transform: translateY(-5px);
        }
        .recommendation-title {
            color: #2c3e50;
            font-size: 1.5em;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .recommendation-content {
            color: #34495e;
            font-size: 1.1em;
            line-height: 1.6;
        }
        .highlight {
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
            padding: 2px 5px;
            border-radius: 3px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Recommandation 1: Investissement
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">💰 Augmentation des Investissements Éducatifs</div>
            <div class="recommendation-content">
                <ul>
                    <li>Augmenter progressivement les dépenses publiques en éducation vers <span class="highlight">6% du PIB</span></li>
                    <li>Prioriser l'investissement dans les infrastructures et le matériel pédagogique</li>
                    <li>Mettre en place des mécanismes de suivi et d'évaluation des investissements</li>
                    <li>Développer des partenariats public-privé pour le financement de l'éducation</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Recommandation 2: Équité
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">⚖️ Promotion de l'Équité Éducative</div>
            <div class="recommendation-content">
                <ul>
                    <li>Renforcer les politiques d'égalité des genres à tous les niveaux d'éducation</li>
                    <li>Mettre en place des programmes de soutien pour les populations défavorisées</li>
                    <li>Développer des bourses et des aides financières ciblées</li>
                    <li>Promouvoir l'inclusion des personnes en situation de handicap</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Recommandation 3: Qualité
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">📚 Amélioration de la Qualité de l'Enseignement</div>
            <div class="recommendation-content">
                <ul>
                    <li>Réduire le ratio élèves/enseignant à <span class="highlight">20:1</span> maximum</li>
                    <li>Renforcer la formation continue des enseignants</li>
                    <li>Moderniser les méthodes pédagogiques</li>
                    <li>Intégrer les technologies éducatives innovantes</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Recommandation 4: Mobilité
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">🌍 Développement de la Mobilité Internationale</div>
            <div class="recommendation-content">
                <ul>
                    <li>Faciliter les échanges universitaires internationaux</li>
                    <li>Harmoniser les systèmes de reconnaissance des diplômes</li>
                    <li>Développer des programmes de double diplôme</li>
                    <li>Promouvoir la mobilité des enseignants et chercheurs</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Recommandation 5: Innovation
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">💡 Innovation et Adaptation</div>
            <div class="recommendation-content">
                <ul>
                    <li>Intégrer les compétences du 21ème siècle dans les programmes</li>
                    <li>Développer l'apprentissage par projet et l'éducation expérientielle</li>
                    <li>Promouvoir l'entrepreneuriat et l'innovation</li>
                    <li>Adapter les curricula aux besoins du marché du travail</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Recommandation 6: Gouvernance
    st.markdown("""
        <div class="recommendation-card">
            <div class="recommendation-title">🏛️ Renforcement de la Gouvernance</div>
            <div class="recommendation-content">
                <ul>
                    <li>Mettre en place des systèmes d'évaluation transparents</li>
                    <li>Renforcer l'autonomie des établissements</li>
                    <li>Impliquer les parties prenantes dans la prise de décision</li>
                    <li>Développer des indicateurs de performance pertinents</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section d'action
    st.markdown("""
        <div style='background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%); 
                    padding: 30px; 
                    border-radius: 15px; 
                    margin: 30px 0;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h2 style='color: #2c3e50; margin-bottom: 20px;'>🚀 Passons à l'Action</h2>
            <p style='color: #34495e; font-size: 1.2em; line-height: 1.6;'>
                Ces recommandations constituent une feuille de route pour transformer nos systèmes éducatifs. 
                Leur mise en œuvre nécessite un engagement collectif et une approche progressive.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")

