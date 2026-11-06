import streamlit as st
import pandas as pd
import requests
import os
import pydeck as pdk

# ================= 1. 页面与 20 国语言 =================
st.set_page_config(page_title="Global Trade Hub", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

UI_TRANSLATIONS = {
    "简体中文": {"title": "全球跨境贸易中控台", "t1": "📦 利润与预测", "t2": "📊 选品库", "t3": "🌍 全球战情室", "t4": "💼 多国文案", "name": "商品名称", "cost": "进价", "sell": "售价", "ship": "运费", "fee": "抽成 %", "calc": "实时利润率", "save": "💾 保存", "news": "📰 财经新闻", "conv": "💱 汇率换算", "map_t": "🌍 全球电商交易热度实时雷达", "ai_lang_select": "选择要生成的语言（可多选）：", "t5": "📄 PDF 提取", "pdf_title": "PDF 关键信息提取", "pdf_caption": "上传供应商报价 PDF，AI 自动提取：产品名称、单价、起订量、总价。", "pdf_upload": "上传报价 PDF", "pdf_no_file": "请先上传一个 PDF 文件（.pdf）。", "pdf_preview": "已解析文本预览", "pdf_pages": "页", "pdf_chars": "字符", "pdf_btn": "🤖 AI 提取关键信息", "pdf_spinner": "AI 正在分析报价单...", "pdf_result": "提取结果", "pdf_prev_result": "上次提取结果"},
    "English": {"title": "Global Trade Hub", "t1": "📦 Profit & Predict", "t2": "📊 Vault", "t3": "🌍 War Room", "t4": "💼 Bulk Listings", "name": "Product Name", "cost": "Cost", "sell": "Sell Price", "ship": "Shipping", "fee": "Fee %", "calc": "Live Margin", "save": "💾 Save", "news": "📰 Financial News", "conv": "💱 FX Converter", "map_t": "🌍 Global E-commerce Heat Radar", "ai_lang_select": "Select languages to generate:", "t5": "📄 PDF Extract", "pdf_title": "PDF Key Info Extractor", "pdf_caption": "Upload a supplier quote PDF; AI extracts product name, unit price, MOQ and total price.", "pdf_upload": "Upload quote PDF", "pdf_no_file": "Please upload a PDF file (.pdf) first.", "pdf_preview": "Parsed text preview", "pdf_pages": "pages", "pdf_chars": "chars", "pdf_btn": "🤖 AI Extract Key Info", "pdf_spinner": "AI is analyzing the quotation...", "pdf_result": "Extraction Result", "pdf_prev_result": "Last Extraction Result"},
    "Bahasa Melayu": {"title": "Hab Perdagangan Global", "t1": "📦 Untung & Ramalan", "t2": "📊 Inventori", "t3": "🌍 Bilik Perang", "t4": "💼 Eksport Teks", "name": "Nama Produk", "cost": "Kos", "sell": "Harga Jual", "ship": "Penghantaran", "fee": "Yuran %", "calc": "Margin Langsung", "save": "💾 Simpan", "news": "📰 Berita Kewangan", "conv": "💱 Penukar FX", "map_t": "🌍 Radar Haba E-dagang Global", "ai_lang_select": "Pilih bahasa untuk dijana:", "t5": "📄 Ekstrak PDF", "pdf_title": "Ekstrak Maklumat Utama PDF", "pdf_caption": "Muat naik PDF sebut harga pembekal; AI mengekstrak nama produk, harga seunit, MOQ dan jumlah harga.", "pdf_upload": "Muat naik PDF sebut harga", "pdf_no_file": "Sila muat naik fail PDF (.pdf) dahulu.", "pdf_preview": "Pratonton teks yang dianalisis", "pdf_pages": "muka surat", "pdf_chars": "aksara", "pdf_btn": "🤖 AI Ekstrak Maklumat", "pdf_spinner": "AI sedang menganalisis sebut harga...", "pdf_result": "Hasil Ekstrak", "pdf_prev_result": "Hasil Ekstrak Terakhir"},
    "Español": {"title": "Centro de Comercio Global", "t1": "📦 Ganancia y Predicción", "t2": "📊 Bóveda", "t3": "🌍 Sala de Guerra", "t4": "💼 Listados Masivos", "name": "Nombre del Producto", "cost": "Costo", "sell": "Precio", "ship": "Envío", "fee": "Comisión %", "calc": "Margen en Vivo", "save": "💾 Guardar", "news": "📰 Noticias Financieras", "conv": "💱 Convertidor FX", "map_t": "🌍 Radar de Calor Global", "ai_lang_select": "Seleccionar idiomas:", "t5": "📄 Extraer PDF", "pdf_title": "Extractor de Información de PDF", "pdf_caption": "Sube un PDF de cotización; la IA extrae nombre del producto, precio unitario, MOQ y precio total.", "pdf_upload": "Subir PDF de cotización", "pdf_no_file": "Primero sube un archivo PDF (.pdf).", "pdf_preview": "Vista previa del texto analizado", "pdf_pages": "páginas", "pdf_chars": "caracteres", "pdf_btn": "🤖 Extraer información", "pdf_spinner": "La IA analiza la cotización...", "pdf_result": "Resultado de extracción", "pdf_prev_result": "Último resultado"},
    "繁體中文": {"title": "全球跨境貿易中控台", "t1": "📦 利潤與預測", "t2": "📊 選品庫", "t3": "🌍 全球戰情室", "t4": "💼 多國文案", "name": "商品名稱", "cost": "進價", "sell": "售價", "ship": "運費", "fee": "抽成 %", "calc": "實時利潤率", "save": "💾 保存", "news": "📰 財經新聞", "conv": "💱 匯率換算", "map_t": "🌍 全球電商交易熱度即時雷達", "ai_lang_select": "選擇要生成的語言（可多選）：", "t5": "📄 PDF 提取", "pdf_title": "PDF 關鍵資訊提取", "pdf_caption": "上傳供應商報價 PDF，AI 自動提取：產品名稱、單價、起訂量、總價。", "pdf_upload": "上傳報價 PDF", "pdf_no_file": "請先上傳一個 PDF 檔案（.pdf）。", "pdf_preview": "已解析文字預覽", "pdf_pages": "頁", "pdf_chars": "字元", "pdf_btn": "🤖 AI 提取關鍵資訊", "pdf_spinner": "AI 正在分析報價單...", "pdf_result": "提取結果", "pdf_prev_result": "上次提取結果"},
    "Bahasa Indonesia": {"title": "Pusat Perdagangan Global", "t1": "📦 Untung & Prediksi", "t2": "📊 Inventaris", "t3": "🌍 Ruang Perang", "t4": "💼 Teks Multi Bahasa", "name": "Nama Produk", "cost": "Harga Beli", "sell": "Harga Jual", "ship": "Ongkir", "fee": "Komisi %", "calc": "Margin Langsung", "save": "💾 Simpan", "news": "📰 Berita Keuangan", "conv": "💱 Konverter FX", "map_t": "🌍 Radar Panas E-dagang Global", "ai_lang_select": "Pilih bahasa yang akan dibuat:", "t5": "📄 Ekstrak PDF", "pdf_title": "Ekstrak Info Utama PDF", "pdf_caption": "Unggah PDF penawaran pemasok; AI mengekstrak nama produk, harga satuan, MOQ, dan harga total.", "pdf_upload": "Unggah PDF penawaran", "pdf_no_file": "Silakan unggah file PDF (.pdf) dulu.", "pdf_preview": "Pratinjau teks terurai", "pdf_pages": "halaman", "pdf_chars": "karakter", "pdf_btn": "🤖 AI Ekstrak Info", "pdf_spinner": "AI sedang menganalisis penawaran...", "pdf_result": "Hasil Ekstraksi", "pdf_prev_result": "Hasil Terakhir"},
    "Français": {"title": "Centre de Commerce Global", "t1": "📦 Profit & Prédiction", "t2": "📊 Coffre", "t3": "🌍 Salle de Guerre", "t4": "💼 Annonces Multi", "name": "Nom du Produit", "cost": "Prix d'Achat", "sell": "Prix de Vente", "ship": "Livraison", "fee": "Commission %", "calc": "Marge en Direct", "save": "💾 Enregistrer", "news": "📰 Actus Financières", "conv": "💱 Convertisseur FX", "map_t": "🌍 Radar de Chaleur E-commerce", "ai_lang_select": "Choisir les langues à générer :", "t5": "📄 Extraire PDF", "pdf_title": "Extracteur d'Infos PDF", "pdf_caption": "Téléversez un devis PDF ; l'IA extrait le nom du produit, le prix unitaire, le MOQ et le prix total.", "pdf_upload": "Téléverser le devis PDF", "pdf_no_file": "Téléversez d'abord un fichier PDF (.pdf).", "pdf_preview": "Aperçu du texte analysé", "pdf_pages": "pages", "pdf_chars": "caractères", "pdf_btn": "🤖 Extraire les infos", "pdf_spinner": "L'IA analyse le devis...", "pdf_result": "Résultat de l'extraction", "pdf_prev_result": "Dernier résultat"},
    "Deutsch": {"title": "Globales Handelszentrum", "t1": "📦 Gewinn & Prognose", "t2": "📊 Tresor", "t3": "🌍 Lagezentrum", "t4": "💼 Mehrsprachige Texte", "name": "Produktname", "cost": "Einkaufspreis", "sell": "Verkaufspreis", "ship": "Versand", "fee": "Gebühr %", "calc": "Live-Marge", "save": "💾 Speichern", "news": "📰 Finanznachrichten", "conv": "💱 FX-Umrechner", "map_t": "🌍 Globales E-Commerce-Hitze-Radar", "ai_lang_select": "Zu erstellende Sprachen wählen:", "t5": "📄 PDF extrahieren", "pdf_title": "PDF-Info-Extraktor", "pdf_caption": "Laden Sie ein Angebots-PDF hoch; die KI extrahiert Produktname, Stückpreis, MOQ und Gesamtpreis.", "pdf_upload": "Angebots-PDF hochladen", "pdf_no_file": "Bitte zuerst eine PDF-Datei (.pdf) hochladen.", "pdf_preview": "Vorschau des extrahierten Texts", "pdf_pages": "Seiten", "pdf_chars": "Zeichen", "pdf_btn": "🤖 Infos extrahieren", "pdf_spinner": "KI analysiert das Angebot...", "pdf_result": "Extraktionsergebnis", "pdf_prev_result": "Letztes Ergebnis"},
    "Italiano": {"title": "Hub di Commercio Globale", "t1": "📦 Profitto & Previsione", "t2": "📊 Cassaforte", "t3": "🌍 Sala Guerra", "t4": "💼 Testi Multilingue", "name": "Nome Prodotto", "cost": "Costo", "sell": "Prezzo di Vendita", "ship": "Spedizione", "fee": "Commissione %", "calc": "Margine Live", "save": "💾 Salva", "news": "📰 Notizie Finanziarie", "conv": "💱 Convertitore FX", "map_t": "🌍 Radar di Calore E-commerce", "ai_lang_select": "Seleziona le lingue da generare:", "t5": "📄 Estrai PDF", "pdf_title": "Estrattore Info PDF", "pdf_caption": "Carica un preventivo PDF; l'IA estrae nome prodotto, prezzo unitario, MOQ e prezzo totale.", "pdf_upload": "Carica preventivo PDF", "pdf_no_file": "Carica prima un file PDF (.pdf).", "pdf_preview": "Anteprima del testo analizzato", "pdf_pages": "pagine", "pdf_chars": "caratteri", "pdf_btn": "🤖 Estrai informazioni", "pdf_spinner": "L'IA sta analizzando il preventivo...", "pdf_result": "Risultato estrazione", "pdf_prev_result": "Ultimo risultato"},
    "Português": {"title": "Centro de Comércio Global", "t1": "📦 Lucro & Previsão", "t2": "📊 Cofre", "t3": "🌍 Sala de Guerra", "t4": "💼 Textos Multilíngues", "name": "Nome do Produto", "cost": "Custo", "sell": "Preço de Venda", "ship": "Frete", "fee": "Comissão %", "calc": "Margem ao Vivo", "save": "💾 Salvar", "news": "📰 Notícias Financeiras", "conv": "💱 Conversor FX", "map_t": "🌍 Radar de Calor E-commerce", "ai_lang_select": "Selecione os idiomas a gerar:", "t5": "📄 Extrair PDF", "pdf_title": "Extrator de Info de PDF", "pdf_caption": "Envie um orçamento em PDF; a IA extrai nome do produto, preço unitário, MOQ e preço total.", "pdf_upload": "Enviar orçamento PDF", "pdf_no_file": "Envie primeiro um arquivo PDF (.pdf).", "pdf_preview": "Prévia do texto analisado", "pdf_pages": "páginas", "pdf_chars": "caracteres", "pdf_btn": "🤖 Extrair informações", "pdf_spinner": "A IA está analisando o orçamento...", "pdf_result": "Resultado da extração", "pdf_prev_result": "Último resultado"},
    "Русский": {"title": "Глобальный Торговый Центр", "t1": "📦 Прибыль и Прогноз", "t2": "📊 Хранилище", "t3": "🌍 Ситуационный Центр", "t4": "💼 Многоязычные Тексты", "name": "Название товара", "cost": "Закупочная цена", "sell": "Цена продажи", "ship": "Доставка", "fee": "Комиссия %", "calc": "Маржа в реальном времени", "save": "💾 Сохранить", "news": "📰 Финансовые новости", "conv": "💱 Конвертер валют", "map_t": "🌍 Глобальный радар E-commerce", "ai_lang_select": "Выберите языки для генерации:", "t5": "📄 Извлечь из PDF", "pdf_title": "Извлечение данных из PDF", "pdf_caption": "Загрузите PDF-смету поставщика; ИИ извлечёт название товара, цену за единицу, MOQ и общую сумму.", "pdf_upload": "Загрузить PDF-смету", "pdf_no_file": "Сначала загрузите PDF-файл (.pdf).", "pdf_preview": "Предпросмотр текста", "pdf_pages": "стр.", "pdf_chars": "симв.", "pdf_btn": "🤖 Извлечь данные", "pdf_spinner": "ИИ анализирует смету...", "pdf_result": "Результат извлечения", "pdf_prev_result": "Прошлый результат"},
    "日本語": {"title": "グローバル貿易センター", "t1": "📦 利益と予測", "t2": "📊 商品庫", "t3": "🌍 作戦室", "t4": "💼 多言語コピー", "name": "商品名", "cost": "仕入れ価格", "sell": "販売価格", "ship": "送料", "fee": "手数料 %", "calc": "リアルタイム利益率", "save": "💾 保存", "news": "📰 金融ニュース", "conv": "💱 為替換算", "map_t": "🌍 グローバルECヒートレーダー", "ai_lang_select": "生成する言語を選択（複数可）：", "t5": "📄 PDF抽出", "pdf_title": "PDFキー情報抽出", "pdf_caption": "サプライヤーの見積PDFをアップロードすると、AIが商品名・単価・最小注文数・合計額を抽出します。", "pdf_upload": "見積PDFをアップロード", "pdf_no_file": "先にPDFファイル（.pdf）をアップロードしてください。", "pdf_preview": "解析テキストのプレビュー", "pdf_pages": "ページ", "pdf_chars": "文字", "pdf_btn": "🤖 AIで抽出", "pdf_spinner": "AIが見積書を分析中...", "pdf_result": "抽出結果", "pdf_prev_result": "前回の抽出結果"},
    "한국어": {"title": "글로벌 무역 센터", "t1": "📦 수익 및 예측", "t2": "📊 상품 창고", "t3": "🌍 워 룸", "t4": "💼 다국어 카피", "name": "상품명", "cost": "매입가", "sell": "판매가", "ship": "배송비", "fee": "수수료 %", "calc": "실시간 마진", "save": "💾 저장", "news": "📰 금융 뉴스", "conv": "💱 환율 변환", "map_t": "🌍 글로벌 이커머스 히트 레이더", "ai_lang_select": "생성할 언어 선택 (복수 가능):", "t5": "📄 PDF 추출", "pdf_title": "PDF 핵심 정보 추출", "pdf_caption": "공급업체 견적 PDF를 업로드하면 AI가 제품명, 단가, 최소주문수량, 총액을 추출합니다.", "pdf_upload": "견적 PDF 업로드", "pdf_no_file": "먼저 PDF 파일(.pdf)을 업로드하세요.", "pdf_preview": "분석된 텍스트 미리보기", "pdf_pages": "페이지", "pdf_chars": "자", "pdf_btn": "🤖 AI로 추출", "pdf_spinner": "AI가 견적서를 분석 중...", "pdf_result": "추출 결과", "pdf_prev_result": "이전 추출 결과"},
    "ไทย": {"title": "ศูนย์กลางการค้าโลก", "t1": "📦 กำไรและการคาดการณ์", "t2": "📊 คลังสินค้า", "t3": "🌍 ห้องบัญชาการ", "t4": "💼 ข้อความหลายภาษา", "name": "ชื่อสินค้า", "cost": "ราคาทุน", "sell": "ราคาขาย", "ship": "ค่าขนส่ง", "fee": "ค่าธรรมเนียม %", "calc": "อัตรากำไรแบบเรียลไทม์", "save": "💾 บันทึก", "news": "📰 ข่าวการเงิน", "conv": "💱 แปลงสกุลเงิน", "map_t": "🌍 เรดาร์ความร้อนอีคอมเมิร์ซทั่วโลก", "ai_lang_select": "เลือกภาษาที่ต้องการสร้าง:", "t5": "📄 สกัด PDF", "pdf_title": "สกัดข้อมูลสำคัญจาก PDF", "pdf_caption": "อัปโหลด PDF ใบเสนอราคา แล้ว AI จะสกัดชื่อสินค้า ราคาต่อหน่วย ยอดสั่งขั้นต่ำ และราคารวม", "pdf_upload": "อัปโหลด PDF ใบเสนอราคา", "pdf_no_file": "กรุณาอัปโหลดไฟล์ PDF (.pdf) ก่อน", "pdf_preview": "ตัวอย่างข้อความที่วิเคราะห์", "pdf_pages": "หน้า", "pdf_chars": "ตัวอักษร", "pdf_btn": "🤖 AI สกัดข้อมูล", "pdf_spinner": "AI กำลังวิเคราะห์ใบเสนอราคา...", "pdf_result": "ผลการสกัด", "pdf_prev_result": "ผลการสกัดล่าสุด"},
    "Tiếng Việt": {"title": "Trung Tâm Thương Mại Toàn Cầu", "t1": "📦 Lợi Nhuận & Dự Đoán", "t2": "📊 Kho Hàng", "t3": "🌍 Phòng Chiến Lược", "t4": "💼 Văn Bản Đa Ngôn Ngữ", "name": "Tên Sản Phẩm", "cost": "Giá Nhập", "sell": "Giá Bán", "ship": "Phí Vận Chuyển", "fee": "Hoa Hồng %", "calc": "Lợi Nhuận Trực Tiếp", "save": "💾 Lưu", "news": "📰 Tin Tài Chính", "conv": "💱 Chuyển Đổi FX", "map_t": "🌍 Radar Nhiệt TMĐT Toàn Cầu", "ai_lang_select": "Chọn ngôn ngữ cần tạo:", "t5": "📄 Trích xuất PDF", "pdf_title": "Trích xuất thông tin chính từ PDF", "pdf_caption": "Tải lên PDF báo giá; AI trích xuất tên sản phẩm, đơn giá, MOQ và tổng giá.", "pdf_upload": "Tải lên PDF báo giá", "pdf_no_file": "Vui lòng tải lên tệp PDF (.pdf) trước.", "pdf_preview": "Xem trước văn bản đã phân tích", "pdf_pages": "trang", "pdf_chars": "ký tự", "pdf_btn": "🤖 AI trích xuất", "pdf_spinner": "AI đang phân tích báo giá...", "pdf_result": "Kết quả trích xuất", "pdf_prev_result": "Kết quả lần trước"},
    "Türkçe": {"title": "Küresel Ticaret Merkezi", "t1": "📦 Kâr ve Tahmin", "t2": "📊 Kasa", "t3": "🌍 Savaş Odası", "t4": "💼 Çok Dilli Metinler", "name": "Ürün Adı", "cost": "Maliyet", "sell": "Satış Fiyatı", "ship": "Kargo", "fee": "Komisyon %", "calc": "Canlı Marj", "save": "💾 Kaydet", "news": "📰 Finans Haberleri", "conv": "💱 Döviz Çevirici", "map_t": "🌍 Küresel E-ticaret Isı Radarı", "ai_lang_select": "Oluşturulacak dilleri seçin:", "t5": "📄 PDF Çıkar", "pdf_title": "PDF Ana Bilgi Çıkarıcı", "pdf_caption": "Tedarikçi teklif PDF'i yükleyin; AI ürün adı, birim fiyat, MOQ ve toplam fiyatı çıkarır.", "pdf_upload": "Teklif PDF'i yükle", "pdf_no_file": "Önce bir PDF dosyası (.pdf) yükleyin.", "pdf_preview": "Ayrıştırılan metin önizlemesi", "pdf_pages": "sayfa", "pdf_chars": "karakter", "pdf_btn": "🤖 AI Bilgi Çıkar", "pdf_spinner": "AI teklifi analiz ediyor...", "pdf_result": "Çıkarma Sonucu", "pdf_prev_result": "Son Sonuç"},
    "العربية": {"title": "مركز التجارة العالمي", "t1": "📦 الربح والتنبؤ", "t2": "📊 المخزن", "t3": "🌍 غرفة العمليات", "t4": "💼 نصوص متعددة اللغات", "name": "اسم المنتج", "cost": "سعر الشراء", "sell": "سعر البيع", "ship": "الشحن", "fee": "العمولة %", "calc": "الهامش الفوري", "save": "💾 حفظ", "news": "📰 أخبار مالية", "conv": "💱 محول العملات", "map_t": "🌍 رادار حرارة التجارة الإلكترونية", "ai_lang_select": "اختر اللغات المطلوب إنشاؤها:", "t5": "📄 استخراج PDF", "pdf_title": "استخراج المعلومات من PDF", "pdf_caption": "حمّل ملف عرض سعر PDF وسيستخرج الذكاء الاصطناعي اسم المنتج وسعر الوحدة والحد الأدنى للطلب والسعر الإجمالي.", "pdf_upload": "تحميل عرض السعر PDF", "pdf_no_file": "يرجى تحميل ملف PDF (.pdf) أولاً.", "pdf_preview": "معاينة النص المستخرج", "pdf_pages": "صفحات", "pdf_chars": "حرف", "pdf_btn": "🤖 استخراج المعلومات", "pdf_spinner": "الذكاء الاصطناعي يحلل عرض السعر...", "pdf_result": "نتيجة الاستخراج", "pdf_prev_result": "النتيجة السابقة"},
    "हिन्दी": {"title": "वैश्विक व्यापार केंद्र", "t1": "📦 लाभ और पूर्वानुमान", "t2": "📊 भंडार", "t3": "🌍 युद्ध कक्ष", "t4": "💼 बहुभाषी पाठ", "name": "उत्पाद का नाम", "cost": "लागत मूल्य", "sell": "बिक्री मूल्य", "ship": "शिपिंग", "fee": "कमीशन %", "calc": "लाइव मार्जिन", "save": "💾 सहेजें", "news": "📰 वित्तीय समाचार", "conv": "💱 मुद्रा परिवर्तक", "map_t": "🌍 वैश्विक ई-कॉमर्स हीट रडार", "ai_lang_select": "बनाने के लिए भाषाएँ चुनें:", "t5": "📄 PDF निकालें", "pdf_title": "PDF मुख्य जानकारी निकालना", "pdf_caption": "आपूर्तिकर्ता का कोटेशन PDF अपलोड करें; AI उत्पाद का नाम, इकाई मूल्य, MOQ और कुल मूल्य निकालेगा।", "pdf_upload": "कोटेशन PDF अपलोड करें", "pdf_no_file": "कृपया पहले एक PDF फ़ाइल (.pdf) अपलोड करें।", "pdf_preview": "विश्लेषित टेक्स्ट का पूर्वावलोकन", "pdf_pages": "पृष्ठ", "pdf_chars": "अक्षर", "pdf_btn": "🤖 AI जानकारी निकालें", "pdf_spinner": "AI कोटेशन का विश्लेषण कर रहा है...", "pdf_result": "निकाला गया परिणाम", "pdf_prev_result": "पिछला परिणाम"},
    "Nederlands": {"title": "Wereldwijd Handelscentrum", "t1": "📦 Winst & Voorspelling", "t2": "📊 Kluis", "t3": "🌍 Oorlogskamer", "t4": "💼 Meertalige Teksten", "name": "Productnaam", "cost": "Inkoopprijs", "sell": "Verkoopprijs", "ship": "Verzending", "fee": "Commissie %", "calc": "Live Marge", "save": "💾 Opslaan", "news": "📰 Financieel Nieuws", "conv": "💱 Valuta-omzetter", "map_t": "🌍 Wereldwijde E-commerce Hitte Radar", "ai_lang_select": "Kies de te genereren talen:", "t5": "📄 PDF extraheren", "pdf_title": "PDF Info-extractor", "pdf_caption": "Upload een offerte-PDF; de AI haalt productnaam, eenheidsprijs, MOQ en totaalprijs eruit.", "pdf_upload": "Offerte-PDF uploaden", "pdf_no_file": "Upload eerst een PDF-bestand (.pdf).", "pdf_preview": "Voorbeeld van de geanalyseerde tekst", "pdf_pages": "pagina's", "pdf_chars": "tekens", "pdf_btn": "🤖 Info extraheren", "pdf_spinner": "AI analyseert de offerte...", "pdf_result": "Extractieresultaat", "pdf_prev_result": "Laatste resultaat"},
    "Polski": {"title": "Globalne Centrum Handlu", "t1": "📦 Zysk i Prognoza", "t2": "📊 Skarbiec", "t3": "🌍 Centrum Dowodzenia", "t4": "💼 Teksty Wielojęzyczne", "name": "Nazwa Produktu", "cost": "Cena Zakupu", "sell": "Cena Sprzedaży", "ship": "Wysyłka", "fee": "Prowizja %", "calc": "Marża na Żywo", "save": "💾 Zapisz", "news": "📰 Wiadomości Finansowe", "conv": "💱 Przelicznik Walut", "map_t": "🌍 Globalny Radar E-commerce", "ai_lang_select": "Wybierz języki do wygenerowania:", "t5": "📄 Wyodrębnij PDF", "pdf_title": "Wyodrębnianie informacji z PDF", "pdf_caption": "Prześlij ofertę PDF; AI wyodrębni nazwę produktu, cenę jednostkową, MOQ i cenę całkowitą.", "pdf_upload": "Prześlij ofertę PDF", "pdf_no_file": "Najpierw prześlij plik PDF (.pdf).", "pdf_preview": "Podgląd przeanalizowanego tekstu", "pdf_pages": "stron", "pdf_chars": "znaków", "pdf_btn": "🤖 Wyodrębnij informacje", "pdf_spinner": "AI analizuje ofertę...", "pdf_result": "Wynik wyodrębniania", "pdf_prev_result": "Ostatni wynik"},
    "Українська": {"title": "Глобальний Торговий Центр", "t1": "📦 Прибуток і Прогноз", "t2": "📊 Сховище", "t3": "🌍 Штаб", "t4": "💼 Багатомовні Тексти", "name": "Назва товару", "cost": "Закупівельна ціна", "sell": "Ціна продажу", "ship": "Доставка", "fee": "Комісія %", "calc": "Маржа в реальному часі", "save": "💾 Зберегти", "news": "📰 Фінансові новини", "conv": "💱 Конвертер валют", "map_t": "🌍 Глобальний радар E-commerce", "ai_lang_select": "Виберіть мови для генерації:", "t5": "📄 Витягти з PDF", "pdf_title": "Витягнення даних з PDF", "pdf_caption": "Завантажте кошторис PDF; ШІ витягне назву товару, ціну за одиницю, MOQ та загальну суму.", "pdf_upload": "Завантажити кошторис PDF", "pdf_no_file": "Спочатку завантажте PDF-файл (.pdf).", "pdf_preview": "Перегляд тексту", "pdf_pages": "стор.", "pdf_chars": "симв.", "pdf_btn": "🤖 Витягти дані", "pdf_spinner": "ШІ аналізує кошторис...", "pdf_result": "Результат витягнення", "pdf_prev_result": "Попередній результат"},
    "Tagalog": {"title": "Pandaigdigang Sentro ng Kalakalan", "t1": "📦 Kita at Hula", "t2": "📊 Imbakan", "t3": "🌍 War Room", "t4": "💼 Maramihang Wika", "name": "Pangalan ng Produkto", "cost": "Puhunan", "sell": "Presyo ng Benta", "ship": "Shipping", "fee": "Komisyon %", "calc": "Live na Margin", "save": "💾 I-save", "news": "📰 Balitang Pinansyal", "conv": "💱 Palitan ng FX", "map_t": "🌍 Pandaigdigang E-commerce Heat Radar", "ai_lang_select": "Pumili ng mga wikang gagawin:", "t5": "📄 Kunin sa PDF", "pdf_title": "PDF Info Extractor", "pdf_caption": "Mag-upload ng PDF ng quotation; kukunin ng AI ang pangalan ng produkto, unit price, MOQ at kabuuang presyo.", "pdf_upload": "I-upload ang PDF ng quotation", "pdf_no_file": "Mag-upload muna ng PDF file (.pdf).", "pdf_preview": "Preview ng na-parse na teksto", "pdf_pages": "pahina", "pdf_chars": "char", "pdf_btn": "🤖 Kunin ang impormasyon", "pdf_spinner": "Sinusuri ng AI ang quotation...", "pdf_result": "Resulta ng pagkuha", "pdf_prev_result": "Huling resulta"}
}

col_lang, col_theme = st.columns([4, 1])
with col_lang:
    ui_lang = st.selectbox("🌐 界面语言 / Language", list(UI_TRANSLATIONS.keys()), label_visibility="collapsed")
with col_theme:
    is_dark = st.toggle("🌙 Dark Mode", value=True)
t = UI_TRANSLATIONS[ui_lang]

# ================= 2. 顶级 UI (完美适配黑白) =================
if is_dark:
    bg_color, text_color = "#0B0F19", "#E2E8F0"
    card_bg, border_color = "rgba(30, 41, 59, 0.5)", "rgba(255, 255, 255, 0.1)"
    map_style = "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json"
    arc_color = [56, 189, 248, 200]
    target_color = [192, 132, 252, 255]
else:
    bg_color, text_color = "#F8FAFC", "#0F172A"
    card_bg, border_color = "rgba(255, 255, 255, 0.9)", "rgba(0, 0, 0, 0.05)"
    map_style = "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json" # 浅色地图
    arc_color = [59, 130, 246, 200]
    target_color = [139, 92, 246, 255]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif !important; }}
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    
    /* 修复输入框和背景的冲突 */
    div[data-baseweb="input"], div[data-baseweb="select"], textarea {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    header {{visibility: hidden;}} footer {{visibility: hidden;}}
    .title-text {{
        font-size: 3.5em !important; font-weight: 800; letter-spacing: -1.5px;
        background: linear-gradient(90deg, #FFD700 0%, #818CF8 50%, #FF8C00 100%);
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
        return res.json()["choices"][0]["message"]["content"] if res.status_code == 200 else "❌ 报错"
    except: return "❌ 失败"

# ================= 4. 核心模块 =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"], t["t5"]])

# 页面 1：利润与预测
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input(t["name"], "Muslim Clothes")
        c_cost = st.number_input(t["cost"], value=25.0)
    with col2:
        s_sell = st.number_input(t["sell"], value=72.0)
        s_curr = st.selectbox("Sell Currency", currency_list, index=0)
    ship = st.number_input(t["ship"], value=8.0)
    fee = st.number_input(t["fee"], value=10.0)
    
    if rates:
        real_profit = s_sell - c_cost - ship - (s_sell * (fee/100))
        margin = (real_profit / s_sell) * 100 if s_sell > 0 else 0
        st.markdown(f"#### {t['calc']}")
        st.success(f"🟢 **{real_profit:.2f} {s_curr}** (Margin: {margin:.1f}%)")
        if st.button(t["save"]):
            df_new = pd.DataFrame([{"Product": p_name, "Cost": c_cost, "Sell": s_sell, "Currency": s_curr, "Profit": round(real_profit,2), "Margin": round(margin,1)}])
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
        get_source_color=arc_color,
        get_target_color=target_color,
        get_width=3, pickable=True,
    )

    target_layer_glow = pdk.Layer(
        "ScatterplotLayer", data=df_arcs,
        get_position=["to_lon", "to_lat"],
        get_radius="volume * 30",
        get_fill_color=target_color[:3] + [60],
        pickable=False,
    )

    target_layer_core = pdk.Layer(
        "ScatterplotLayer", data=df_arcs,
        get_position=["to_lon", "to_lat"],
        get_radius="volume * 8", 
        get_fill_color=[255, 255, 255, 200] if is_dark else [50, 50, 50, 200],
        pickable=True,
    )

    origin_layer = pdk.Layer(
        "ScatterplotLayer", data=[origin],
        get_position=["lon", "lat"],
        get_radius=50000,
        get_fill_color=arc_color[:3] + [255],
    )

    view_state = pdk.ViewState(
        longitude=80.0, latitude=20.0, zoom=1.2, pitch=45, bearing=0,
    )

    st.pydeck_chart(pdk.Deck(
        map_style=map_style,
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
    available_langs = ["English", "Bahasa Melayu", "中文 (Chinese)", "ไทย (Thai)", "Tiếng Việt", "Español"]
    selected_langs = st.multiselect(t["ai_lang_select"], available_langs, default=["English", "Bahasa Melayu"])
    if st.button("生成多国文案"):
        if not selected_langs:
            st.warning("请至少选择一种语言！")
        else:
            with st.spinner("AI 正在生成..."):
                lang_str = ", ".join(selected_langs)
                prompt = f"商品：{bulk_prod}。请输出一个 Markdown 表格：| 语言 | 标题 | 3个卖点 |。请严格按照以下语言生成：{lang_str}。"
                st.markdown(call_groq(prompt, 0.4))

# ================= 5. PDF 关键信息提取（已整合进本文件） =================
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

MAX_PDF_CHARS = 15000  # 限制文本长度，避免超出模型上下文


def extract_pdf_text(file_bytes):
    """从 PDF 字节流抽取纯文本，返回 (text, pages, error)。"""
    if not HAS_PYPDF:
        return None, 0, "未安装 pypdf，请在终端执行: pip install pypdf"
    import io
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return None, 0, "PDF 已加密，无法读取"
        parts = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(parts).strip()
        if not text:
            return None, len(reader.pages), "没有提取到文字（可能是扫描版 PDF，需要 OCR）"
        return text[:MAX_PDF_CHARS], len(reader.pages), None
    except Exception as exc:
        return None, 0, f"PDF 解析失败：{exc}"


def build_pdf_prompt(text):
    return (
        "你是采购助理。下面是从供应商报价单 PDF 中提取的文本，"
        "请提取关键信息，只输出一个 Markdown 表格，列固定为：\n"
        "| 产品名称 | 单价 | 起订量 | 总价 | 备注 |\n"
        "要求：\n"
        "1. 报价单里有多个产品就输出多行；\n"
        "2. 价格必须保留原币种（如 USD、RMB、MYR）；\n"
        "3. 找不到的字段写“未提及”，禁止编造；\n"
        "4. 不要输出表格以外的任何内容。\n\n"
        f"<报价单文本>\n{text}\n</报价单文本>"
    )


# 页面 5：PDF 关键信息提取
with tab5:
    st.markdown(f"### {t['pdf_title']}")
    st.caption(t["pdf_caption"])

    pdf_file = st.file_uploader(t["pdf_upload"], type=["pdf"], key="quote_pdf")

    if pdf_file is None:
        st.info(t["pdf_no_file"])
        # 文件被移除时仍保留上次结果
        if st.session_state.get("pdf_result"):
            st.markdown(f"#### 📋 {t['pdf_prev_result']}")
            st.markdown(st.session_state["pdf_result"])
    else:
        # 换了文件才重新解析，避免每次交互都重跑
        file_key = f"{pdf_file.name}_{pdf_file.size}"
        if st.session_state.get("pdf_text_key") != file_key:
            text, pages, err = extract_pdf_text(pdf_file.getvalue())
            if err:
                st.session_state.pop("pdf_text", None)
                st.session_state.pop("pdf_text_key", None)
                st.session_state.pop("pdf_result", None)
                st.error(err)
            else:
                st.session_state["pdf_text"] = text
                st.session_state["pdf_text_key"] = file_key
                st.session_state["pdf_pages"] = pages
                st.session_state.pop("pdf_result", None)  # 新文件清掉旧结果

        if st.session_state.get("pdf_text"):
            text = st.session_state["pdf_text"]
            pages = st.session_state.get("pdf_pages", "?")
            with st.expander(f"📃 {t['pdf_preview']} · {pages} {t['pdf_pages']} · {len(text)} {t['pdf_chars']}", expanded=False):
                st.text(text[:3000])

            if st.button(t["pdf_btn"], key="pdf_extract_btn"):
                with st.spinner(t["pdf_spinner"]):
                    result = call_groq(build_pdf_prompt(text), 0.2)
                if isinstance(result, str) and result.startswith("❌"):
                    st.error(result)
                else:
                    st.session_state["pdf_result"] = result

            if st.session_state.get("pdf_result"):
                st.markdown(f"#### 📋 {t['pdf_result']}")
                st.markdown(st.session_state["pdf_result"])
