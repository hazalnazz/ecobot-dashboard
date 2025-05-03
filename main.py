import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# Import configurations and calculations
from config import (
    SISTEM_GUC, MODEL_PATHS, CO2_CARPAN, VERIMLILIK_CARPAN,
    SURDURULEBILIRLIK_ESIK, STATIC_SERVER_URL
)
from calculations import (
    hesapla_karbon_ayakizi, surdurulebilirlik_puani, hesapla_zaman_bazli_etki
)
# Import our custom model viewer module
from model_viewer import display_3d_model

# --- Helper Functions ---

def get_license_info(sistem_tipi):
    """Retrieves license information for the selected system's model."""
    if sistem_tipi in MODEL_PATHS:
        model_rel_path = Path(MODEL_PATHS[sistem_tipi])
        # Assume license.txt is in the same directory as the model file
        license_path = model_rel_path.parent / "license.txt"
        # Construct absolute path relative to this script's location
        abs_license_path = Path(__file__).parent / license_path
        if abs_license_path.exists():
            try:
                with open(abs_license_path, 'r', encoding='utf-8') as f:
                    return license_path.as_posix(), f.read() # Return relative path and content
            except Exception as e:
                return license_path.as_posix(), f"Error reading license file: {e}"
        else:
            return license_path.as_posix(), "License file not found."
    return "N/A", "Model path not defined."

# --- UI Rendering Functions ---

def display_sidebar(sistem_listesi):
    """Renders the sidebar controls."""
    with st.sidebar:
        st.header("⚙️ Sistem Konfigürasyonu")

        sistem_tipi = st.selectbox(
            "Otonom Sistem Türü",
            options=sistem_listesi
        )

        st.subheader("⚡ Parametreler")
        sure_dk = st.number_input(
            "Günlük Kullanım Süresi (dakika)",
            min_value=1,
            max_value=1440, # 24 * 60
            value=60,
            step=10,
            help="Sistemin bir günde ortalama aktif olduğu süre."
        )

        enerji_kaynagi = st.selectbox(
            "Enerji Kaynağı",
            options=list(CO2_CARPAN.keys()),
            help="Sistemin kullandığı birincil enerji kaynağı."
        )

        verimlilik = st.selectbox(
            "Verimlilik Modu",
            options=list(VERIMLILIK_CARPAN.keys()),
            help="Sistemin operasyonel verimlilik ayarı."
        )

        st.info("💡 Güneş ve rüzgar gibi yenilenebilir enerji kaynakları ve verimli modlar sürdürülebilirlik puanınızı iyileştirir.")

        st.subheader("🧊 3D Model (Küçük Önizleme)")
        if sistem_tipi in MODEL_PATHS:
            with st.spinner("Önizleme yükleniyor..."):
                 display_3d_model(MODEL_PATHS[sistem_tipi], height=200)
        else:
            st.warning("Bu sistem için 3D model tanımlanmamış.")

    return sistem_tipi, sure_dk, enerji_kaynagi, verimlilik

def display_model_tab(sistem_tipi):
    """Renders the 3D Model tab."""
    with st.container(): # Use container for better layout control
        st.header(f"🧊 {sistem_tipi} - 3D Model Görselleştirme")
        st.markdown("Modeli incelemek için fareyle sürükleyin, yakınlaştırmak/uzaklaştırmak için tekerleği kullanın.")

        if sistem_tipi in MODEL_PATHS:
            # Display the main, larger 3D model
            with st.spinner("3D model yükleniyor... Lütfen bekleyin."):
                display_3d_model(MODEL_PATHS[sistem_tipi], height=500)

            # Display License Info
            st.subheader("📜 Model Lisans Bilgileri")
            rel_license_path, license_content = get_license_info(sistem_tipi)
            st.caption(f"Lisans Dosyası: `{rel_license_path}`")
            st.text_area("Lisans Detayları:", license_content, height=150, disabled=True)
        else:
            st.error(f"'{sistem_tipi}' için 3D model yolu tanımlanmamış.")
            st.info("Lütfen `config.py` dosyasını kontrol edin.")


