import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Global Trade", page_icon="🌎", layout="wide")

# ================= 全球多语言界面字典 =================
UI_TRANSLATIONS = {
    "简体中文": {"title": "全球跨境贸易智能终端", "t1": "📦 利润计算", "t2": "📊 选品库", "t3": "🌍 市场情报", "t4": "💼 AI 贸易助手", "calc": "计算真实利润", "save": "保存到选品库", "name": "商品名称", "cost": "进价", "sell": "售价", "ship": "运费 (RM)", "fee": "平台抽成 %", "amt": "金额", "from": "从", "to": "到", "ai_lang": "🌐 AI 生成的目标语言", "prod": "你的商品或问题", "call": "🚀 呼叫 AI 专家"},
    "繁體中文": {"title": "全球跨境貿易智能終端", "t1": "📦 利潤計算", "t2": "📊 選品庫", "t3": "🌍 市場情報", "t4": "💼 AI 貿易助手", "calc": "計算真實利潤", "save": "保存到選品庫", "name": "商品名稱", "cost": "進價", "sell": "售價", "ship": "運費 (RM)", "fee": "平台抽成 %", "amt": "金額", "from": "從", "to": "到", "ai_lang": "🌐 AI 生成的目標語言", "prod": "你的商品或問題", "call": "🚀 呼叫 AI 專家"},
    "English": {"title": "Global Trade Terminal", "t1": "📦 Profit Calculator", "t2": "📊 Vault", "t3": "🌍 Market Intel", "t4": "💼 AI Trade Expert", "calc": "Calculate Profit", "save": "Save to Vault", "name": "Product Name", "cost": "Cost", "sell": "Sell Price", "ship": "Shipping (RM)", "fee": "Platform Fee %", "amt": "Amount", "from": "From", "to": "To", "ai_lang": "🌐 AI Target Language", "prod": "Your Product or Question", "call": "🚀 Call AI Expert"},
    "Bahasa Melayu": {"title": "Terminal Perdagangan Global", "t1": "📦 Kira Untung", "t2": "📊 Inventori", "t3": "🌍 Pasaran", "t4": "💼 Pakar AI", "calc": "Kira Keuntungan", "save": "Simpan", "name": "Nama Produk", "cost": "Kos", "sell": "Harga Jual", "ship": "Penghantaran (RM)", "fee": "Yuran Platform %", "amt": "Jumlah", "from": "Dari", "to": "Ke", "ai_lang": "🌐 Bahasa Sasaran AI", "prod": "Produk atau Soalan Anda", "call": "🚀 Panggil Pakar AI"},
    "Español": {"title": "Terminal Comercial Global", "t1": "📦 Calculadora", "t2": "📊 Bóveda", "t3": "🌍 Mercado", "t4": "💼 Experto IA", "calc": "Calcular Ganancia", "save": "Guardar", "name": "Nombre del Producto", "cost": "Costo", "sell": "Precio de Venta", "ship": "Envío (RM)", "fee": "Comisión %", "amt": "Cantidad", "from": "De", "to": "A", "ai_lang": "🌐 Idioma objetivo de IA", "prod": "Tu Producto o Pregunta", "call": "🚀 Llamar a IA"},
    "Français": {"title": "Terminal Commercial Global", "t1": "📦 Calculatrice", "t2": "📊 Coffre", "t3": "🌍 Marché", "t4": "💼 Expert IA", "calc": "Calculer le Profit", "save": "Enregistrer", "name": "Nom du Produit", "cost": "Coût", "sell": "Prix de Vente", "ship": "Expédition (RM)", "fee": "Frais de Plateforme %", "amt": "Montant", "from": "De", "to": "À", "ai_lang": "🌐 Langue cible de l'IA", "prod": "Votre Produit ou Question", "call": "🚀 Appeler l'Expert IA"},
    "Deutsch": {"title": "Globales Handels-Terminal", "t1": "📦 Gewinnrechner", "t2": "📊 Tresor", "t3": "🌍 Marktinfo", "t4": "💼 KI-Experte", "calc": "Gewinn Berechnen", "save": "Speichern", "name": "Produktname", "cost": "Kosten", "sell": "Verkaufspreis", "ship": "Versand (RM)", "fee": "Plattformgebühr %", "amt": "Betrag", "from": "Von", "to": "Zu", "ai_lang": "🌐 KI-Zielsprache", "prod": "Ihr Produkt oder Ihre Frage", "call": "🚀 KI-Experten Rufen"},
    "日本語": {"title": "グローバル貿易ターミナル", "t1": "📦 利益計算", "t2": "📊 選品庫", "t3": "🌍 市場情報", "t4": "💼 AI専門家", "calc": "利益を計算する", "save": "保存する", "name": "商品名", "cost": "原価", "sell": "販売価格", "ship": "送料 (RM)", "fee": "プラットフォーム手数料 %", "amt": "金額", "from": "から", "to": "まで", "ai_lang": "🌐 AIのターゲット言語", "prod": "商品または質問", "call": "🚀 AI専門家を呼ぶ"},
    "한국어": {"title": "글로벌 무역 터미널", "t1": "📦 이익 계산", "t2": "📊 보관함", "t3": "🌍 시장 정보", "t4": "💼 AI 전문가", "calc": "이익 계산", "save": "저장", "name": "상품명", "cost": "원가", "sell": "판매가", "ship": "배송비 (RM)", "fee": "플랫폼 수수료 %", "amt": "금액", "from": "부터", "to": "까지", "ai_lang": "🌐 AI 대상 언어", "prod": "상품 또는 질문", "call": "🚀 AI 전문가 호출"},
    "العربية": {"title": "محطة التجارة العالمية", "t1": "📦 حاسبة الربح", "t2": "📊 المخزن", "t3": "🌍 معلومات السوق", "t4": "💼 خبير الذكاء الاصطناعي", "calc": "احسب الربح", "save": "حفظ", "name": "اسم المنتج", "cost": "التكلفة", "sell": "سعر البيع", "ship": "الشحن (RM)", "fee": "رسوم المنصة %", "amt": "المبلغ", "from": "من", "to": "إلى", "ai_lang": "🌐 اللغة المستهدفة للذكاء الاصطناعي", "prod": "المنتج أو السؤال", "call": "🚀 استدعاء خبير الذكاء الاصطناعي"}
}

