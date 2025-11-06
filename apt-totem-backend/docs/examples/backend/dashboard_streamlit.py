import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Configuración de la página
st.set_page_config(
    page_title="NeoTotem AI - Analytics Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Función para obtener datos de la API
@st.cache_data(ttl=60)
def get_analytics_data(days=7):
    """Obtener datos de analytics desde la API"""
    try:
        response = requests.get(f"http://localhost:8001/analytics/dashboard?dias={days}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

@st.cache_data(ttl=30)
def get_real_time_data():
    """Obtener datos en tiempo real"""
    try:
        response = requests.get("http://localhost:8001/dashboard/real-time")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Header principal
st.markdown('<h1 class="main-header">🤖 NeoTotem AI - Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar para controles
st.sidebar.title("🎛️ Controles")
days_filter = st.sidebar.selectbox(
    "Período de análisis",
    [1, 7, 14, 30],
    index=1,
    format_func=lambda x: f"{x} días"
)

auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=True)

# Obtener datos
analytics_data = get_analytics_data(days_filter)
real_time_data = get_real_time_data()

if analytics_data is None:
    st.error("❌ No se pudo conectar con la API. Asegúrate de que el backend esté ejecutándose.")
    st.stop()

# Métricas principales
st.subheader("📊 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Conversiones Hoy",
        real_time_data.get("conversions_today", 0) if real_time_data else 0,
        delta="12%"
    )

with col2:
    st.metric(
        "Sesiones Activas",
        real_time_data.get("active_sessions", 0) if real_time_data else 0,
        delta="8%"
    )

with col3:
    ctr = real_time_data.get("ctr_average", 0) if real_time_data else 0
    st.metric(
        "CTR Promedio",
        f"{ctr:.1%}",
        delta="5%"
    )

with col4:
    st.metric(
        "Productos Vistos",
        real_time_data.get("products_viewed", 0) if real_time_data else 0,
        delta="23%"
    )

# Gráficos principales
st.subheader("📈 Análisis de Tendencias")

# Gráfico de conversiones por hora
if real_time_data and "hourly_conversions" in real_time_data:
    fig_hourly = px.line(
        x=list(range(24)),
        y=real_time_data["hourly_conversions"],
        title="Conversiones por Hora",
        labels={"x": "Hora", "y": "Conversiones"}
    )
    fig_hourly.update_layout(
        xaxis_title="Hora del día",
        yaxis_title="Número de conversiones",
        showlegend=False
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

# Productos más populares
st.subheader("🏆 Productos Más Populares")

if analytics_data and "productos_top" in analytics_data:
    productos_df = pd.DataFrame(analytics_data["productos_top"])
    
    if not productos_df.empty:
        # Gráfico de barras
        fig_products = px.bar(
            productos_df.head(10),
            x="clics",
            y="producto",
            orientation="h",
            title="Top 10 Productos por Clics",
            labels={"clics": "Número de clics", "producto": "Producto"}
        )
        fig_products.update_layout(
            yaxis_title="Producto",
            xaxis_title="Clics"
        )
        st.plotly_chart(fig_products, use_container_width=True)
        
        # Tabla de productos
        st.subheader("📋 Detalles de Productos")
        st.dataframe(
            productos_df[["producto", "marca", "clics", "ctr"]].head(10),
            use_container_width=True
        )

# Análisis de rendimiento
st.subheader("⚡ Análisis de Rendimiento")

if analytics_data and "rendimiento" in analytics_data:
    rendimiento = analytics_data["rendimiento"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Total Recomendaciones",
            rendimiento.get("total_recomendaciones", 0)
        )
    
    with col2:
        st.metric(
            "CTR Promedio",
            f"{rendimiento.get('ctr_promedio', 0):.1%}"
        )

# Estado del sistema
st.subheader("🔧 Estado del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    status = "🟢 Online" if real_time_data else "🔴 Offline"
    st.markdown(f"**Estado:** {status}")

with col2:
    if real_time_data:
        st.markdown(f"**Última actualización:** {real_time_data.get('timestamp', 'N/A')}")

with col3:
    if real_time_data:
        accuracy = real_time_data.get("detection_accuracy", 0)
        st.metric("Precisión IA", f"{accuracy:.1%}")

# Auto-refresh
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🤖 NeoTotem AI Dashboard | Actualizado: {timestamp}
    </div>
    """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)

