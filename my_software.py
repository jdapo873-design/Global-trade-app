import streamlit as st
import pandas as pd
import requests
import os
import pydeck as pdk

# ================= 1. 页面与 20 国语言 =================
st.set_page_config(page_title="Global Trade Hub", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

UI_TRANSLATIONS = {
    "简体中文": {"title": "全球跨境贸易中控台", "t1": "📦 利润与预测", "t2": "📊 选品库", "t3": "🌍 全球战情室", "t4": "💼 多国文案", "name": "商品名称", "cost": "进价", "sell": "售价", "ship": "运费", "fee": "抽成 %", "calc": "实时利润率", "save": "💾 保存", "news": "📰 财经新闻", "conv": "💱 汇率换算", "map_t": "🌍 全球电商交易热度实时雷达", "ai_lang_select": "选择要生成的语言（可多选）："},
    "繁體中文": {"title": "全球跨境貿易中控台", "t1": "📦 利潤與預測", "t2": "📊 選品庫", "t3": "🌍 全球戰情室", "t4": "💼 多國文案", "name": "商品名稱", "cost": "進價", "sell": "售價", "ship": "運費", "fee": "抽成 %", "calc": "實時利潤率", "save": "💾 保存", "news": "📰 財經新聞", "conv": "💱 匯率換算", "map_t": "🌍 全球電商交易熱度實時雷達", "ai_lang_select": "選擇要生成的語言（可多選）："},
    "English": {"title": "Global Trade Hub", "t1": "📦 Profit & Predict", "t2": "📊 Vault", "t3": "🌍 War Room", "t4": "💼 Bulk Listings", "name": "Product Name", "cost": "Cost", "sell": "Sell Price", "ship": "Shipping", "fee": "Fee %", "calc": "Live Margin", "save": "💾 Save", "news": "📰 Financial News", "conv": "💱 FX Converter", "map_t": "🌍 Global E-commerce Heat Radar", "ai_lang_select": "Select languages to generate:"},
    "Bahasa Melayu": {"title": "Hab Perdagangan Global", "t1": "📦 Untung & Ramalan", "t2": "📊 Inventori", "t3": "🌍 Bilik Perang", "t4": "💼 Eksport Teks", "name": "Nama Produk", "cost": "Kos", "sell": "Harga Jual", "ship": "Penghantaran", "fee": "Yuran %", "calc": "Margin Langsung", "save": "💾 Simpan", "news": "📰 Berita Kewangan", "conv": "💱 Penukar FX", "map_t": "🌍 Radar Haba E-dagang Global", "ai_lang_select": "Pilih bahasa untuk dijana:"},
    "Español": {"title": "Centro de Comercio Global", "t1": "📦 Ganancia y Predicción", "t2": "📊 Bóveda", "t3": "🌍 Sala de Guerra", "t4": "💼 Listados Masivos", "name": "Nombre del Producto", "cost": "Costo", "sell": "Precio", "ship": "Envío", "fee": "Comisión %", "calc": "Margen en Vivo", "save": "💾 Guardar", "news": "📰 Noticias Financieras", "conv": "💱 Convertidor FX", "map_t": "🌍 Radar de Calor Global", "ai_lang_select": "Seleccionar idiomas:"},
    "Français": {"title": "Centre de Commerce Global", "t1": "📦 Profit et Prédiction", "t2": "📊 Coffre", "t3": "🌍 Salle de Guerre", "t4": "💼 Listes en Vrac", "name": "Nom du Produit", "cost": "Coût", "sell": "Prix", "ship": "Expédition", "fee": "Frais %", "calc": "Marge en Direct", "save": "💾 Enregistrer", "news": "📰 Actualités Financières", "conv": "💱 Convertisseur FX", "map_t": "🌍 Radar de Chaleur Global", "ai_lang_select": "Sélectionner les langues:"},
    "Deutsch": {"title": "Globales Handelszentrum", "t1": "📦 Gewinn", "t2": "📊 Tresor", "t3": "🌍 War Room", "t4": "💼 Massen-Listings", "name": "Produktname", "cost": "Kosten", "sell": "Verkaufspreis", "ship": "Versand", "fee": "Gebühr %", "calc": "Live-Marge", "save": "💾 Speichern", "news": "📰 Finanznachrichten", "conv": "💱 FX-Konverter", "map_t": "🌍 Globaler E-Commerce-Radar", "ai_lang_select": "Sprachen auswählen:"},
    "Italiano": {"title": "Hub del Commercio", "t1": "📦 Profitto", "t2": "📊 Cassaforte", "t3": "🌍 Sala Operativa", "t4": "💼 Annunci", "name": "Nome Prodotto", "cost": "Costo", "sell": "Prezzo", "ship": "Spedizione", "fee": "Commissione %", "calc": "Margine", "save": "💾 Salva", "news": "📰 Notizie", "conv": "💱 Convertitore", "map_t": "🌍 Radar Calore Globale", "ai_lang_select": "Seleziona lingue:"},
    "Português": {"title": "Hub de Comércio", "t1": "📦 Lucro", "t2": "📊 Cofre", "t3": "🌍 Sala de Guerra", "t4": "💼 Listagens", "name": "Nome", "cost": "Custo", "sell": "Preço", "ship": "Envio", "fee": "Taxa %", "calc": "Margem", "save": "💾 Salvar", "news": "📰 Notícias", "conv": "💱 Conversor", "map_t": "🌍 Radar de Calor Global", "ai_lang_select": "Selecione idiomas:"},
    "Русский": {"title": "Глобальный Хаб", "t1": "📦 Прибыль", "t2": "📊 Хранилище", "t3": "🌍 Ситуационный центр", "t4": "💼 Листинги", "name": "Название", "cost": "Себестоимость", "sell": "Цена", "ship": "Доставка", "fee": "Комиссия %", "calc": "Маржа", "save": "💾 Сохранить", "news": "📰 Новости", "conv": "💱 Конвертер", "map_t": "🌍 Глобальный Радар", "ai_lang_select": "Выберите языки:"},
    "العربية": {"title": "مركز التجارة", "t1": "📦 الربح", "t2": "📊 المخزن", "t3": "🌍 غرفة الحرب", "t4": "💼 قوائم", "name": "الاسم", "cost": "التكلفة", "sell": "السعر", "ship": "الشحن", "fee": "رسوم %", "calc": "الهامش", "save": "💾 حفظ", "news": "📰 الأخبار", "conv": "💱 محول", "map_t": "🌍 رادار التجارة العالمي", "ai_lang_select": "اختر اللغات:"},
    "हिन्दी": {"title": "वैश्विक व्यापार", "t1": "📦 लाभ", "t2": "📊 तिजोरी", "t3": "🌍 युद्ध कक्ष", "t4": "💼 थोक", "name": "नाम", "cost": "लागत", "sell": "मूल्य", "ship": "शिपिंग", "fee": "शुल्क %", "calc": "मार्जिन", "save": "💾 सहेजें", "news": "📰 समाचार", "conv": "💱 परिवर्तक", "map_t": "🌍 ग्लोबल ई-कॉमर्स रडार", "ai_lang_select": "भाषाएं चुनें:"},
    "日本語": {"title": "グローバル貿易ハブ", "t1": "📦 利益", "t2": "📊 選品庫", "t3": "🌍 ウォールーム", "t4": "💼 一括出品", "name": "商品名", "cost": "原価", "sell": "販売価格", "ship": "送料", "fee": "手数料 %", "calc": "利益率", "save": "💾 保存", "news": "📰 金融ニュース", "conv": "💱 為替", "map_t": "🌍 グローバルEコマースレーダー", "ai_lang_select": "言語を選択:"},
    "한국어": {"title": "글로벌 무역 허브", "t1": "📦 이익", "t2": "📊 보관함", "t3": "🌍 상황실", "t4": "💼 대량 등록", "name": "상품명", "cost": "원가", "sell": "판매가", "ship": "배송비", "fee": "수수료 %", "calc": "마진", "save": "💾 저장", "news": "📰 금융 뉴스", "conv": "💱 환율", "map_t": "🌍 글로벌 이커머스 레이더", "ai_lang_select": "언어 선택:"},
    "ภาษาไทย": {"title": "ศูนย์กลางการค้า", "t1": "📦 กำไร", "t2": "📊 ห้องนิรภัย", "t3": "🌍 ห้องสงคราม", "t4": "💼 รายการ", "name": "ชื่อสินค้า", "cost": "ต้นทุน", "sell": "ราคา", "ship": "ค่าส่ง", "fee": "ค่าธรรมเนียม %", "calc": "มาร์จิน", "save": "💾 บันทึก", "news": "📰 ข่าว", "conv": "💱 แปลงสกุลเงิน", "map_t": "🌍 เรดาร์อีคอมเมิร์ซ", "ai_lang_select": "เลือกภาษา:"},
    "Tiếng Việt": {"title": "Trung Tâm Thương Mại", "t1": "📦 Lợi nhuận", "t2": "📊 Kho", "t3": "🌍 Phòng Chiến Tranh", "t4": "💼 Niêm yết", "name": "Tên", "cost": "Chi phí", "sell": "Giá", "ship": "Phí", "fee": "Thuế %", "calc": "Biên LN", "save": "💾 Lưu", "news": "📰 Tin tức", "conv": "💱 Chuyển đổi", "map_t": "🌍 Radar Thương mại", "ai_lang_select": "Chọn ngôn ngữ:"},
    "Türkçe": {"title": "Küresel Ticaret", "t1": "📦 Kâr", "t2": "📊 Kasa", "t3": "🌍 Savaş Odası", "t4": "💼 Listeler", "name": "Ad", "cost": "Maliyet", "sell": "Fiyat", "ship": "Kargo", "fee": "Ücret %", "calc": "Marj", "save": "💾 Kaydet", "news": "📰 Haberler", "conv": "💱 Çevirici", "map_t": "🌍 Küresel E-Ticaret Radarı", "ai_lang_select": "Dil seçin:"},
    "Nederlands": {"title": "Globaal Handelscentrum", "t1": "📦 Winst", "t2": "📊 Kluis", "t3": "🌍 Oorlogskamer", "t4": "💼 Advertenties", "name": "Naam", "cost": "Kosten", "sell": "Prijs", "ship": "Verzending", "fee": "Kosten %", "calc": "Marge", "save": "💾 Opslaan", "news": "📰 Nieuws", "conv": "💱 Converter", "map_t": "🌍 Wereldwijde E-commerce Radar", "ai_lang_select": "Selecteer talen:"},
    "Polski": {"title": "Centrum Handlowe", "t1": "📦 Zysk", "t2": "📊 Sejf", "t3": "🌍 Sztab", "t4": "💼 Listy", "name": "Nazwa", "cost": "Koszt", "sell": "Cena", "ship": "Wysyłka", "fee": "Opłata %", "calc": "Marża", "save": "💾 Zapisz", "news": "📰 Wiadomości", "conv": "💱 Konwerter", "map_t": "🌍 Globalny Radar E-commerce", "ai_lang_select": "Wybierz języki:"}
}

col_lang, col_theme = st.columns([4, 1])
with col_lang:
    ui_lang = st.selectbox("🌐 界面语言 / Language", list(UI_TRANSLATIONS.keys()), label_visibility="collapsed")
with col_theme:
    is_dark = st.toggle("🌙 Dark Mode", value=True)
t = UI_TRANSLATIONS[ui_lang]

# ================= 2. 顶级 UI =================
if is_dark:
    bg_color, text_color = "#0B0F19", "#E2E8F0"
    card_bg, border_color = "rgba(30, 41, 59, 0.5)", "rgba(255, 255, 255, 0.1)"
    accent_glow = "rgba(56, 189, 248, 0.4)"
else:
    bg_color, text_color = "#F8FAFC", "#0F172A"
    card_bg, border_color = "rgba(255, 255, 255, 0.9)", "rgba(0, 0, 0, 0.05)"
    accent_glow = "rgba(56, 189, 248, 0.2)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif !important; }}
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    header {{visibility: hidden;}} footer {{visibility: hidden;}}
    .title-text {{
        font-size: 3.5em !important; font-weight: 800; letter-spacing: -1.5px;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; padding-bottom: 10px;
    }}
    div[data-testid="stVerticalBlock"] > div {{
        background: {card_bg}; backdrop-filter: blur(12px);
        border-radius: 16px; border: 1px solid {border_color}; padding: 15px;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        color: #FFFFFF; border-radius: 12px; border: none; padding: 12px 28px;
        font-weight: 600; font-size: 16px;
    }}
    .stTabs [data-baseweb="tab"] {{ font-size: 18px; font-weight: 600; padding: 10px 0; border-bottom: 3px solid transparent; }}
    .stTabs [aria-selected="true"] {{ border-bottom: 3px solid #38BDF8 !important; color: #38BDF8 !important; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<h1 class="title-text">{t["title"]}</h1>', unsafe_allow_html=True)

# ================= 3. 数据工具 =================
@st.cache_data(ttl=3600)
def get_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
    except: return None
rates = get_rates()
currency_list = ["MYR", "CNY", "USD", "EUR", "GBP", "SGD", "JPY", "THB"]

def call_groq(prompt, temp=0.5):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: return "❌ 未配置 Key。请在终端执行: export GROQ_API_KEY='gsk_xxx'"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "temperature": temp}
    try:
        res = requests.post(url, headers=headers, json=data)
        return res.json()["choices"][0]["message"]["content"] if res.status_code == 200 else "❌ 接口报错"
    except: return "❌ 请求失败"

# ================= 4. 核心模块 =================
tab1, tab2, tab3, tab4 = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

# 页面 1：利润与预测
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input(t["name"], "Muslim Clothes")
        c_cost = st.number_input(t["cost"], value=25.0)
        c_curr = st.selectbox("Cost Currency", currency_list, index=1) 
    with col2:
        s_sell = st.number_input(t["sell"], value=72.0)
        s_curr = st.selectbox("Sell Currency", currency_list, index=0) 
    ship = st.number_input(t["ship"], value=8.0)
    fee = st.number_input(t["fee"], value=10.0)
    
    if rates:
        cost_conv = (c_cost / rates[c_curr]) * rates[s_curr]
        real_profit = s_sell - cost_conv - ship - (s_sell * (fee/100))
        margin = (real_profit / s_sell) * 100 if s_sell > 0 else 0
        st.markdown(f"#### {t['calc']}")
        st.success(f"🟢 **{real_profit:.2f} {s_curr}** (Margin: {margin:.1f}%)")
        if st.button(t["save"]):
            df_new = pd.DataFrame([{"Product": p_name, "Cost": round(cost_conv,2), "Sell": s_sell, "Currency": s_curr, "Profit": round(real_profit,2), "Margin": round(margin,1)}])
            file = "my_selection.csv"
            df_new.to_csv(file, mode='a', header=not os.path.exists(file), index=False)
            st.balloons(); st.success("Saved!")

# 页面 2：选品库
with tab2:
    file = "my_selection.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        if not df.empty:
            st.dataframe(df.sort_values(by="Profit", ascending=False), use_container_width=True, height=400)
        else: st.info("库为空。")
    else: st.info("暂无记录。")

# 页面 3：国际大厂级 3D 飞线物流地图
with tab3:
    st.markdown(f"### {t['map_t']} (Global Logistics Arc Radar)")
    
    origin = {"lat": 22.5431, "lon": 114.0579, "name": "China (Origin)"}
    destinations = [
        {"lat": 4.2105, "lon": 101.9758, "name": "Malaysia", "volume": 8500},
        {"lat": -0.7893, "lon": 113.9213, "name": "Indonesia", "volume": 9500},
        {"lat": 15.8700, "lon": 100.9925, "name": "Thailand", "volume": 7000},
        {"lat": 14.0583, "lon": 108.2772, "name": "Vietnam", "volume": 8000},
        {"lat": 37.0902, "lon": -95.7129, "name": "USA", "volume": 10000},
        {"lat": 23.8859, "lon": 45.0792, "name": "Saudi Arabia", "volume": 6000},
        {"lat": -14.2350, "lon": -51.9253, "name": "Brazil", "volume": 5500},
        {"lat": 55.3781, "lon": -3.4360, "name": "UK", "volume": 7500},
        {"lat": -25.2744, "lon": 133.7751, "name": "Australia", "volume": 6500}
    ]
    
    arc_data = []
    for dest in destinations:
        arc_data.append({
            "from_lat": origin["lat"], "from_lon": origin["lon"],
            "to_lat": dest["lat"], "to_lon": dest["lon"],
            "dest_name": dest["name"], "volume": dest["volume"]
        })
    df_arcs = pd.DataFrame(arc_data)

    arc_layer = pdk.Layer(
        "ArcLayer", data=df_arcs,
        get_source_position=["from_lon", "from_lat"],
        get_target_position=["to_lon", "to_lat"],
        get_source_color=[56, 189, 248, 200],
        get_target_color=[192, 132, 252, 255],
        get_width=3, pickable=True,
    )

    target_layer_glow = pdk.Layer(
        "ScatterplotLayer", data=df_arcs,
        get_position=["to_lon", "to_lat"],
        get_radius="volume * 30",
        get_fill_color=[192, 132, 252, 60],
        pickable=False,
    )

    target_layer_core = pdk.Layer(
        "ScatterplotLayer", data=df_arcs,
        get_position=["to_lon", "to_lat"],
        get_radius="volume * 8", 
        get_fill_color=[255, 255, 255, 200],
        pickable=True,
    )

    origin_layer = pdk.Layer(
        "ScatterplotLayer", data=[origin],
        get_position=["lon", "lat"],
        get_radius=50000,
        get_fill_color=[56, 189, 248, 255],
    )

    view_state = pdk.ViewState(
        longitude=80.0, latitude=20.0, zoom=1.2, pitch=45, bearing=0,
    )

    st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json",
        initial_view_state=view_state,
        layers=[arc_layer, target_layer_glow, target_layer_core, origin_layer],
        tooltip={"text": "Destination: {dest_name}\nVolume: {volume}"}
    ))

    st.markdown("---")
    col_news, col_fx = st.columns([1, 1])
    with col_news:
        st.markdown(f"### {t['news']}")
        if st.button("生成今日简报"):
            with st.spinner("AI 正在汇总..."):
                st.info(call_groq("请用中文总结今天全球最主要的3条宏观经济或跨境电商新闻，并简短分析影响。", 0.6))
    with col_fx:
        st.markdown(f"### {t['conv']}")
        if rates:
            amt = st.number_input("Amount", value=1000.0)
            f_curr = st.selectbox("From", currency_list, index=1)
            t_curr = st.selectbox("To", currency_list, index=0)
            st.metric(label="Result", value=f"{(amt / rates[f_curr]) * rates[t_curr]:.2f} {t_curr}")

# 页面 4：多国文案（支持自定义多选！）
with tab4:
    bulk_prod = st.text_area("输入商品信息:", "便携榨汁机，USB充电。")
    
    available_langs = ["English", "Bahasa Melayu", "中文 (Chinese)", "ไทย (Thai)", "Tiếng Việt", "Español", "日本語", "한국어", "العربية"]
    selected_langs = st.multiselect(t["ai_lang_select"], available_langs, default=["English", "Bahasa Melayu"])
    
    if st.button("生成多国文案"):
        if not selected_langs:
            st.warning("请至少选择一种语言！")
        else:
            with st.spinner("AI 正在生成多国语言文案..."):
                lang_str = ", ".join(selected_langs)
                prompt = f"商品：{bulk_prod}。请输出一个 Markdown 表格：| 语言 | 标题 | 3个卖点 |。请严格按照以下语言生成：{lang_str}。"
                st.markdown(call_groq(prompt, 0.4))
