import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("D:/Document/Firman Hasibuan/Bangkit/Streamlit/PRSA_DATA_CLEAN.csv")

st.title('Air Quality Dashboard')
st.write("""
Dashboard ini menjelaskan kualitas udara di kota-kota China pada Tahun 2017.
""")

with st.sidebar:
    st.header('Dashboard Sidebar')
    option = st.sidebar.selectbox('Pilih Tampilan', 
                                  ('Descriptive Analysis', 'Exploratory Data Analysis (EDA)', 'Advanced Analysis'))

if option == 'Descriptive Analysis':
    st.subheader('Summary Dataset')

    stations = df['station'].unique()
    selected_station = st.selectbox('Pilih Station: ', stations)

    df_station = df[df['station'] == selected_station]

    st.write(f"### Data Teratas untuk Stasiun {selected_station}:")
    st.write(df_station.head())

    st.write(f"### Summary Statistics untuk Stasiun {selected_station}:")
    st.write(df_station.describe())

elif option == 'Exploratory Data Analysis (EDA)':
    st.subheader('Exploratory Data Analysis (EDA)')
    
    tab1, tab2, tab3, tab4 = st.tabs(["Boxplot", "Line Plot", "Scatter Plot", "Top Cities"])
    
    with tab1:
        stations = df['station'].unique()
        selected_station = st.selectbox('Pilih Station:', stations)

        df_station = df[df['station'] == selected_station]

        columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
        numeric_columns = df_station.select_dtypes(include=['float64', 'int64']).columns.tolist()
        columns = [col for col in columns if col in numeric_columns]

        st.write(f"### Boxplot Polutan di Stasiun {selected_station}")
        fig, axes = plt.subplots(4, 3, figsize=(15, 10))
        axes = axes.flatten()

        for i, col in enumerate(columns):
            ax = sns.boxplot(y=df_station[col], ax=axes[i])  
            ax.set_title(f'{col} Distribution')
            ax.set_xlabel(f'{col}')
            ax.set_ylabel('Concentration (ug/m3)')

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        st.pyplot(fig)

    with tab2:
        selected_station = st.selectbox('Pilih Station untuk Line Plot:', stations)

        df_station = df[df['station'] == selected_station]

        selected_polutant = st.selectbox('Pilih Polutan untuk Line Plot:', columns)
        option = st.selectbox('Pilih Tampilan Line Plot', ['Daily', 'Monthly', 'Hourly'])

        if option == 'Daily':
            daily_avg = df_station.groupby(['year', 'month', 'day'])[columns].mean().reset_index()

            st.write(f"### Daily Line Plot untuk Stasiun {selected_station}")
            fig, ax = plt.subplots(figsize=(15, 5))
            sns.lineplot(x='day', y=daily_avg[selected_polutant], data=daily_avg, ax=ax)
            ax.set_title(f'Rata-rata Harian {selected_polutant} di Stasiun {selected_station}')
            ax.set_xlabel('Hari')
            ax.set_ylabel('Konsentrasi (ug/m3)')
            plt.tight_layout()
            st.pyplot(fig)

        elif option == 'Monthly':
            monthly_avg = df_station.groupby(['year', 'month'])[columns].mean().reset_index()

            st.write(f"### Monthly Line Plot untuk Stasiun {selected_station}")
            fig, ax = plt.subplots(figsize=(15, 5))
            sns.lineplot(x='month', y=monthly_avg[selected_polutant], hue='year', data=monthly_avg, ax=ax)
            ax.set_title(f'Rata-rata Bulanan {selected_polutant} di Stasiun {selected_station}')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Konsentrasi (ug/m3)')
            plt.tight_layout()
            st.pyplot(fig)

        elif option == 'Hourly':
            hourly_avg = df_station.groupby('hour')[columns].mean().reset_index()

            st.write(f"### Hourly Line Plot untuk Stasiun {selected_station}")
            fig, ax = plt.subplots(figsize=(15, 5))
            sns.lineplot(x='hour', y=hourly_avg[selected_polutant], data=hourly_avg, ax=ax)
            ax.set_title(f'Rata-rata Per Jam {selected_polutant} di Stasiun {selected_station}')
            ax.set_xlabel('Jam')
            ax.set_ylabel('Konsentrasi (ug/m3)')
            plt.tight_layout()
            st.pyplot(fig)

    with tab3:
        st.subheader('Scatter Plot di Stasiun')

        selected_station = st.selectbox('Pilih Station untuk Scatter Plot:', stations)
        df_station = df[df['station'] == selected_station]

        x_axis = st.selectbox('Pilih variabel untuk sumbu X:', columns)
        y_axis = st.selectbox('Pilih variabel untuk sumbu Y:', columns)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=df_station[x_axis], y=df_station[y_axis], ax=ax)
        ax.set_title(f'Scatter Plot antara {x_axis} dan {y_axis} di Stasiun {selected_station}')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        plt.tight_layout()
        st.pyplot(fig)

    with tab4:
        st.subheader('Top 10 Kota dengan Polutan Tertinggi')

        selected_pollutant = st.selectbox('Pilih Polutan untuk Bar Plot:', columns)

        top_cities = df.groupby('station').agg({selected_pollutant: 'mean'}).reset_index()
        top_cities = top_cities.sort_values(by=selected_pollutant, ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='station', y=selected_pollutant, data=top_cities, ax=ax, palette='viridis')
        ax.set_title(f'Top 10 Kota dengan Rata-rata {selected_pollutant} Tertinggi')
        ax.set_ylabel('Kota')
        ax.set_xlabel(f'Rata-rata {selected_pollutant} (ug/m3)') 
        plt.tight_layout()
        st.pyplot(fig)

elif option == 'Advanced Analysis':
    st.subheader('Advanced Analysis')
    
    stations = df['station'].unique()
    selected_station = st.selectbox('Pilih Station:', stations)
    
    df_station = df[df['station'] == selected_station]
    
    tab1, tab2 = st.tabs(["RFM Analysis", "Correlation Heatmap"])
    
    with tab1:
        st.write("### RFM Analysis")
        
        rfm_data = df_station.groupby('station').agg({
            'PM2.5': 'mean',
            'PM10': 'mean',
            'SO2': 'mean',
            'NO2': 'mean',
            'CO': 'mean',
            'O3': 'mean',
        }).reset_index()

        rfm_data['R'] = rfm_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].rank(method='min', ascending=False).mean(axis=1)
        rfm_data['F'] = rfm_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].rank(method='min', ascending=True).mean(axis=1)
        rfm_data['M'] = rfm_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].rank(method='min', ascending=True).mean(axis=1)

        rfm_data['RFM Score'] = rfm_data[['R', 'F', 'M']].sum(axis=1)

        col1, col2, col3 = st.columns(3)

        with col1:
            avg_recency = round(rfm_data['R'].mean(), 1)
            st.metric("Average Recency", value=avg_recency)

        with col2:
            avg_frequency = round(rfm_data['F'].mean(), 2)
            st.metric("Average Frequency", value=avg_frequency)

        with col3:
            avg_monetary = round(rfm_data['M'].mean(), 2)
            st.metric("Average Monetary", value=avg_monetary)

    with tab2:
        st.write("### Correlation Heatmap")

        numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
        corr_matrix = df_station[numeric_columns].corr()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title(f'Correlation Heatmap of Pollutants and Weather Variables di Stasiun {selected_station}')
        plt.tight_layout()
        st.pyplot(fig)