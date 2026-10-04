import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sayfa Ayarları ve Başlık
st.set_page_config(page_title="Dijital Pazarlama Analitiği", layout="wide")
st.title("🚀 Dijital Pazarlama ve Bütçe Optimizasyonu Panosu")
st.markdown("Bu interaktif panel, markaların dijital reklam kampanyalarını analiz ederek bütçe optimizasyonu sağlamak için veri bilimi ile hazırlanmıştır.")

# 2. Veriyi Yükleme (Sunucuyu yormamak için cache kullanıyoruz)
@st.cache_data
def load_data():
    df = pd.read_csv('global_ads_performance_dataset.csv')
    df['Conversion_Rate'] = (df['conversions'] / df['clicks']) * 100
    df['ROI'] = ((df['revenue'] - df['ad_spend']) / df['ad_spend']) * 100
    df['CPA_Maliyet'] = df['ad_spend'] / df['conversions']
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# 3. Web Sitesi İçin Sekmeler (Tabs) Oluşturma
tab1, tab2, tab3 = st.tabs(["📊 Genel Bakış", "🌍 Zaman ve Coğrafya", "🤖 Gelecek Tahmini"])

with tab1:
    st.header("Reklam Kanallarına Göre Ortalama Yatırım Getirisi (ROI)")
    platform_roi = df.groupby('platform')['ROI'].mean().reset_index()
    fig1 = px.bar(platform_roi, x='platform', y='ROI', color='platform', text_auto='.2f')
    st.plotly_chart(fig1, use_container_width=True)

    st.header("Reklam Harcaması ve Gelir İlişkisi")
    fig2 = px.scatter(df, x='ad_spend', y='revenue', color='campaign_type', size='conversions', hover_data=['platform'])
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Günlük Trafik Trendi")
    trend_data = df.groupby(['date', 'platform'])['clicks'].sum().reset_index()
    fig3 = px.line(trend_data, x='date', y='clicks', color='platform', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.header("Ülkelere Göre Müşteri Edinme Maliyeti (CPA)")
    ulke_analizi = df.groupby('country')['CPA_Maliyet'].mean().reset_index().sort_values(by='CPA_Maliyet')
    fig6 = px.bar(ulke_analizi, x='country', y='CPA_Maliyet', color='CPA_Maliyet', text_auto='.2f', color_continuous_scale='Reds')
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.header("Bütçe ve Gelir Tahmini (Makine Öğrenmesi ile)")
    fig4 = px.scatter(df, x='ad_spend', y='revenue', color='platform', trendline='ols', opacity=0.6)
    st.plotly_chart(fig4, use_container_width=True)

    st.header("Sektör ve Platform Uyumu (Isı Haritası)")
    pivot_tablo = df.pivot_table(values='Conversion_Rate', index='industry', columns='platform', aggfunc='mean')
    fig5 = px.imshow(pivot_tablo, text_auto=".2f", aspect="auto", color_continuous_scale='Blues')
    st.plotly_chart(fig5, use_container_width=True)