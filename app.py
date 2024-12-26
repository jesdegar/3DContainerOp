import streamlit as st
import plotly.graph_objects as go

# Fungsi untuk menempatkan barang dalam kontainer
def place_items(container_dim, items):
    container_x, container_y, container_z = container_dim
    placements = []
    current_x = 0
    current_y = 0
    current_z = 0

    for item in items:
        item_x, item_y, item_z = item
        if current_x + item_x <= container_x:
            placements.append((current_x, current_y, current_z, item_x, item_y, item_z))
            current_x += item_x
        else:
            current_x = 0
            current_y += item_y
            if current_y + item_y > container_y:
                current_y = 0
                current_z += item_z
                if current_z + item_z > container_z:
                    st.warning("Tidak cukup ruang untuk semua barang!")
                    break
    return placements

# Visualisasi 3D susunan barang dalam kontainer
def visualize_container(container_dim, placements):
    fig = go.Figure()
    container_x, container_y, container_z = container_dim

    # Gambar kontainer
    fig.add_trace(go.Mesh3d(
        x=[0, container_x, container_x, 0, 0, container_x, container_x, 0],
        y=[0, 0, container_y, container_y, 0, 0, container_y, container_y],
        z=[0, 0, 0, 0, container_z, container_z, container_z, container_z],
        color='lightblue', opacity=0.50
    ))

    # Tambahkan barang
    for i, (x, y, z, dx, dy, dz) in enumerate(placements):
        fig.add_trace(go.Mesh3d(
            x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x],
            y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy],
            z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz],
            color='orange', opacity=0.80
        ))

    fig.update_layout(scene=dict(
        xaxis_title='Length',
        yaxis_title='Width',
        zaxis_title='Height'
    ))
    st.plotly_chart(fig)

# Antarmuka Streamlit
st.title('Cargo Container Optimizer')

# Input dimensi kontainer
st.header('Dimensi Kontainer')
container_x = st.number_input('Panjang (x)', min_value=1, value=10)
container_y = st.number_input('Lebar (y)', min_value=1, value=10)
container_z = st.number_input('Tinggi (z)', min_value=1, value=10)

# Input barang
st.header('Barang')
num_items = st.number_input('Jumlah Barang', min_value=1, value=5)
items = []
for i in range(num_items):
    st.subheader(f'Barang {i+1}')
    item_x = st.number_input(f'Panjang Barang {i+1}', min_value=1, value=2)
    item_y = st.number_input(f'Lebar Barang {i+1}', min_value=1, value=2)
    item_z = st.number_input(f'Tinggi Barang {i+1}', min_value=1, value=2)
    items.append((item_x, item_y, item_z))

# Tombol Optimasi
if st.button('Optimalkan dan Visualisasikan'):
    placements = place_items((container_x, container_y, container_z), items)
    visualize_container((container_x, container_y, container_z), placements)
