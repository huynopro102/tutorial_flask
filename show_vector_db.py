import faiss
import numpy as np
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Load FAISS index
index = faiss.read_index("vector_db/index.faiss")
vectors = index.reconstruct_n(0, index.ntotal)

# Giảm chiều xuống còn 3D
pca = PCA(n_components=3)
vectors_3d = pca.fit_transform(vectors)

# Phân cụm các vectors
kmeans = KMeans(n_clusters=5)
labels = kmeans.fit_predict(vectors_3d)

# Tạo chú thích chi tiết
hover_text = []
for i, (vec, vec_3d) in enumerate(zip(vectors, vectors_3d)):
    text = f"Vector ID: {i}<br>"
    text += f"Original Vector: {vec[:5]}...<br>"  # Hiển thị 5 phần tử đầu tiên
    text += f"3D Coordinates: ({vec_3d[0]:.2f}, {vec_3d[1]:.2f}, {vec_3d[2]:.2f})<br>"
    text += f"Cluster: {labels[i]}"
    hover_text.append(text)

# Hiển thị mô hình 3D với Plotly
trace = go.Scatter3d(
    x=vectors_3d[:, 0],
    y=vectors_3d[:, 1],
    z=vectors_3d[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=labels,  # Màu sắc theo cụm
        colorscale='Viridis',
        opacity=0.8
    ),
    text=hover_text,
    hoverinfo='text'
)

layout = go.Layout(
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    ),
    title="3D Visualization of FAISS Vectors",
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Rockwell"
    )
)

fig = go.Figure(data=[trace], layout=layout)

# Thêm thông tin thống kê
stats_text = f"Total Vectors: {len(vectors)}<br>"
stats_text += f"Number of Clusters: {kmeans.n_clusters}<br>"
stats_text += f"PCA Explained Variance Ratio: {pca.explained_variance_ratio_}"

fig.add_annotation(
    xref="paper", yref="paper",
    x=0.02, y=1,
    text=stats_text,
    showarrow=False,
    font=dict(size=12),
    align="left",
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="black",
    borderwidth=1
)

fig.show()

# số lượng vector tượng chưng cho 7 chunks