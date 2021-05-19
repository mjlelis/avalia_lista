from sklearn.cluster import KMeans
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


st.title("Backoffice para segmentação em cluster")
st.write("Esta aplicação permite configurar parâmetros elementares para geração de novos resultados em segmentação.")
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor="none", **kwargs):
    if x.size != y.size:
        raise ValueError("X e Y precisam ter as mesmas dimensões")
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse(
        (0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs
    )
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    transf = (
        transforms.Affine2D()
            .rotate_deg(45)
            .scale(scale_x, scale_y)
            .translate(mean_x, mean_y)
    )
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


@st.cache
def data():
    X = np.random.normal(0, 1, 1000).reshape(-1, 2)
    return X

st.sidebar.header('Explorador de Clusterização')
st.sidebar.write("O explorador de clusterização permite reparametrizar e visualizar com mais clareza resultados de retreino em função de score atribuido. ")


X = data()
constrain_cluster = st.sidebar.slider(
    min_value=0, max_value=300, value=0, step=50, label="Constrain por Cluster: "
)
cluster_slider = st.sidebar.slider(
    min_value=3, max_value=5, value=2, label="Número de Clusters: "
)
kmeans = KMeans(n_clusters=cluster_slider, random_state=0).fit(X)
labels = kmeans.labels_

selectbox = st.sidebar.selectbox("Limites de Confiança", [False, True])
stdbox = st.sidebar.selectbox("Desvio padrão: ", [1, 2, 3])

clrs = ["red", "seagreen", "orange", "blue", "yellow", "purple"]

n_labels = len(set(labels))

individual = st.selectbox("Gráficos Independentes?", [False, True])

if individual:
    fig, ax = plt.subplots(ncols=n_labels)
else:
    fig, ax = plt.subplots()

for i, yi in enumerate(set(labels)):
    if not individual:
        a = ax
    else:
        a = ax[i]

    xi = X[labels == yi]
    x_pts = xi[:, 0]
    y_pts = xi[:, 1]
    a.scatter(x_pts, y_pts, c=clrs[yi])

    if selectbox:
        confidence_ellipse(
            x=x_pts,
            y=y_pts,
            ax=a,
            edgecolor="black",
            facecolor=clrs[yi],
            alpha=0.2,
            n_std=stdbox,
        )
plt.tight_layout()
st.write(fig)

st.sidebar.subheader("Considerar Média de Avaliadores")
st.sidebar.write("Ao considerar a média dos avaliadores, o modelo será retreinado e considerará uma penalidade para ocorrencias com scores abaixo 2.")

st.sidebar.subheader("Score médio atual = 3")
submeter = st.sidebar.button("Submeter a Retreino")