# AI 生成内容支持的语言
AI_LANGS = ["简体中文", "繁體中文", "English", "Bahasa Melayu", "Español", "Français", "Deutsch", "Italiano", "Português", "Русский", "العربية", "हिन्दी", "日本語", "한국어", "ภาษาไทย", "Tiếng Việt"]

# ================= 顶部切换 =================
st.markdown("### 🌐 界面语言 / UI Language")
ui_lang = st.selectbox("", list(UI_TRANSLATIONS.keys()), label_visibility="collapsed")
t = UI_TRANSLATIONS[ui_lang]

# ================= UI 美化 =================
st.markdown("""
<style>
    .title-text { font-size: 3em !important; font-weight: 800; background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)
st.markdown(f'<h1 class="title-text">{t["title"]}</h1>', unsafe_allow_html=True)

# ================= 汇率 =================
@st.cache_data(ttl=3600)
def get_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
    except: return None
rates = get_rates()
currency_list = ["MYR", "CNY", "USD", "EUR", "GBP", "SGD", "JPY"]

# ================= 页面 =================
tab1, tab2, tab3, tab4 = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

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
    
    if st.button(t["calc"]):
        if rates:
            cost_conv = (c_cost / rates[c_curr]) * rates[s_curr]
            real_profit = s_sell - cost_conv - ship - (s_sell * (fee/100))
            st.success(f"Profit: {real_profit:.2f} {s_curr}")
            st.session_state['new_product'] = {"Product": p_name, "Cost": round(cost_conv,2), "Sell": s_sell, "Currency": s_curr, "Profit": round(real_profit,2)}
    
    if st.button(t["save"]):
        if 'new_product' in st.session_state:
            df_new = pd.DataFrame([st.session_state['new_product']])
            file = "my_selection.csv"
            df_new.to_csv(file, mode='a', header=not os.path.exists(file), index=False)
            st.balloons()
            st.success("Saved!")

with tab2:
    file = "my_selection.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        if not df.empty:
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
            st.dataframe(df.sort_values(by="Profit", ascending=False), use_container_width=True, height=400)

with tab3:
    if rates:
        amt = st.number_input(t["amt"], value=100.0)
        f_curr = st.selectbox(t["from"], currency_list, index=1)
        t_curr = st.selectbox(t["to"], currency_list, index=0)
        st.info(f"{amt} {f_curr} = {(amt / rates[f_curr]) * rates[t_curr]:.2f} {t_curr}")

with tab4:
    st.write(f"### {t['t4']}")
    target_lang = st.selectbox(t["ai_lang"], AI_LANGS)
    prod_desc = st.text_area(t["prod"], "便携榨汁机，USB充电。")
    
    if st.button(t["call"]):
        with st.spinner("AI Thinking..."):
            try:
                prompt = f"你是顶级电商文案专家。请用【{target_lang}】为以下商品写3个吸引人的卖点，不要任何中文或英文解释，直接输出纯正的{target_lang}。商品：{prod_desc}"
                res = requests.post("http://localhost:11434/api/generate", json={
                    "model": "qwen2.5:3b", "prompt": prompt, "stream": False
                })
                st.info(res.json()["response"])
            except:
                st.error("AI Offline. Ensure Ollama is running.")