def display_analysis_tab(enerji_kwh, co2_salimi, surdurulebilirlik_skoru, sistem_tipi, sure_dk, enerji_kaynagi, verimlilik):
    """Renders the Sustainability Analysis tab."""
    st.header("📊 Sürdürülebilirlik Analizi")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Günlük Enerji Tüketimi", f"{enerji_kwh:.3f} kWh")
    with col2:
        st.metric("💨 Günlük CO₂ Salımı", f"{co2_salimi:.2f} g")
    with col3:
        # Display Sustainability Score with color
        skor_renk = {
            "A+": "#1e8449", "A": "#27ae60", "B": "#2ecc71",
            "C": "#f1c40f", "D": "#e67e22", "E": "#d35400", "F": "#c0392b"
        }
        st.markdown(f"""
            <div style="background-color: {skor_renk.get(surdurulebilirlik_skoru, '#7f8c8d')}; padding: 10px; border-radius: 10px; text-align: center; height: 100%;">
                <p style="color: white; font-size: 1.1em; margin-bottom: 5px; font-weight: bold;">Sürdürülebilirlik Skoru</p>
                <h1 style="color: white; margin: 0; line-height: 1;">{surdurulebilirlik_skoru}</h1>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🌡️ CO₂ Salım Göstergesi")
    # Gauge Chart for CO2
    max_gauge = max(1000, co2_salimi * 1.2) # Adjust gauge max based on value
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = co2_salimi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Günlük CO₂ Salımı (gram)", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, max_gauge], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [ # Use score thresholds for steps
                {'range': [0, SURDURULEBILIRLIK_ESIK["A+"]], 'color': skor_renk["A+"]},
                {'range': [SURDURULEBILIRLIK_ESIK["A+"], SURDURULEBILIRLIK_ESIK["A"]], 'color': skor_renk["A"]},
                {'range': [SURDURULEBILIRLIK_ESIK["A"], SURDURULEBILIRLIK_ESIK["B"]], 'color': skor_renk["B"]},
                {'range': [SURDURULEBILIRLIK_ESIK["B"], SURDURULEBILIRLIK_ESIK["C"]], 'color': skor_renk["C"]},
                {'range': [SURDURULEBILIRLIK_ESIK["C"], SURDURULEBILIRLIK_ESIK["D"]], 'color': skor_renk["D"]},
                {'range': [SURDURULEBILIRLIK_ESIK["D"], SURDURULEBILIRLIK_ESIK["E"]], 'color': skor_renk["E"]},
                {'range': [SURDURULEBILIRLIK_ESIK["E"], max_gauge], 'color': skor_renk["F"]} # Last step to max
            ],
            'threshold': { # Example threshold at 'C' level
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': SURDURULEBILIRLIK_ESIK["C"]
            }
        }
    ))
    fig_gauge.update_layout(height=250, margin={'t':50, 'b':50})
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Optimizasyon Önerileri")
    # Optimization suggestions
    en_iyi_kaynak = min(CO2_CARPAN, key=CO2_CARPAN.get)
    en_iyi_verimlilik = min(VERIMLILIK_CARPAN, key=VERIMLILIK_CARPAN.get)

    _, mevcut_co2 = hesapla_karbon_ayakizi(sistem_tipi, sure_dk, enerji_kaynagi, verimlilik)
    _, en_iyi_co2 = hesapla_karbon_ayakizi(sistem_tipi, sure_dk, en_iyi_kaynak, en_iyi_verimlilik)
    _, sadece_kaynak_co2 = hesapla_karbon_ayakizi(sistem_tipi, sure_dk, en_iyi_kaynak, verimlilik)
    _, sadece_verim_co2 = hesapla_karbon_ayakizi(sistem_tipi, sure_dk, enerji_kaynagi, en_iyi_verimlilik)

    col1, col2 = st.columns(2)
    with col1:
        if enerji_kaynagi != en_iyi_kaynak:
            kaynak_tasarruf = mevcut_co2 - sadece_kaynak_co2
            if kaynak_tasarruf > 0:
                 st.success(f"✅ **Enerji Kaynağı:** '{en_iyi_kaynak}' kullanarak **{kaynak_tasarruf:.2f} g CO₂** tasarruf edebilirsiniz.")
            else:
                 st.info(f"ℹ️ **Enerji Kaynağı:** Zaten en verimli kaynaklardan birini ({enerji_kaynagi}) kullanıyorsunuz.")
        else:
            st.info(f"ℹ️ **Enerji Kaynağı:** En verimli kaynak olan '{en_iyi_kaynak}' seçili.")

    with col2:
        if verimlilik != en_iyi_verimlilik:
            verim_tasarruf = mevcut_co2 - sadece_verim_co2
            if verim_tasarruf > 0:
                st.success(f"✅ **Verimlilik Modu:** '{en_iyi_verimlilik}' moduna geçerek **{verim_tasarruf:.2f} g CO₂** tasarruf edebilirsiniz.")
            else:
                 st.info(f"ℹ️ **Verimlilik Modu:** Zaten en verimli modlardan birini ({verimlilik}) kullanıyorsunuz.")
        else:
            st.info(f"ℹ️ **Verimlilik Modu:** En verimli mod olan '{en_iyi_verimlilik}' seçili.")

    optimum_tasarruf = mevcut_co2 - en_iyi_co2
    if optimum_tasarruf > 0.1: # Show only if there's meaningful saving
        st.warning(f"⚠️ **Optimum:** Hem '{en_iyi_kaynak}' hem de '{en_iyi_verimlilik}' kullanarak toplam **{optimum_tasarruf:.2f} g CO₂** tasarrufu mümkündür (Günlük salım: {en_iyi_co2:.2f} g).")


def display_comparison_tab(sistem_tipi, sure_dk, verimlilik):
    """Renders the Comparative Analysis tab."""
    st.header("⚖️ Karşılaştırmalı Analiz")

    st.subheader("Enerji Kaynağına Göre CO₂ Salımı Karşılaştırması")
    karsilastirma_data = []
    for kaynak, co2_carpan in CO2_CARPAN.items():
        _, co2 = hesapla_karbon_ayakizi(sistem_tipi, sure_dk, kaynak, verimlilik)
        skor = surdurulebilirlik_puani(co2)
        karsilastirma_data.append({
            'Kaynak': kaynak,
            'CO₂ Salımı (gram)': co2,
            'Sürdürülebilirlik Skoru': skor
        })

    df_kaynaklar = pd.DataFrame(karsilastirma_data).sort_values('CO₂ Salımı (gram)')

    # Bar chart for comparison
    fig_bar = px.bar(
        df_kaynaklar,
        x='Kaynak',
        y='CO₂ Salımı (gram)',
        title=f'{sistem_tipi} için Enerji Kaynaklarının CO₂ Etkisi ({sure_dk} dk/gün, {verimlilik} Modu)',
        color='Sürdürülebilirlik Skoru',
        color_discrete_map={ # Use consistent colors
            "A+": "#1e8449", "A": "#27ae60", "B": "#2ecc71",
            "C": "#f1c40f", "D": "#e67e22", "E": "#d35400", "F": "#c0392b"
        },
        labels={'CO₂ Salımı (gram)': 'Günlük CO₂ Salımı (g)'}
    )
    fig_bar.update_layout(xaxis_title="Enerji Kaynağı", yaxis_title="Günlük CO₂ Salımı (gram)")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.dataframe(df_kaynaklar.style.format({'CO₂ Salımı (gram)': "{:.2f}"}), use_container_width=True)


def display_projection_tab(zaman_birimleri, enerji_verileri, co2_verileri):
    """Renders the Time-Based Projection tab."""
    st.header("⏱️ Zaman Bazlı Projeksiyon")

    proj_df = pd.DataFrame({
        'Zaman Dilimi': zaman_birimleri,
        'Enerji Tüketimi (kWh)': enerji_verileri,
        'CO₂ Salımı (gram)': co2_verileri
    })

    # Line chart for projections
    fig_line = px.line(
        proj_df,
        x='Zaman Dilimi',
        y=['Enerji Tüketimi (kWh)', 'CO₂ Salımı (gram)'],
        title='Kümülatif Enerji Tüketimi ve CO₂ Salımı Projeksiyonu',
        markers=True,
        labels={'value': 'Toplam Değer', 'variable': 'Metrik'}
    )
    fig_line.update_layout(xaxis_title="Zaman Dilimi", yaxis_title="Kümülatif Değer")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.subheader("🌳 Yıllık Çevresel Etki Özeti")
    yillik_enerji = enerji_verileri[3]
    yillik_co2_gram = co2_verileri[3]
    yillik_co2_kg = yillik_co2_gram / 1000
    # Average tree absorbs ~22 kg CO2 per year
    agac_denkligi = yillik_co2_kg / 22

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Yıllık Enerji", f"{yillik_enerji:.1f} kWh")
    with col2:
        st.metric("💨 Yıllık CO₂", f"{yillik_co2_kg:.2f} kg")
    with col3:
        st.metric("🌳 Ağaç Denkliği", f"{agac_denkligi:.2f} ağaç/yıl",
                  help="Yıllık CO₂ salımını dengelemek için gereken ortalama ağaç sayısı (yaklaşık).")

    # Display tree icons visually
    num_trees = int(agac_denkligi) + 1
    max_trees_display = 50 # Limit displayed icons
    tree_icons = "🌳" * min(num_trees, max_trees_display)
    if num_trees > max_trees_display:
        tree_icons += f" ... (+{num_trees - max_trees_display})"
    st.markdown(f"**Yıllık CO₂ Dengelemesi:** {tree_icons}")

    st.markdown("---")
    st.subheader("🔮 5 Yıllık Kümülatif Projeksiyon")
    yillar = list(range(1, 6))
    proj_5yil_df = pd.DataFrame({
        'Yıl': [f"{y}. Yıl" for y in yillar],
        'Toplam Enerji (kWh)': [yillik_enerji * y for y in yillar],
        'Toplam CO₂ (kg)': [yillik_co2_kg * y for y in yillar]
    })

    fig_area = px.area(
        proj_5yil_df,
        x='Yıl',
        y=['Toplam Enerji (kWh)', 'Toplam CO₂ (kg)'],
        title='5 Yıllık Kümülatif Enerji ve CO₂ Etkisi',
        labels={'value': 'Toplam Kümülatif Değer', 'variable': 'Metrik'},
         color_discrete_sequence=px.colors.qualitative.Safe # Use a colorblind-safe sequence
    )
    st.plotly_chart(fig_area, use_container_width=True)
    st.dataframe(proj_5yil_df.style.format({
        'Toplam Enerji (kWh)': "{:.1f}",
        'Toplam CO₂ (kg)': "{:.2f}"
        }), use_container_width=True)

# --- Main Application Logic ---

def main():
    st.set_page_config(
        page_title="EcoBot Dashboard",
        page_icon="🌱",
        layout="wide"
    )

    st.title("🌱 EcoBot Sürdürülebilirlik Dashboard")
    st.markdown("Otonom sistemlerinizin çevresel etkisini analiz edin, karşılaştırın ve optimize edin.")

    sistem_listesi = list(SISTEM_GUC.keys())
    sistem_tipi, sure_dk, enerji_kaynagi, verimlilik = display_sidebar(sistem_listesi)

    # Perform calculations
    enerji_kwh, co2_salimi = hesapla_karbon_ayakizi(
        sistem_tipi, sure_dk, enerji_kaynagi, verimlilik
    )
    surdurulebilirlik_skoru = surdurulebilirlik_puani(co2_salimi)
    zaman_birimleri, enerji_verileri, co2_verileri = hesapla_zaman_bazli_etki(
        enerji_kwh, co2_salimi
    )

    # Define tabs
    tab_titles = ["🧊 3D Model", "📊 Analiz", "⚖️ Karşılaştırma", "⏱️ Projeksiyon"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_titles)

    with tab1:
        display_model_tab(sistem_tipi)

    with tab2:
        display_analysis_tab(enerji_kwh, co2_salimi, surdurulebilirlik_skoru, sistem_tipi, sure_dk, enerji_kaynagi, verimlilik)

    with tab3:
        display_comparison_tab(sistem_tipi, sure_dk, verimlilik)

    with tab4:
        display_projection_tab(zaman_birimleri, enerji_verileri, co2_verileri)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.9em; color: #555;">
        <span>🌿 EcoBot v2.2</span>
        <span>Son Hesaplama: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        <span><a href="https://github.com/your-repo/ecobot" target="_blank">GitHub</a></span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()