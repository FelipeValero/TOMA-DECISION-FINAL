import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análisis Interactivo de Datos")
st.sidebar.header("Filtros")

uploaded_file = st.sidebar.file_uploader("Carga tu archivo CSV", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Vista previa de los datos:")
    st.dataframe(data.head())

    columns = data.columns.tolist()
    selected_column = st.sidebar.selectbox("Selecciona una columna para explorar", columns)

    st.subheader(f"Estadísticas de {selected_column}")
    st.write(data[selected_column].describe())

    if pd.api.types.is_numeric_dtype(data[selected_column]):
        min_val, max_val = st.sidebar.slider(
            f"Rango para {selected_column}",
            min_value=float(data[selected_column].min()),
            max_value=float(data[selected_column].max()),
            value=(float(data[selected_column].min()), float(data[selected_column].max()))
        )
        filtered_data = data[data[selected_column].between(min_val, max_val)]
    else:
        unique_values = data[selected_column].unique()
        selected_values = st.sidebar.multiselect(f"Valores para {selected_column}", unique_values, unique_values)
        filtered_data = data[data[selected_column].isin(selected_values)]

    st.write(f"Datos filtrados por {selected_column}:")
    st.dataframe(filtered_data)

    st.subheader("Gráficos")
    if pd.api.types.is_numeric_dtype(data[selected_column]):
        fig, ax = plt.subplots()
        filtered_data[selected_column].hist(ax=ax, bins=20)
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        filtered_data[selected_column].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)
else:
    st.write("Carga un archivo para empezar.")
