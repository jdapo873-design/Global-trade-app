import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Global Trade", page_icon="🌎", layout="wide")

# ================= 1. 20+ 种全球语言界面 =================
UI_TRANSLATIONS = {
    "简体中文": {"title": "全球跨境贸易智能终端", "t1": "📦 实时利润", "t2": "📊 选品库", "t3": "💱 汇率换算", "t4": "💼 AI 贸易助手", "save": "💾 保存", "name": "商品名称", "cost": "进价", "sell": "售价", "ship": "运费 (RM)", "fee": "平台抽成 %", "calc": "实时利润：", "ai_prod": "输入商品，AI 自动生成文案：", "ai_lang": "🌐 选择生成语言"},
    "繁體中文": {"title": "全球跨境貿易智能終端", "t1": "📦 實時利潤", "t2": "📊 選品庫", "t3": "💱 匯率換算", "t4": "💼 AI 貿易助手", "save": "💾 保存", "name": "商品名稱", "cost": "進價", "sell": "售價", "ship": "運費 (RM)", "fee": "平台抽成 %", "calc": "實時利潤：", "ai_prod": "輸入商品，AI 自動生成文案：", "ai_lang": "🌐 選擇生成語言"},
    "English": {"title": "Global Trade Terminal", "t1": "📦 Live Profit", "t2": "📊 Vault", "t3": "💱 Exchange", "t4": "💼 AI Trade Expert", "save": "💾 Save", "name": "Product Name", "cost": "Cost", "sell": "Sell Price", "ship": "Shipping (RM)", "fee": "Platform Fee %", "calc": "Live Profit:", "ai_prod": "Enter product, AI generates copy:", "ai_lang": "🌐 Target Language"},
    "Bahasa Melayu": {"title": "Terminal Perdagangan Global", "t1": "📦 Untung Langsung", "t2": "📊 Inventori", "t3": "💱 Tukar Wang", "t4": "💼 Pakar AI", "save": "💾 Simpan", "name": "Nama Produk", "cost": "Kos", "sell": "Harga Jual", "ship": "Penghantaran (RM)", "fee": "Yuran Platform %", "calc": "Keuntungan Langsung:", "ai_prod": "Masukkan produk, AI jana teks:", "ai_lang": "🌐 Bahasa Sasaran"},
    "Español": {"title": "Terminal Comercial Global", "t1": "📦 Ganancia en Vivo", "t2": "📊 Bóveda", "t3": "💱 Cambio", "t4": "💼 Experto IA", "save": "💾 Guardar", "name": "Nombre del Producto", "cost": "Costo", "sell": "Precio de Venta", "ship": "Envío (RM)", "fee": "Comisión %", "calc": "Ganancia en Vivo:", "ai_prod": "Ingresa producto, IA genera texto:", "ai_lang": "🌐 Idioma Objetivo"},
    "Français": {"title": "Terminal Commercial Global", "t1": "📦 Profit en Direct", "t2": "📊 Coffre", "t3": "💱 Change", "t4": "💼 Expert IA", "save": "💾 Enregistrer", "name": "Nom du Produit", "cost": "Coût", "sell": "Prix de Vente", "ship": "Expédition (RM)", "fee": "Frais %", "calc": "Profit en Direct:", "ai_prod": "Entrez le produit, l'IA génère:", "ai_lang": "🌐 Langue Cible"},
    "Deutsch": {"title": "Globales Handels-Terminal", "t1": "📦 Live-Gewinn", "t2": "📊 Tresor", "t3": "💱 Wechsel", "t4": "💼 KI-Experte", "save": "💾 Speichern", "name": "Produktname", "cost": "Kosten", "sell": "Verkaufspreis", "ship": "Versand (RM)", "fee": "Plattformgebühr %", "calc": "Live-Gewinn:", "ai_prod": "Produkt eingeben, KI generiert:", "ai_lang": "🌐 Zielsprache"},
    "日本語": {"title": "グローバル貿易ターミナル", "t1": "📦 リアルタイム利益", "t2": "📊 選品庫", "t3": "💱 為替", "t4": "💼 AI専門家", "save": "💾 保存", "name": "商品名", "cost": "原価", "sell": "販売価格", "ship": "送料 (RM)", "fee": "手数料 %", "calc": "リアルタイム利益：", "ai_prod": "商品を入力、AIが生成:", "ai_lang": "🌐 ターゲット言語"},
    "한국어": {"title": "글로벌 무역 터미널", "t1": "📦 실시간 이익", "t2": "📊 보관함", "t3": "💱 환율", "t4": "💼 AI 전문가", "save": "💾 저장", "name": "상품명", "cost": "원가", "sell": "판매가", "ship": "배송비 (RM)", "fee": "수수료 %", "calc": "실시간 이익:", "ai_prod": "상품 입력, AI 생성:", "ai_lang": "🌐 대상 언어"},
    "العربية": {"title": "محطة التجارة العالمية", "t1": "📦 الربح المباشر", "t2": "📊 المخزن", "t3": "💱 صرف العملات", "t4": "💼 خبير الذكاء الاصطناعي", "save": "💾 حفظ", "name": "اسم المنتج", "cost": "التكلفة", "sell": "سعر البيع", "ship": "الشحن (RM)", "fee": "رسوم المنصة %", "calc": "الربح المباشر:", "ai_prod": "أدخل المنتج، الذكاء الاصطناعي ينشئ:", "ai_lang": "🌐 اللغة المستهدفة"},
    "हिन्दी": {"title": "वैश्विक व्यापार टर्मिनल", "t1": "📦 लाइव लाभ", "t2": "📊 तिजोरी", "t3": "💱 विनिमय", "t4": "💼 एआई विशेषज्ञ", "save": "💾 सहेजें", "name": "उत्पाद का नाम", "cost": "लागत", "sell": "बिक्री मूल्य", "ship": "शिपिंग (RM)", "fee": "प्लेटफ़ॉर्म शुल्क %", "calc": "लाइव लाभ:", "ai_prod": "उत्पाद दर्ज करें, एआई उत्पन्न करता है:", "ai_lang": "🌐 लक्ष्य भाषा"},
    "ภาษาไทย": {"title": "เทอร์มินัลการค้าโลก", "t1": "📦 กำไรสด", "t2": "📊 ห้องนิรภัย", "t3": "💱 แลกเปลี่ยน", "t4": "💼 ผู้เชี่ยวชาญ AI", "save": "💾 บันทึก", "name": "ชื่อสินค้า", "cost": "ต้นทุน", "sell": "ราคาขาย", "ship": "ค่าส่ง (RM)", "fee": "ค่าธรรมเนียม %", "calc": "กำไรสด:", "ai_prod": "ป้อนสินค้า, AI สร้าง:", "ai_lang": "🌐 ภาษเป้าหมาย"},
    "Tiếng Việt": {"title": "Thiết bị đầu cuối thương mại", "t1": "📦 Lợi nhuận trực tiếp", "t2": "📊 Kho", "t3": "💱 Tỷ giá", "t4": "💼 Chuyên gia AI", "save": "💾 Lưu", "name": "Tên sản phẩm", "cost": "Chi phí", "sell": "Giá bán", "ship": "Phí vận chuyển (RM)", "fee": "Phí nền tảng %", "calc": "Lợi nhuận trực tiếp:", "ai_prod": "Nhập sản phẩm, AI tạo:", "ai_lang": "🌐 Ngôn ngữ đích"}
}

