import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="全球跨境贸易智能终端", page_icon="🌎", layout="wide")

# ================= 1. 语言与配置 =================
st.markdown("### 🌐 选择界面语言 / Choose Language")
lang = st.selectbox("", ["中文", "English"], label_visibility="collapsed")

if lang == "中文":
    t = {"title": "全球跨境贸易智能终端", "cap": "探索全球市场，算清每一笔利润。", "tab1": "📦 利润计算", "tab2": "📊 选品库", "tab3": "🌍 汇率市场", "tab4": "💼 AI 贸易专家"}
else:
    t = {"title": "Global Trade Terminal", "cap": "Explore markets, calculate profits.", "tab1": "📦 Calculator", "tab2": "📊 Vault", "tab3": "🌍 Market", "tab4": "💼 AI Expert"}

# 高级 UI
st.markdown("""
<style>
    .title-text { font-size: 3em !important; font-weight: 800; background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)
st.markdown(f'<h1 class="title-text">{t["title"]}</h1>', unsafe_allow_html=True)

# ================= 2. 汇率获取 =================
@st.cache_data(ttl=3600)
def get_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
    except: return None
rates = get_rates()
currency_list = ["MYR", "CNY", "USD", "EUR", "GBP", "SGD", "THB"]

# ================= 3. 页面标签 =================
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# ===== 标签 1：利润计算 =====
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("商品名称 / Product Name", "穆斯林衣服")
        c_cost = st.number_input("进价 / Cost", value=25.0)
        c_curr = st.selectbox("进货货币 / Cost Currency", currency_list, index=1)
    with col2:
        s_sell = st.number_input("售价 / Sell Price", value=72.0)
        s_curr = st.selectbox("售卖货币 / Sell Currency", currency_list, index=0)
    ship = st.number_input("运费 (RM) / Shipping", value=8.0)
    fee = st.number_input("平台抽成 % / Fee", value=10.0)
    
    if st.button("计算真实利润 / Calculate Profit"):
        if rates:
            cost_conv = (c_cost / rates[c_curr]) * rates[s_curr]
            real_profit = s_sell - cost_conv - ship - (s_sell * (fee/100))
            st.success(f"真实利润 / Real Profit: {real_profit:.2f} {s_curr}")
            
            # 存到 session_state，准备保存
            st.session_state['new_product'] = {
                "Product": p_name, "Cost": round(cost_conv,2), 
                "Sell": s_sell, "Currency": s_curr, "Profit": round(real_profit,2)
            }
    
    # 保存按钮（必须放在计算之后）
    if st.button("💾 保存到选品库 / Save to Vault"):
        if 'new_product' in st.session_state:
            df_new = pd.DataFrame([st.session_state['new_product']])
            file = "my_selection.csv"
            df_new.to_csv(file, mode='a', header=not os.path.exists(file), index=False)
            st.balloons()
            st.success("已保存！去第二页查看。")
        else:
            st.warning("请先计算利润，再保存。")

# ===== 标签 2：选品库 =====
with tab2:
    file = "my_selection.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        if not df.empty:
            # 数据清洗，确保能排序
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
            df_sorted = df.sort_values(by="Profit", ascending=False)
            st.dataframe(df_sorted, use_container_width=True, height=500)
        else:
            st.info("选品库是空的。")
    else:
        st.info("暂无记录。")

# ===== 标签 3：汇率市场 =====
with tab3:
    if rates:
        amt = st.number_input("金额 / Amount", value=100.0)
        f_curr = st.selectbox("从 / From", currency_list, index=1)
        t_curr = st.selectbox("到 / To", currency_list, index=0)
        st.info(f"{amt} {f_curr} = {(amt / rates[f_curr]) * rates[t_curr]:.2f} {t_curr}")

# ===== 标签 4：AI 贸易专家 =====
with tab4:
    st.write("### 💼 全球选品与文案专家")
    
    # 国家/地区列表
    countries = ["马来西亚 (Malaysia)", "中国 (China)", "美国 (USA)", "新加坡 (Singapore)", "泰国 (Thailand)", "印尼 (Indonesia)", "英国 (UK)", "沙特阿拉伯 (Saudi Arabia)"]
    
    col_a, col_b = st.columns(2)
    with col_a:
        target_country = st.selectbox("目标国家 / Target Country", countries)
    with col_b:
        task_type = st.selectbox("任务类型 / Task", ["分析该国热销趋势", "写当地语言的商品文案", "解答当地贸易政策"])
        
    prod_desc = st.text_area("你的商品或问题 / Your Product or Question:", "便携榨汁机，USB充电，价格便宜。")
    
    if st.button("🚀 呼叫 AI 专家 / Call AI"):
        with st.spinner("AI 正在深度思考..."):
            try:
                if task_type == "分析该国热销趋势":
                    prompt = f"你是跨境电商专家。请分析【{target_country}】目前最适合卖什么？请给出3个具体的选品建议，并说明理由。"
                elif task_type == "写当地语言的商品文案":
                    prompt = f"你是电商文案专家。请为【{target_country}】的消费者，用当地常用语言，为这个商品写一个吸引人的标题和3个卖点：{prod_desc}。"
                else:
                    prompt = f"你是贸易政策专家。请解答卖家关于【{target_country}】的以下问题：{prod_desc}。"
                
                res = requests.post("http://localhost:11434/api/generate", json={
                    "model": "qwen2.5:3b", "prompt": prompt, "stream": False
                })
                st.info(res.json()["response"])
            except Exception as e:
                st.error(f"连接本地 AI 失败，请确保 Ollama 已打开。错误信息：{e}")