st.markdown("### 🌐 界面语言 / UI Language")
ui_lang = st.selectbox("", list(UI_TRANSLATIONS.keys()), label_visibility="collapsed")
t = UI_TRANSLATIONS[ui_lang]

# ================= 2. 极简 UI =================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .title-text { font-size: 3em !important; font-weight: 800; background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; }
    .stButton>button { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)
st.markdown(f'<h1 class="title-text">{t["title"]}</h1>', unsafe_allow_html=True)

# ================= 3. 汇率 =================
@st.cache_data(ttl=3600)
def get_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
    except: return None
rates = get_rates()
currency_list = ["MYR", "CNY", "USD", "EUR", "GBP", "SGD"]

# ================= 4. 页面 =================
tab1, tab2, tab3, tab4 = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input(t["name"], "Muslim Clothes")
        c_cost = st.number_input(t["cost"], value=25.0, step=1.0)
        c_curr = st.selectbox("Cost Currency", currency_list, index=1)
    with col2:
        s_sell = st.number_input(t["sell"], value=72.0, step=1.0)
        s_curr = st.selectbox("Sell Currency", currency_list, index=0)
    ship = st.number_input(t["ship"], value=8.0, step=1.0)
    fee = st.number_input(t["fee"], value=10.0, step=1.0)
    
    if rates:
        cost_conv = (c_cost / rates[c_curr]) * rates[s_curr]
        real_profit = s_sell - cost_conv - ship - (s_sell * (fee/100))
        st.markdown(f"### {t['calc']}")
        if real_profit > 10:
            st.success(f"**{real_profit:.2f} {s_curr}**")
        else:
            st.error(f"**{real_profit:.2f} {s_curr}**")
        if st.button(t["save"]):
            df_new = pd.DataFrame([{"Product": p_name, "Cost": round(cost_conv,2), "Sell": s_sell, "Currency": s_curr, "Profit": round(real_profit,2)}])
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
        amt = st.number_input("Amount", value=100.0)
        f_curr = st.selectbox("From", currency_list, index=1)
        t_curr = st.selectbox("To", currency_list, index=0)
        st.info(f"{amt} {f_curr} = {(amt / rates[f_curr]) * rates[t_curr]:.2f} {t_curr}")

with tab4:
    st.write(f"### {t['t4']}")
    target_lang = st.selectbox(t["ai_lang"], list(UI_TRANSLATIONS.keys()))
    prod_desc = st.text_area(t["ai_prod"], "便携榨汁机，USB充电。")
    
    if st.button("🚀 呼叫 AI / Call AI"):
        with st.spinner("云端 AI 正在飞速生成..."):
            try:
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    st.error("API Key 未配置，请在终端运行: export GROQ_API_KEY='gsk_xxx'")
                    st.stop()

                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                prompt = f"你是顶级电商文案专家。请用【{target_lang}】为以下商品写3个吸引人的卖点，不要任何中文或英文解释，直接输出纯正的{target_lang}。商品：{prod_desc}"
                
                data = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
                res = requests.post(url, headers=headers, json=data)
                
                if res.status_code == 200:
                    st.info(res.json()["choices"][0]["message"]["content"])
                else:
                    st.error(f"Groq 接口报错: {res.json()}")
                    
            except Exception as e:
                st.error(f"AI 请求失败：{e}")
