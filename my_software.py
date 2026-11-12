import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from html import escape
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

_COMPARE_TAB_LABELS = {
    "简体中文": "🏆 比价中心",
    "English": "🏆 Compare",
    "Bahasa Melayu": "🏆 Banding Harga",
    "Español": "🏆 Comparar",
    "繁體中文": "🏆 比價中心",
    "Bahasa Indonesia": "🏆 Bandingkan",
    "Français": "🏆 Comparer",
    "Deutsch": "🏆 Vergleichen",
    "Italiano": "🏆 Confronta",
    "Português": "🏆 Comparar",
    "Русский": "🏆 Сравнить",
    "日本語": "🏆 比較",
    "한국어": "🏆 비교",
    "ไทย": "🏆 เปรียบเทียบ",
    "Tiếng Việt": "🏆 So sánh",
    "Türkçe": "🏆 Karşılaştır",
    "العربية": "🏆 مقارنة",
    "हिन्दी": "🏆 तुलना",
    "Nederlands": "🏆 Vergelijken",
    "Polski": "🏆 Porównaj",
    "Українська": "🏆 Порівняти",
    "Tagalog": "🏆 Ihambing",
}
for _lang, _label in _COMPARE_TAB_LABELS.items():
    if _lang in UI_TRANSLATIONS:
        UI_TRANSLATIONS[_lang]["t6"] = _label

_EXTRA_TAB_LABELS = {
    "简体中文": ("💰 利润沙盘", "🔍 选品雷达"),
    "English": ("💰 Sandbox", "🔍 Product Radar"),
    "Bahasa Melayu": ("💰 Simulasi Untung", "🔍 Radar Produk"),
    "Español": ("💰 Simulador", "🔍 Radar de Productos"),
    "繁體中文": ("💰 利潤沙盤", "🔍 選品雷達"),
    "Bahasa Indonesia": ("💰 Simulasi Laba", "🔍 Radar Produk"),
    "Français": ("💰 Simulateur", "🔍 Radar Produits"),
    "Deutsch": ("💰 Sandbox", "🔍 Produkt-Radar"),
    "Italiano": ("💰 Simulatore", "🔍 Radar Prodotti"),
    "Português": ("💰 Simulador", "🔍 Radar de Produtos"),
    "Русский": ("💰 Песочница", "🔍 Радар товаров"),
    "日本語": ("💰 利益シミュレーター", "🔍 商品レーダー"),
    "한국어": ("💰 수익 샌드박스", "🔍 상품 레이더"),
    "ไทย": ("💰 จำลองกำไร", "🔍 เรดาร์สินค้า"),
    "Tiếng Việt": ("💰 Mô phỏng", "🔍 Radar sản phẩm"),
    "Türkçe": ("💰 Simülasyon", "🔍 Ürün Radarı"),
    "العربية": ("💰 محاكاة", "🔍 رادار المنتجات"),
    "हिन्दी": ("💰 सिम्युलेटर", "🔍 उत्पाद रडार"),
    "Nederlands": ("💰 Sandbox", "🔍 Productradar"),
    "Polski": ("💰 Symulacja", "🔍 Radar produktów"),
    "Українська": ("💰 Симулятор", "🔍 Радар товарів"),
    "Tagalog": ("💰 Simulator", "🔍 Product Radar"),
}
for _lang, (_t7, _t8) in _EXTRA_TAB_LABELS.items():
    if _lang in UI_TRANSLATIONS:
        UI_TRANSLATIONS[_lang]["t7"] = _t7
        UI_TRANSLATIONS[_lang]["t8"] = _t8

col_lang, col_theme = st.columns([4, 1])
with col_lang:
    ui_lang = st.selectbox("🌐 界面语言 / Language", list(UI_TRANSLATIONS.keys()), label_visibility="collapsed")
with col_theme:
    is_dark = st.toggle("🌙 Dark Mode", value=True)
t = UI_TRANSLATIONS[ui_lang]

# ================= 2. 顶级 UI (完美适配黑白) =================
if is_dark:
    bg_color, text_color = "#0A0A0C", "#F3EEE3"
    card_bg, border_color = "rgba(20, 20, 23, 0.72)", "rgba(212, 175, 55, 0.22)"
    map_style = "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json"
    arc_color = [212, 175, 55, 210]
    target_color = [240, 217, 140, 255]
else:
    bg_color, text_color = "#FBF8F1", "#1A1408"
    card_bg, border_color = "rgba(255, 253, 247, 0.94)", "rgba(140, 107, 31, 0.20)"
    map_style = "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json" # 浅色地图
    arc_color = [176, 137, 43, 210]
    target_color = [201, 162, 39, 255]

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
        background: linear-gradient(90deg, #FFD700 0%, #B8892B 50%, #FF8C00 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; padding-bottom: 10px;
    }}
    div[data-testid="stVerticalBlock"] > div {{
        background: {card_bg}; backdrop-filter: blur(12px);
        border-radius: 16px; border: 1px solid {border_color}; padding: 15px;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #D4AF37 0%, #F0D98C 55%, #B8892B 100%);
        color: #14100A; border-radius: 12px; border: 1px solid rgba(255, 236, 179, .35);
        padding: 12px 28px; font-weight: 700; font-size: 16px; letter-spacing: .01em;
    }}
    .stTabs [data-baseweb="tab"] {{ font-size: 18px; font-weight: 600; padding: 10px 0; border-bottom: 3px solid transparent; }}
    .stTabs [aria-selected="true"] {{ border-bottom: 3px solid #D4AF37 !important; color: #D4AF37 !important; }}
</style>
""", unsafe_allow_html=True)

# ===== 国际商务风皮肤：背景 / 发光结果卡 / 呼吸灯按钮 =====
if is_dark:
    _biz_bg = (
        "radial-gradient(1200px 680px at 10% -14%, rgba(212,175,55,.13), transparent 62%),"
        "radial-gradient(900px 560px at 92% -6%, rgba(140,107,31,.12), transparent 60%),"
        "radial-gradient(760px 520px at 50% 114%, rgba(212,175,55,.05), transparent 62%),"
        "linear-gradient(rgba(212,175,55,.045) 1px, transparent 1px),"
        "linear-gradient(90deg, rgba(212,175,55,.045) 1px, transparent 1px),"
        "linear-gradient(180deg, #050506 0%, #0B0B0D 58%, #08080A 100%)"
    )
    _biz_size = "auto, auto, auto, 46px 46px, 46px 46px, auto"
    _biz_glow = "212,175,55"
    _gold_grad = "linear-gradient(94deg,#F8EFCE 0%,#D4AF37 52%,#A97F1E 100%)"
else:
    _biz_bg = (
        "radial-gradient(1000px 560px at 10% -10%, rgba(176,137,43,.10), transparent 62%),"
        "radial-gradient(820px 500px at 92% -4%, rgba(140,107,31,.08), transparent 60%),"
        "linear-gradient(rgba(140,107,31,.06) 1px, transparent 1px),"
        "linear-gradient(90deg, rgba(140,107,31,.06) 1px, transparent 1px),"
        "linear-gradient(180deg, #FCFAF4 0%, #F6F1E4 60%, #F1EAD8 100%)"
    )
    _biz_size = "auto, auto, 46px 46px, 46px 46px, auto"
    _biz_glow = "176,137,43"
    _gold_grad = "linear-gradient(94deg,#2B2210 0%,#8C6B1F 55%,#A97F1E 100%)"

_BIZ_CSS = """
<style>
/* ===== 国际商务风背景：深海军蓝 + 细网格 + 光晕 ===== */
.stApp{
  background-color: __BG__ !important;
  background-image: __BIMG__ !important;
  background-size: __BSIZE__ !important;
  background-attachment: fixed !important;
  color: __TEXT__ !important;
}

/* ===== 按钮：呼吸灯 ===== */
@keyframes gx-breathe{
  0%,100%{box-shadow:0 0 0 0 rgba(__GLOW__,0), 0 0 0 0 rgba(129,140,248,0);}
  50%{box-shadow:0 0 16px rgba(__GLOW__,.55), 0 0 38px rgba(129,140,248,.28);}
}
.stButton>button, .stDownloadButton>button, [data-testid="stDownloadButton"] button{
  animation: gx-breathe 3.4s ease-in-out infinite;
  transition: transform .18s ease, filter .18s ease, box-shadow .18s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover, [data-testid="stDownloadButton"] button:hover{
  animation-play-state: paused;
  transform: translateY(-1px);
  filter: brightness(1.08);
  box-shadow: 0 0 22px rgba(__GLOW__,.75), 0 6px 24px rgba(0,0,0,.25);
}
.stButton>button:active, .stDownloadButton>button:active, [data-testid="stDownloadButton"] button:active{transform: translateY(0);}
@media (prefers-reduced-motion: reduce){
  .stButton>button, .stDownloadButton>button, [data-testid="stDownloadButton"] button{animation:none !important;}
}

/* ===== 提取结果卡片：发光边框（放表格的 markdown 容器） ===== */
@keyframes gx-glow{
  0%,100%{box-shadow:0 0 10px rgba(__GLOW__,.22), inset 0 0 18px rgba(__GLOW__,.04);}
  50%{box-shadow:0 0 28px rgba(__GLOW__,.55), inset 0 0 26px rgba(__GLOW__,.12);}
}
[data-testid="stMarkdownContainer"]:has(table){
  position:relative;
  border-radius:14px;
  border:1px solid rgba(__GLOW__,.55);
  background:rgba(__GLOW__,.05);
  padding:10px 12px;
  animation:gx-glow 3.2s ease-in-out infinite;
}
[data-testid="stMarkdownContainer"] table{border-collapse:separate; border-spacing:0; width:100%;}
[data-testid="stMarkdownContainer"] thead th{
  background:rgba(__GLOW__,.14) !important;
  color:__TEXT__ !important;
  border-bottom:1px solid rgba(__GLOW__,.35) !important;
  font-weight:700; letter-spacing:.02em; padding:10px 12px !important;
}
[data-testid="stMarkdownContainer"] tbody td{
  border-bottom:1px solid __BORDER__ !important;
  padding:9px 12px !important;
  color:__TEXT__ !important;
}
[data-testid="stMarkdownContainer"] tbody tr:hover td{background:rgba(__GLOW__,.07);}
[data-testid="stMarkdownContainer"] tbody tr:last-child td{border-bottom:none !important;}

/* ===== 标题光晕 / 卡片质感 ===== */
.title-text{filter:drop-shadow(0 0 18px rgba(__GLOW__,.35));}
div[data-testid="stVerticalBlock"] > div{box-shadow:0 10px 30px rgba(0,0,0,.16);}
</style>
"""
st.markdown(
    _BIZ_CSS.replace("__BG__", bg_color)
    .replace("__BIMG__", _biz_bg)
    .replace("__BSIZE__", _biz_size)
    .replace("__TEXT__", text_color)
    .replace("__BORDER__", border_color)
    .replace("__GLOW__", _biz_glow)
    .replace("__GOLDGRAD__", _gold_grad),
    unsafe_allow_html=True,
)

# ===== UI v3：Hero / 胶囊 Tab / KPI / 精致卡片 =====
_ui_text = text_color
_ui_muted = "rgba(148,163,184,.85)" if is_dark else "rgba(71,85,105,.8)"
_ui_card = "rgba(30,41,59,.55)" if is_dark else "rgba(255,255,255,.92)"
_ui_menu = "#0E1626" if is_dark else "#FFFFFF"
_ui_accent = "#D4AF37" if is_dark else "#0284C7"

_UI3_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
/* ---------- 基础排印 ---------- */
html, body, .stApp{font-family:'Inter','Outfit',-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif !important;}
[data-testid="stMainBlockContainer"], .block-container{padding-top:1.1rem !important; max-width:1420px !important;}
[data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] p, label{color:__TEXT__ !important;}
[data-testid="stCaptionContainer"] p{color:__MUTED__ !important;}

/* ---------- Hero ---------- */
.hero{padding:2px 2px 0;}
.hero .eyebrow{font-size:10px;letter-spacing:.32em;text-transform:uppercase;color:__MUTED__;font-weight:700;}
.hero .title{font-size:clamp(28px,3.3vw,44px);font-weight:800;letter-spacing:-1.2px;line-height:1.12;margin:8px 0 0;
 background:__GOLDGRAD__;
 -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
 font-family:'Cormorant Garamond','Playfair Display',Georgia,'Songti SC',serif;font-weight:700;letter-spacing:-.6px;}
.hero .sub{color:__MUTED__;font-size:13px;margin-top:8px;letter-spacing:.02em;}
.hero .chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;}
.hero .chip{display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:999px;
 border:1px solid __BORDER__;background:__CARD__;color:__MUTED__;font-size:11px;font-weight:600;}
.hero .chip b{color:__TEXT__;font-weight:800;}
.hero .dot{width:6px;height:6px;border-radius:50%;background:#4FB28C;box-shadow:0 0 0 3px rgba(52,211,153,.16);}
.hero .rule{height:1px;margin-top:16px;background:linear-gradient(90deg,transparent,rgba(__GLOW__,.45) 18%,rgba(__GLOW__,.45) 82%,transparent);}
.hero .clocks{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:12px;align-items:baseline;}
.hero .mk{display:inline-flex;align-items:baseline;gap:7px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:__MUTED__;}
.hero .mk b{color:__TEXT__;font-weight:700;letter-spacing:.16em;}
.hero .mk em{font-style:normal;font-variant-numeric:tabular-nums;color:__ACCENT__;font-weight:700;letter-spacing:.06em;}

/* ---------- Tabs（React Aria） ---------- */
[data-testid="stTabs"] [role="tablist"]{gap:6px !important;border-bottom:1px solid __BORDER__ !important;}
[data-testid="stTab"]{border-radius:10px 10px 0 0 !important;padding:7px 14px !important;color:__MUTED__ !important;background:transparent !important;}
[data-testid="stTab"] p{font-size:14px !important;font-weight:600 !important;color:inherit !important;}
[data-testid="stTab"]:hover{background:rgba(__GLOW__,.08) !important;color:__TEXT__ !important;}
[data-testid="stTab"][data-selected="true"]{background:rgba(__GLOW__,.13) !important;color:__TEXT__ !important;}
[data-testid="stTab"] .react-aria-SelectionIndicator{background:linear-gradient(90deg,__ACCENT__,#F0D98C) !important;height:2px !important;}

/* ---------- 输入控件 ---------- */
[data-testid="stSelectbox"] div[role="group"],[data-testid="stMultiSelect"] div[role="group"],
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"],[data-testid="stTextAreaRootElement"]{
 background:rgba(__GLOW__,.035) !important;border:1px solid __BORDER__ !important;border-radius:12px !important;
 transition:border-color .18s,box-shadow .18s;}
[data-testid="stSelectbox"] div[role="group"]:focus-within,[data-testid="stMultiSelect"] div[role="group"]:focus-within,
[data-testid="stTextInputRootElement"]:focus-within,[data-testid="stNumberInputContainer"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within{border-color:__ACCENT__ !important;box-shadow:0 0 0 3px rgba(__GLOW__,.15) !important;}
input,textarea,[data-testid="stSelectbox"] input[role="combobox"]{color:__TEXT__ !important;}
[role="listbox"]{background:__MENU__ !important;border:1px solid __BORDER__ !important;border-radius:12px !important;}

/* ---------- 卡片 / 面板 ---------- */
div[data-testid="stVerticalBlock"] > div{border-radius:18px !important;padding:16px 18px !important;
 border:1px solid __BORDER__ !important;background:__CARD__ !important;}
[data-testid="stExpander"] details{border-radius:14px !important;border:1px solid __BORDER__ !important;background:__CARD__ !important;}
[data-testid="stFileUploader"] section{border-radius:14px !important;border:1px dashed rgba(__GLOW__,.45) !important;
 background:rgba(__GLOW__,.04) !important;}
[data-testid="stMetricValue"]{color:__TEXT__ !important;font-weight:800 !important;}
[data-testid="stMetricLabel"] p{color:__MUTED__ !important;}
[data-testid="stAlert"]{border-radius:14px !important;}

/* ---------- KPI ---------- */
.kpi-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:16px 0 10px;}
@media(max-width:900px){.kpi-row{grid-template-columns:repeat(2,minmax(0,1fr));}}
.kpi{position:relative;padding:14px 16px;border-radius:16px;border:1px solid __BORDER__;
 background:linear-gradient(180deg,rgba(__GLOW__,.07),transparent 72%);overflow:hidden;}
.kpi:before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;
 background:linear-gradient(90deg,__ACCENT__,#F0D98C);opacity:.9;}
.kpi .k{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:__MUTED__;font-weight:700;}
.kpi .v{font-size:22px;font-weight:800;color:__TEXT__;margin-top:6px;font-variant-numeric:tabular-nums;letter-spacing:-.02em;}
.kpi .v small{font-size:12px;font-weight:700;opacity:.75;}
.kpi .d{font-size:11px;color:__MUTED__;margin-top:4px;}
.kpi .good{color:#4FB28C;} .kpi .bad{color:#E06C5A;}

/* ---------- 区块标题 ---------- */
.sec{display:flex;align-items:center;gap:10px;margin:6px 0 2px;}
.sec .bullet{width:8px;height:8px;border-radius:2px;background:linear-gradient(135deg,__ACCENT__,#F0D98C);
 box-shadow:0 0 12px rgba(__GLOW__,.6);}
.sec .t{font-size:15px;font-weight:800;color:__TEXT__;letter-spacing:-.01em;}
.sec .s{font-size:11px;color:__MUTED__;margin-left:auto;}
</style>
"""
st.markdown(
    _UI3_CSS.replace("__TEXT__", _ui_text)
    .replace("__MUTED__", _ui_muted)
    .replace("__CARD__", _ui_card)
    .replace("__MENU__", _ui_menu)
    .replace("__ACCENT__", _ui_accent)
    .replace("__BORDER__", border_color)
    .replace("__GLOW__", _biz_glow)
    .replace("__GOLDGRAD__", _gold_grad),
    unsafe_allow_html=True,
)

_CLOCKS = [
    ("Shenzhen", "Asia/Shanghai"), ("Singapore", "Asia/Singapore"), ("Dubai", "Asia/Dubai"),
    ("London", "Europe/London"), ("New York", "America/New_York"),
]


def _city_clock(tz_name):
    try:
        return datetime.now(ZoneInfo(tz_name)).strftime("%H:%M")
    except Exception:
        return "--:--"


_clocks_html = "".join(
    f'<span class="mk"><b>{city}</b><em>{_city_clock(tz)}</em></span>' for city, tz in _CLOCKS
)
st.markdown(
    '<div class="hero">'
    '<div class="eyebrow">Global Trade Operations Console</div>'
    f'<div class="title">{escape(t["title"])}</div>'
    '<div class="sub">Profit · Sourcing · Logistics · Listings · Reverse Engineering</div>'
    '<div class="chips">'
    '<span class="chip"><i class="dot"></i>LIVE</span>'
    '<span class="chip"><b>22</b> languages</span>'
    '<span class="chip"><b>5</b> modules</span>'
    '<span class="chip">AI ready</span>'
    '</div>'
    f'<div class="clocks">{_clocks_html}</div>'
    '<div class="rule"></div></div>',
    unsafe_allow_html=True,
)

# ================= 3. 数据工具 =================
@st.cache_data(ttl=1800)
def get_rates():
    """汇率（USD 基准）：超时 10 秒、失败重试一次，仍失败返回 None。"""
    for _ in range(2):
        try:
            res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
            data = res.json()
            if isinstance(data.get("rates"), dict) and data["rates"]:
                return data["rates"]
        except Exception:
            continue
    return None


rates = get_rates()
currency_list = ["MYR", "CNY", "USD", "EUR", "GBP", "SGD", "JPY", "THB"]


def call_groq(prompt, temp=0.5, max_tokens=2000):
    """调用 Groq：任何失败都返回带原因的中文提示，绝不抛异常拖垮页面。"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ 未配置 Key。请在终端执行: export GROQ_API_KEY='gsk_xxx'"
    payload = {
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temp,
        "max_tokens": max_tokens,
    }
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=90,
        )
    except requests.Timeout:
        return "❌ AI 请求超时（90 秒），请检查网络后重试。"
    except Exception as exc:
        return f"❌ 网络异常：{type(exc).__name__}"
    if res.status_code != 200:
        detail = ""
        try:
            detail = res.json().get("error", {}).get("message", "")
        except Exception:
            detail = (res.text or "")[:160]
        return f"❌ AI 调用失败（HTTP {res.status_code}）" + (f"：{detail}" if detail else "")
    try:
        content = res.json()["choices"][0]["message"]["content"]
    except Exception:
        return "❌ AI 返回格式异常"
    return content or "❌ AI 返回内容为空"


# ================= 3.1 选品库读写（容错） =================
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_selection.csv")
VAULT_COLUMNS = ["Product", "Cost", "Sell", "Currency", "Profit", "Margin"]


def load_vault():
    """读选品库；文件不存在/损坏/缺列/为空时返回空表，页面不崩。"""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=VAULT_COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE)
    except Exception:
        return pd.DataFrame(columns=VAULT_COLUMNS)
    if df.empty:
        return pd.DataFrame(columns=VAULT_COLUMNS)
    for col in VAULT_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    for col in ("Cost", "Sell", "Profit", "Margin"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[VAULT_COLUMNS]


def save_row(row):
    """整表重写（避免旧表头导致列错位），失败时提示而不是崩溃。"""
    merged = pd.concat([load_vault(), pd.DataFrame([row])], ignore_index=True)
    try:
        merged.to_csv(DATA_FILE, index=False)
    except Exception as exc:
        st.error(f"保存失败：{exc}")


def show_df(df, height=400):
    """兼容新旧 Streamlit 的宽度参数。"""
    try:
        st.dataframe(df, width="stretch", height=height)
    except TypeError:
        st.dataframe(df, use_container_width=True, height=height)

# ================= 4. 核心模块 =================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [t["t1"], t["t2"], t["t3"], t["t4"], t["t5"], t["t6"], t["t7"], t["t8"]]
)

# 页面 1：利润与预测
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input(t["name"], "Muslim Clothes")
        c_cost = st.number_input(t["cost"], min_value=0.0, value=25.0, step=1.0)
    with col2:
        s_sell = st.number_input(t["sell"], min_value=0.0, value=72.0, step=1.0)
        s_curr = st.selectbox("Sell Currency", currency_list, index=0)
    ship = st.number_input(t["ship"], min_value=0.0, value=8.0, step=0.5)
    fee = st.number_input(t["fee"], min_value=0.0, max_value=100.0, value=10.0, step=0.5)

    real_profit = s_sell - c_cost - ship - (s_sell * (fee / 100))
    margin = (real_profit / s_sell) * 100 if s_sell > 0 else 0.0
    _cls = "good" if real_profit >= 0 else "bad"
    st.markdown(
        '<div class="sec"><i class="bullet"></i>'
        f'<span class="t">{escape(t["calc"])}</span><span class="s">Live margin</span></div>'
        '<div class="kpi-row">'
        f'<div class="kpi"><div class="k">{escape(t["sell"])}</div>'
        f'<div class="v">{s_sell:,.2f} <small>{s_curr}</small></div><div class="d">Sell price</div></div>'
        f'<div class="kpi"><div class="k">{escape(t["cost"])}</div>'
        f'<div class="v">{c_cost:,.2f}</div><div class="d">Unit cost</div></div>'
        f'<div class="kpi"><div class="k">{escape(t["fee"])}</div>'
        f'<div class="v">{fee:.1f}%</div><div class="d">{s_sell * fee / 100:,.2f} {s_curr}</div></div>'
        '<div class="kpi"><div class="k">NET / UNIT</div>'
        f'<div class="v {_cls}">{real_profit:,.2f} <small>{s_curr}</small></div>'
        f'<div class="d">Margin {margin:.1f}%</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )
    if st.button(t["save"]):
        save_row({
            "Product": (p_name or "未命名商品").strip(),
            "Cost": round(c_cost, 2),
            "Sell": round(s_sell, 2),
            "Currency": s_curr,
            "Profit": round(real_profit, 2),
            "Margin": round(margin, 1),
        })
        st.balloons()
        st.success("Saved!")

# 页面 2：选品库
with tab2:
    df = load_vault()
    if df.empty:
        st.info("库为空。")
    else:
        df = df.sort_values(by="Profit", ascending=False, na_position="last")
        show_df(df, 400)

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
        if not rates:
            st.warning("汇率服务暂不可用，请稍后重试。")
        else:
            amt = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)
            f_curr = st.selectbox("From", currency_list, index=1)
            t_curr = st.selectbox("To", currency_list, index=0)
            r_from, r_to = rates.get(f_curr), rates.get(t_curr)
            if not r_from or not r_to:
                st.warning("该币种汇率暂不可用。")
            else:
                st.metric(label="Result", value=f"{(amt / r_from) * r_to:.2f} {t_curr}")

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


# ================= 5.1 商业逆向工程：提示词 / JSON 解析 / 数据看板 =================
REVERSE_PROMPT = """你是资深采购与竞品分析师，长期在跨境电商与制造业一线做成本拆解。
下面是一份供应商报价单 PDF 的文字内容，请基于它做「商业逆向工程」分析。
严格只输出一个 JSON 对象（不要 Markdown 代码块、不要解释、不要前后缀），结构如下：
{
  "product": "产品名称",
  "currency": "推测的结算币种，例如 CNY / USD",
  "cost": {
    "breakdown": [
      {"name": "材料", "pct": 45, "note": "判断依据（20字内）"},
      {"name": "人工", "pct": 20, "note": "依据"},
      {"name": "包装", "pct": 10, "note": "依据"},
      {"name": "其他", "pct": 25, "note": "模具/物流/损耗/税费等"}
    ],
    "margin_pct": 55,
    "cost_range": "12-16",
    "retail_ref": "39-49",
    "verdict": "一句话结论（30字内）"
  },
  "competitiveness": {
    "selling_points": [{"title": "核心卖点", "detail": "为什么算技术壁垒/具体依据"}],
    "risks": [{"title": "风险或虚标点", "detail": "哪个参数可能虚标、怎么验证"}]
  },
  "supply_chain": {
    "regions": ["产业带1", "产业带2"],
    "factory_types": [{"type": "工厂类型", "why": "为什么找它 + 筛选标准"}],
    "checklist": ["验厂/验货要点1", "要点2"]
  }
}
硬性要求：
1. breakdown 的 pct 为 0-100 的数字，四项合计约 100；margin_pct 为 0-100 的整数（毛利率估算）。
2. selling_points 2-4 条、risks 2-4 条，必须具体可验证（例如「标称 IPX7 但结构无防水圈，疑似虚标」）。
3. factory_types 2-4 条，写清「找什么类型的工厂 + 判断标准」；regions 给 2-4 个国内产业带。
4. checklist 3-6 条，偏实操（打样、验厂、验货、认证）。
5. 信息不足时给合理推测并标注「推测」，禁止编造具体供应商名称与联系方式。"""


def build_reverse_prompt(text):
    return REVERSE_PROMPT + "\n\n<PDF文本>\n" + text + "\n</PDF文本>"


def parse_reverse_json(raw):
    """从模型返回里抠出 JSON 对象；解析失败返回 None。"""
    if not isinstance(raw, str):
        return None
    s = raw.strip()
    if s.startswith("```"):
        s = s.strip("`").strip()
        if s[:4].lower() == "json":
            s = s[4:]
    start, end = s.find("{"), s.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        data = json.loads(s[start:end + 1])
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _br_num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _br_list(v):
    return v if isinstance(v, list) else []


def _br_txt(v, default=""):
    if v is None or isinstance(v, (dict, list)):
        return default
    s = str(v).strip()
    return escape(s) if s else default


def _br_palette(is_dark, bg, text, card, border):
    if is_dark:
        return {
            "bg": bg, "text": text, "card": "rgba(15,23,42,.55)", "card2": "rgba(15,23,42,.35)",
            "border": border, "muted": "rgba(148,163,184,.85)", "track": "rgba(148,163,184,.18)",
            "accent": "#D4AF37", "accent2": "#F0D98C", "accent_soft": "rgba(212,175,55,.13)",
            "good": "#4FB28C", "good_soft": "rgba(79,178,140,.14)",
            "warn": "#E0A64B", "warn_soft": "rgba(224,166,75,.14)",
            "bad": "#E06C5A", "bad_soft": "rgba(224,108,90,.14)",
        }
    return {
        "bg": bg, "text": text, "card": "rgba(255,255,255,.92)", "card2": "rgba(248,250,252,.95)",
        "border": border, "muted": "rgba(71,85,105,.8)", "track": "rgba(15,23,42,.10)",
        "accent": "#A97F1E", "accent2": "#8C6B1F", "accent_soft": "rgba(176,137,43,.12)",
        "good": "#2F8F6B", "good_soft": "rgba(47,143,107,.12)",
        "warn": "#B45309", "warn_soft": "rgba(180,83,9,.12)",
        "bad": "#DC2626", "bad_soft": "rgba(220,38,38,.10)",
    }


BR_CSS = """
<style>
.br-wrap{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;margin-top:6px}
.br-hero{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;padding:14px 18px;border-radius:14px;border:1px solid __BORDER__;background:linear-gradient(120deg,__CARD__,transparent 70%);margin:0 0 14px}
.br-hero .k{font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:__MUTED__;font-weight:700}
.br-hero .v{font-size:22px;font-weight:800;color:__TEXT__;letter-spacing:-.01em;margin-top:3px;line-height:1.2}
.br-hero .tag{flex:none;font-size:11px;padding:3px 10px;border-radius:999px;border:1px solid __BORDER__;color:__MUTED__;background:__CARD2__;font-variant-numeric:tabular-nums}
.br-grid{display:grid;grid-template-columns:1.05fr .95fr 1.05fr;gap:14px;align-items:start}
@media(max-width:1200px){.br-grid{grid-template-columns:1fr}}
.br-card{position:relative;padding:16px;border-radius:16px;border:1px solid __BORDER__;background:__CARD__;overflow:hidden;box-shadow:0 0 26px __ACCENT_SOFT__}
.br-card:before{content:"";position:absolute;left:0;top:0;width:100%;height:2px;background:linear-gradient(90deg,__ACCENT__,__ACCENT2__,transparent)}
.br-card h4{margin:0;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:__MUTED__;font-weight:800}
.br-card .sub{font-size:11px;color:__MUTED__;margin:4px 0 14px}
.br-sec{display:flex;align-items:center;gap:8px;margin:14px 0 8px}
.br-sec i{width:6px;height:6px;border-radius:50%;background:__ACCENT__;box-shadow:0 0 0 3px __ACCENT_SOFT__}
.br-sec span{font-size:12px;font-weight:700;color:__TEXT__}
.br-bar{margin:0 0 12px}
.br-bar .top{display:flex;justify-content:space-between;font-size:12px;color:__TEXT__;margin-bottom:5px}
.br-bar .top em{font-style:normal;font-weight:800;font-variant-numeric:tabular-nums}
.br-track{height:7px;border-radius:99px;background:__TRACK__;overflow:hidden}
.br-track i{display:block;height:100%;border-radius:99px}
.br-note{display:block;margin-top:4px;font-size:11px;color:__MUTED__;line-height:1.45}
.br-gauge{--v:0;width:122px;height:122px;border-radius:50%;margin:4px auto 12px;background:conic-gradient(var(--c) calc(var(--v)*1%),__TRACK__ 0);display:flex;align-items:center;justify-content:center;position:relative}
.br-gauge:after{content:"";position:absolute;inset:9px;border-radius:50%;background:__CARD__;border:1px solid __BORDER__}
.br-gauge-in{position:relative;z-index:1;text-align:center}
.br-gauge-in b{display:block;font-size:25px;font-weight:800;color:__TEXT__;font-variant-numeric:tabular-nums;line-height:1.1}
.br-gauge-in small{display:block;font-size:10px;color:__MUTED__;letter-spacing:.08em;margin-top:2px}
.br-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}
.br-meta div{padding:8px 9px;border-radius:10px;border:1px solid __BORDER__;background:__CARD2__}
.br-meta .k{font-size:10px;color:__MUTED__;letter-spacing:.06em}
.br-meta .v{font-size:13px;font-weight:700;color:__TEXT__;margin-top:2px;font-variant-numeric:tabular-nums}
.br-verdict{margin-top:10px;padding:9px 11px;border-radius:10px;border-left:2px solid __ACCENT__;background:__ACCENT_SOFT__;font-size:11.5px;color:__TEXT__;line-height:1.55}
.br-item{display:flex;gap:9px;padding:9px 10px;border-radius:11px;border:1px solid __BORDER__;background:__CARD2__;margin:7px 0}
.br-item .ico{flex:none;width:18px;height:18px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;margin-top:1px}
.br-item.good .ico{background:__GOOD_SOFT__;color:__GOOD__}
.br-item.bad .ico{background:__WARN_SOFT__;color:__WARN__}
.br-item .t{font-size:12px;font-weight:700;color:__TEXT__;line-height:1.35}
.br-item .d{font-size:11px;color:__MUTED__;line-height:1.5;margin-top:3px}
.br-empty{font-size:11px;color:__MUTED__;padding:6px 0}
.br-chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.br-chip{font-size:11px;padding:3px 9px;border-radius:999px;background:__ACCENT_SOFT__;color:__ACCENT_TX__;border:1px solid __BORDER__;font-weight:600}
.br-fitem{padding:9px 10px;border-radius:11px;border:1px dashed __BORDER__;margin:7px 0;background:__CARD2__}
.br-fitem .t{font-size:12px;font-weight:700;color:__TEXT__}
.br-fitem .d{font-size:11px;color:__MUTED__;margin-top:3px;line-height:1.5}
.br-check{margin:0;padding:0;list-style:none}
.br-check li{position:relative;padding-left:17px;font-size:11.5px;color:__TEXT__;line-height:1.6;margin:5px 0}
.br-check li:before{content:"›";position:absolute;left:4px;top:0;color:__ACCENT__;font-weight:800}
.br-gap{height:10px}
</style>
"""


def render_reverse_dashboard(data, p):
    """把 AI 的 JSON 渲染成科技感数据看板（返回 HTML 字符串）。"""
    cost = data.get("cost") if isinstance(data.get("cost"), dict) else {}
    comp = data.get("competitiveness") if isinstance(data.get("competitiveness"), dict) else {}
    sc = data.get("supply_chain") if isinstance(data.get("supply_chain"), dict) else {}

    css = (BR_CSS.replace("__BORDER__", p["border"]).replace("__CARD__", p["card"])
           .replace("__CARD2__", p["card2"]).replace("__TEXT__", p["text"])
           .replace("__MUTED__", p["muted"]).replace("__TRACK__", p["track"])
           .replace("__ACCENT_TX__", p["accent"]).replace("__ACCENT2__", p["accent2"])
           .replace("__ACCENT__", p["accent"]).replace("__ACCENT_SOFT__", p["accent_soft"])
           .replace("__GOOD__", p["good"]).replace("__GOOD_SOFT__", p["good_soft"])
           .replace("__WARN__", p["warn"]).replace("__WARN_SOFT__", p["warn_soft"]))

    product = _br_txt(data.get("product"), "未命名产品")
    currency = _br_txt(data.get("currency"), "—")
    hero = (
        f'<div class="br-hero"><div><div class="k">Business Reverse Engineering</div>'
        f'<div class="v">{product}</div></div><div class="tag">{currency}</div></div>'
    )

    # ---- 成本拆解 ----
    colors = [p["accent"], p["accent2"], p["good"], p["warn"], p["bad"]]
    bars = ""
    for idx, item in enumerate(_br_list(cost.get("breakdown"))[:5]):
        if not isinstance(item, dict):
            continue
        name = _br_txt(item.get("name"), "其他")
        pct = max(0.0, min(100.0, _br_num(item.get("pct"))))
        note = _br_txt(item.get("note"))
        note_html = f'<span class="br-note">{note}</span>' if note else ""
        bars += (
            f'<div class="br-bar"><div class="top"><span>{name}</span>'
            f"<em>{pct:.0f}%</em></div>"
            f'<div class="br-track"><i style="width:{pct:.1f}%;background:{colors[idx % len(colors)]}"></i></div>'
            f"{note_html}</div>"
        )
    if not bars:
        bars = '<div class="br-empty">暂无可拆解的成本结构</div>'

    margin = max(0.0, min(100.0, _br_num(cost.get("margin_pct"))))
    gcol = p["good"] if margin >= 50 else (p["warn"] if margin >= 30 else p["bad"])
    gauge = (
        f'<div class="br-gauge" style="--v:{margin:.0f};--c:{gcol}">'
        f'<div class="br-gauge-in"><b>{margin:.0f}%</b><small>毛利率估算</small></div></div>'
    )
    cost_range = _br_txt(cost.get("cost_range"), "—")
    retail_ref = _br_txt(cost.get("retail_ref"), "—")
    verdict = _br_txt(cost.get("verdict"))
    verdict_html = f'<div class="br-verdict">{verdict}</div>' if verdict else ""

    cost_card = (
        '<div class="br-card"><h4>01 · Cost Structure</h4>'
        '<div class="sub">成本拆解与毛利估算</div>'
        f"{bars}"
        '<div class="br-sec"><i></i><span>毛利空间</span></div>'
        f"{gauge}"
        '<div class="br-meta">'
        f'<div><div class="k">估算出厂成本</div><div class="v">{cost_range} {currency}</div></div>'
        f'<div><div class="k">参考零售价</div><div class="v">{retail_ref} {currency}</div></div>'
        "</div>"
        f"{verdict_html}</div>"
    )

    # ---- 竞争力剖析 ----
    def _items(rows, kind):
        out = ""
        for row in _br_list(rows)[:4]:
            if isinstance(row, dict):
                title = _br_txt(row.get("title")) or _br_txt(row.get("name"))
                detail = _br_txt(row.get("detail")) or _br_txt(row.get("note"))
            else:
                title, detail = _br_txt(row), ""
            if not title:
                continue
            icon = "✓" if kind == "good" else "!"
            out += (
                f'<div class="br-item {kind}"><div class="ico">{icon}</div><div>'
                f'<div class="t">{title}</div>'
                + (f'<div class="d">{detail}</div>' if detail else "")
                + "</div></div>"
            )
        return out

    good_items = _items(comp.get("selling_points"), "good") or '<div class="br-empty">未识别到明显技术壁垒</div>'
    bad_items = _items(comp.get("risks"), "bad") or '<div class="br-empty">未发现明显虚标或缺陷</div>'

    comp_card = (
        '<div class="br-card"><h4>02 · Competitiveness</h4>'
        '<div class="sub">核心卖点与技术壁垒 / 虚标与缺陷</div>'
        '<div class="br-sec"><i></i><span>核心卖点（技术壁垒）</span></div>'
        f"{good_items}"
        '<div class="br-sec"><i></i><span>参数虚标 / 潜在缺陷</span></div>'
        f"{bad_items}</div>"
    )

    # ---- 供应链建议 ----
    chips = "".join(
        f'<span class="br-chip">{_br_txt(r)}</span>'
        for r in _br_list(sc.get("regions"))[:6] if _br_txt(r)
    )
    chips_html = f'<div class="br-chips">{chips}</div>' if chips else ""

    factories = ""
    for row in _br_list(sc.get("factory_types"))[:4]:
        if isinstance(row, dict):
            ftype = _br_txt(row.get("type"))
            why = _br_txt(row.get("why")) or _br_txt(row.get("detail"))
        else:
            ftype, why = _br_txt(row), ""
        if not ftype:
            continue
        factories += (
            f'<div class="br-fitem"><div class="t">{ftype}</div>'
            + (f'<div class="d">{why}</div>' if why else "")
            + "</div>"
        )
    if not factories:
        factories = '<div class="br-empty">暂无工厂类型建议</div>'

    checklist = "".join(
        f"<li>{_br_txt(c)}</li>" for c in _br_list(sc.get("checklist"))[:6] if _br_txt(c)
    )
    checklist_html = f'<ul class="br-check">{checklist}</ul>' if checklist else ""

    sc_card = (
        '<div class="br-card"><h4>03 · Supply Chain</h4>'
        '<div class="sub">国内平替代工：产业带与工厂筛选</div>'
        f"{chips_html}"
        f"{factories}"
        + ('<div class="br-sec"><i></i><span>验厂 / 验货清单</span></div>' + checklist_html if checklist_html else "")
        + "</div>"
    )

    return (
        f"{css}<div class=\"br-wrap\">{hero}"
        f'<div class="br-grid">{cost_card}{comp_card}{sc_card}</div></div>'
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
                st.session_state.pop("reverse_data", None)
                st.session_state.pop("reverse_raw", None)
                st.error(err)
            else:
                st.session_state["pdf_text"] = text
                st.session_state["pdf_text_key"] = file_key
                st.session_state["pdf_pages"] = pages
                st.session_state.pop("pdf_result", None)  # 新文件清掉旧结果
                st.session_state.pop("reverse_data", None)
                st.session_state.pop("reverse_raw", None)

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

    # ===== 5.2 商业逆向工程看板（始终可见，需先上传 PDF） =====
    st.markdown('<div class="br-gap"></div>', unsafe_allow_html=True)
    st.markdown("#### 🧬 商业逆向工程")
    st.caption("成本拆解 · 竞争力剖析 · 供应链建议｜基于同一份 PDF 的深度分析")
    _rev_text = st.session_state.get("pdf_text")
    if not _rev_text:
        st.info("先上传报价单 PDF，解析成功后即可生成逆向分析。")
    else:
        if st.button("🚀 生成逆向分析", key="reverse_btn"):
            with st.spinner("AI 正在做成本拆解与竞品分析..."):
                _raw = call_groq(build_reverse_prompt(_rev_text), 0.3)
            if isinstance(_raw, str) and _raw.startswith("❌"):
                st.error(_raw)
            else:
                _data = parse_reverse_json(_raw)
                if _data:
                    st.session_state["reverse_data"] = _data
                    st.session_state.pop("reverse_raw", None)
                else:
                    st.session_state["reverse_raw"] = _raw
                    st.session_state.pop("reverse_data", None)

        if st.session_state.get("reverse_data"):
            _palette = _br_palette(is_dark, bg_color, text_color, card_bg, border_color)
            st.markdown(render_reverse_dashboard(st.session_state["reverse_data"], _palette), unsafe_allow_html=True)
            st.download_button(
                "⬇ 导出分析 JSON",
                data=json.dumps(st.session_state["reverse_data"], ensure_ascii=False, indent=2),
                file_name="reverse_engineering.json",
                mime="application/json",
                key="dl_reverse",
            )
        elif st.session_state.get("reverse_raw"):
            st.warning("AI 返回的不是标准 JSON，先展示原始内容：")
            st.markdown(st.session_state["reverse_raw"])


# ================= 6. 供应商比价：多份报价单横向对比 =================
COMPARE_EXTRA = """
另外，请在同一个 JSON 里再补充这些字段：
  "supplier": "供应商名称（看不清就写文件名）",
  "unit_price": "单价，纯数字不带币种，例如 12.50",
  "moq": "起订量，例如 500 pcs",
  "total_price": "总价（带币种）",
  "score": 78,
  "verdict": "一句话结论：这家值不值得谈（30 字内）"
硬性要求：score 是 0-100 的整数，综合价格竞争力、成本结构、资质与风险打分；不要编造供应商联系方式。
"""

COMPARE_HISTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compare_history.json")


def build_compare_prompt(text):
    return build_reverse_prompt(text) + COMPARE_EXTRA


def _load_compare_history():
    try:
        with open(COMPARE_HISTORY, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_compare_history(records):
    ok = [r for r in records if not r.get("error")]
    if not ok:
        return
    best = _best_record(ok) or {}
    entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "product": ok[0].get("product", "—"),
        "count": len(ok),
        "best": best.get("supplier") or best.get("file") or "—",
        "suppliers": [
            {
                "supplier": r.get("supplier") or r.get("file"),
                "price": r.get("unit_price"),
                "moq": r.get("moq"),
                "score": r.get("score"),
                "margin": (r.get("cost") or {}).get("margin_pct"),
            }
            for r in ok
        ],
    }
    hist = _load_compare_history()
    hist.append(entry)
    try:
        with open(COMPARE_HISTORY, "w", encoding="utf-8") as fh:
            json.dump(hist[-200:], fh, ensure_ascii=False, indent=1)
    except Exception:
        pass


def _best_record(records):
    best, best_score = None, -1.0
    for r in records:
        sc = _br_num(r.get("score"), -1.0)
        if sc > best_score:
            best, best_score = r, sc
    return best


def _price_num(value):
    if value is None:
        return None
    s = str(value).replace(",", "").replace("¥", "").replace("$", "").replace(" ", "")
    try:
        return float(s)
    except Exception:
        return None


def render_compare_table(records, p):
    """横向对比表：价格 / 起订量 / 成本 / 毛利 / 评分。"""
    rows = ""
    prices = [_price_num(r.get("unit_price")) for r in records]
    valid_prices = [x for x in prices if x is not None]
    cheapest = min(valid_prices) if valid_prices else None
    best = _best_record(records)
    best_id = id(best) if best is not None else None

    for idx, r in enumerate(records, 1):
        name = _br_txt(r.get("supplier")) or _br_txt(r.get("file"))
        price = _price_num(r.get("unit_price"))
        cur = _br_txt(r.get("currency"))
        price_html = f"{price:,.2f} <small>{cur}</small>" if price is not None else "—"
        price_flag = (
            '<span class="cmp-tag good">最低价</span>' if price is not None and cheapest is not None and abs(price - cheapest) < 1e-9 else ""
        )
        sc = _br_num(r.get("score"))
        sc_cls = "good" if sc >= 75 else ("mid" if sc >= 55 else "bad")
        is_best = id(r) == best_id
        rows += (
            f'<tr class="{"best" if is_best else ""}">'
            f'<td class="cmp-idx">{idx:02d}</td>'
            f'<td><div class="cmp-name">{name}'
            + ('<span class="cmp-tag gold">推荐</span>' if is_best else "")
            + f'</div><div class="cmp-sub">{_br_txt(r.get("file"))}</div></td>'
            f'<td class="cmp-num">{price_html}{price_flag}</td>'
            f'<td>{_br_txt(r.get("moq")) or "—"}</td>'
            f'<td>{_br_txt((r.get("cost") or {}).get("cost_range"), "—")} <small>{cur}</small></td>'
            f'<td class="cmp-num">{_br_num((r.get("cost") or {}).get("margin_pct")):.0f}%</td>'
            f'<td class="cmp-num"><span class="cmp-score {sc_cls}">{sc:.0f}</span></td>'
            f'<td class="cmp-verdict">{_br_txt(r.get("verdict")) or "—"}</td>'
            "</tr>"
        )

    css = f"""
<style>
.cmp-wrap{{margin:16px 0 6px}}
.cmp-head{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:10px}}
.cmp-head .t{{font-size:15px;font-weight:800;color:{p['text']}}}
.cmp-head .s{{font-size:11px;color:{p['muted']}}}
.cmp-table{{width:100%;border-collapse:separate;border-spacing:0;font-size:12.5px;border-radius:14px;overflow:hidden;
 border:1px solid {p['border']};background:{p['card']}}}
.cmp-table th{{text-align:left;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:{p['muted']};
 padding:11px 12px;border-bottom:1px solid {p['border']};font-weight:700;white-space:nowrap}}
.cmp-table td{{padding:11px 12px;border-bottom:1px solid {p['border']};color:{p['text']};vertical-align:middle}}
.cmp-table tr:last-child td{{border-bottom:none}}
.cmp-table tr.best td{{background:rgba(212,175,55,.07)}}
.cmp-table tr:hover td{{background:rgba(212,175,55,.05)}}
.cmp-idx{{color:{p['muted']};font-variant-numeric:tabular-nums}}
.cmp-name{{font-weight:700;display:flex;align-items:center;gap:7px}}
.cmp-sub{{font-size:10.5px;color:{p['muted']};margin-top:2px}}
.cmp-num{{font-variant-numeric:tabular-nums;text-align:right;font-weight:700;white-space:nowrap}}
.cmp-num small,.cmp-table small{{font-size:10px;opacity:.7;font-weight:600}}
.cmp-verdict{{color:{p['muted']};font-size:11.5px;max-width:260px}}
.cmp-tag{{font-size:9.5px;padding:2px 7px;border-radius:999px;font-weight:800;letter-spacing:.04em}}
.cmp-tag.gold{{background:rgba(212,175,55,.16);color:{p['accent']};border:1px solid rgba(212,175,55,.35)}}
.cmp-tag.good{{background:{p['good_soft']};color:{p['good']};margin-left:6px}}
.cmp-score{{display:inline-block;min-width:42px;padding:3px 9px;border-radius:9px;font-weight:800;font-variant-numeric:tabular-nums}}
.cmp-score.good{{background:{p['good_soft']};color:{p['good']}}}
.cmp-score.mid{{background:{p['warn_soft']};color:{p['warn']}}}
.cmp-score.bad{{background:{p['bad_soft']};color:{p['bad']}}}
</style>
"""
    return (
        css
        + '<div class="cmp-wrap"><div class="cmp-head">'
        f'<span class="t">{len(records)} 家供应商横向对比</span>'
        '<span class="s">Score = 价格 · 成本 · 风险 综合评分</span></div>'
        '<table class="cmp-table"><thead><tr>'
        '<th>#</th><th>供应商</th><th class="cmp-num">单价</th><th>起订量</th>'
        '<th>成本区间</th><th class="cmp-num">毛利</th><th class="cmp-num">评分</th><th>结论</th>'
        "</tr></thead><tbody>" + rows + "</tbody></table></div>"
    )


def build_compare_report(records, is_dark):
    """生成可下载、可打印成 PDF 的单文件 HTML 报告。"""
    bg = "#0B0B0D" if is_dark else "#FBF8F1"
    fg = "#F3EEE3" if is_dark else "#1A1408"
    muted = "#9C9689" if is_dark else "#6B6355"
    card = "#141416" if is_dark else "#FFFFFF"
    border = "rgba(212,175,55,.22)" if is_dark else "rgba(140,107,31,.22)"
    gold = "#D4AF37" if is_dark else "#8C6B1F"

    rows = ""
    best = _best_record(records) or {}
    best_name = best.get("supplier") or best.get("file")
    for idx, r in enumerate(records, 1):
        name = _br_txt(r.get("supplier")) or _br_txt(r.get("file"))
        sc = _br_num(r.get("score"))
        rows += (
            f"<tr><td>{idx}</td><td><b>{name}</b><div class='sub'>{_br_txt(r.get('file'))}</div></td>"
            f"<td>{_br_txt(r.get('unit_price'))} {_br_txt(r.get('currency'))}</td>"
            f"<td>{_br_txt(r.get('moq'))}</td>"
            f"<td>{_br_txt((r.get('cost') or {}).get('cost_range'))}</td>"
            f"<td>{_br_num((r.get('cost') or {}).get('margin_pct')):.0f}%</td>"
            f"<td><b>{sc:.0f}</b></td>"
            f"<td>{_br_txt(r.get('verdict'))}</td></tr>"
        )

    details = ""
    for r in records:
        name = _br_txt(r.get("supplier")) or _br_txt(r.get("file"))
        points = "".join(f"<li>{_br_txt(x.get('title') if isinstance(x, dict) else x)}</li>" for x in _br_list((r.get("competitiveness") or {}).get("selling_points"))[:4])
        risks = "".join(f"<li>{_br_txt(x.get('title') if isinstance(x, dict) else x)}</li>" for x in _br_list((r.get("competitiveness") or {}).get("risks"))[:4])
        details += (
            f"<section><h2>{name}</h2>"
            f"<p class='v'>{_br_txt(r.get('verdict'))}</p>"
            f"<div class='cols'><div><h3>核心卖点</h3><ul>{points or '<li>—</li>'}</ul></div>"
            f"<div><h3>风险 / 虚标</h3><ul>{risks or '<li>—</li>'}</ul></div></div></section>"
        )

    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>供应商比价报告</title>
<style>
body{{margin:0;padding:40px;background:{bg};color:{fg};font:14px/1.6 -apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif}}
h1{{font-size:28px;margin:0 0 4px;letter-spacing:-.5px;color:{gold}}}
.meta{{color:{muted};font-size:12px;margin-bottom:26px}}
table{{width:100%;border-collapse:collapse;background:{card};border:1px solid {border};border-radius:12px;overflow:hidden}}
th,td{{padding:10px 12px;border-bottom:1px solid {border};text-align:left;font-size:12.5px}}
th{{color:{muted};font-size:10px;letter-spacing:.1em;text-transform:uppercase}}
tr:last-child td{{border-bottom:none}}
.sub{{color:{muted};font-size:10.5px}}
section{{margin:28px 0;padding:18px 20px;border:1px solid {border};border-radius:14px;background:{card}}}
h2{{font-size:17px;margin:0 0 6px}}
h3{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{muted};margin:14px 0 6px}}
ul{{margin:0;padding-left:18px}} li{{margin:3px 0;font-size:12.5px}}
.v{{color:{muted};margin:0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
footer{{margin-top:30px;color:{muted};font-size:11px;text-align:center}}
</style></head><body>
<h1>供应商比价报告</h1>
<div class="meta">生成时间 {datetime.now().strftime("%Y-%m-%d %H:%M")} · 共 {len(records)} 家供应商 · Global Trade Hub</div>
<table><thead><tr><th>#</th><th>供应商</th><th>单价</th><th>起订量</th><th>成本区间</th><th>毛利</th><th>评分</th><th>结论</th></tr></thead>
<tbody>{rows}</tbody></table>
{details}
<footer>本报告由 AI 依据报价单文本推测生成，成本与毛利为估算值，仅供决策参考。</footer>
</body></html>"""


# ================= 7. 供应商比价页 =================
with tab6:
    st.markdown("### 🏆 供应商比价")
    st.caption("一次上传 2-5 份报价单，AI 横向对比单价、成本结构、风险与综合评分，并给出推荐。")

    cmp_files = st.file_uploader(
        "上传报价 PDF（2-5 份）", type=["pdf"], accept_multiple_files=True, key="cmp_files"
    )
    if st.button("⚖️ 开始比价", key="cmp_btn"):
        if not cmp_files or len(cmp_files) < 2:
            st.warning("请至少上传 2 份报价单才能比价。")
        else:
            files = cmp_files[:5]
            records = []
            bar = st.progress(0.0, text="准备中…")
            for i, f in enumerate(files, 1):
                bar.progress((i - 0.5) / len(files), text=f"分析 {f.name}（{i}/{len(files)}）")
                _text, _pages, _err = extract_pdf_text(f.getvalue())
                if _err:
                    records.append({"file": f.name, "error": _err})
                    continue
                _raw = call_groq(build_compare_prompt(_text), 0.3, max_tokens=2600)
                _data = parse_reverse_json(_raw) if not (isinstance(_raw, str) and _raw.startswith("❌")) else None
                if not _data:
                    records.append({"file": f.name, "error": (_raw or "解析失败")[:160]})
                else:
                    _data["file"] = f.name
                    records.append(_data)
                bar.progress(i / len(files), text=f"完成 {i}/{len(files)}")
            bar.empty()
            st.session_state["compare_records"] = records
            _save_compare_history(records)

    _recs = st.session_state.get("compare_records") or []
    if _recs:
        _ok = [r for r in _recs if not r.get("error")]
        _bad = [r for r in _recs if r.get("error")]
        if _ok:
            _pal = _br_palette(is_dark, bg_color, text_color, card_bg, border_color)
            st.markdown(render_compare_table(_ok, _pal), unsafe_allow_html=True)
            _best = _best_record(_ok)
            if _best:
                st.success(
                    f"🏆 推荐：**{_br_txt(_best.get('supplier')) or _br_txt(_best.get('file'))}**"
                    f"（综合评分 {_br_num(_best.get('score')):.0f}）— {_br_txt(_best.get('verdict'))}"
                )
            for _r in _ok:
                with st.expander(f"📄 {_br_txt(_r.get('supplier')) or _br_txt(_r.get('file'))} · 明细", expanded=False):
                    st.markdown(render_reverse_dashboard(_r, _pal), unsafe_allow_html=True)
            st.download_button(
                "⬇ 导出比价报告（HTML，可打印成 PDF）",
                data=build_compare_report(_ok, is_dark),
                file_name="supplier_compare_report.html",
                mime="text/html",
                key="dl_compare",
            )
        for _r in _bad:
            st.warning(f"{_r.get('file')}：{_r.get('error')}")

    with st.expander("🗂 比价历史", expanded=False):
        _hist = _load_compare_history()
        if not _hist:
            st.caption("还没有历史记录，完成一次比价后会自动保存在本地。")
        else:
            for _h in _hist[-8:][::-1]:
                st.markdown(
                    f"- **{_h.get('ts', '—')}** · {_h.get('product', '—')} · "
                    f"{_h.get('count', 0)} 家 · 推荐 **{_h.get('best', '—')}**"
                )


# ================= 7. 利润沙盘 / 选品雷达（可视化增强） =================
RADAR_PROMPT = """你是跨境电商选品专家。请针对下面的品类与目标市场，给出 6-8 个具体可做的产品方向。
严格只输出一个 JSON（不要 Markdown 代码块、不要解释）：
{
  "category": "品类",
  "market": "目标市场",
  "products": [
    {"name": "产品名", "demand": 78, "competition": 45, "margin": 55,
     "price_low": 12, "price_high": 19,
     "reason": "为什么有需求（20 字内）", "risk": "主要风险（20 字内）", "score": 74}
  ],
  "summary": "一句话总结（30 字内）"
}
要求：
1. demand / competition / margin / score 均为 0-100 的整数。
2. price_low / price_high 用纯数字（统一按 USD 估算）。
3. 产品要具体可落地（不要写「家居用品」这种大类），要能对应到具体工厂与平台。
4. reason 与 risk 必须具体，禁止编造品牌名或具体供应商。
"""


def build_radar_prompt(category, market, budget):
    return (
        RADAR_PROMPT
        + f"\n品类：{category}\n目标市场：{market}\n目标客单价：{budget} USD 左右\n"
    )


def _quadrant_label(demand, competition):
    if demand >= 55 and competition < 55:
        return "蓝海机会", "#4FB28C"
    if demand >= 55 and competition >= 55:
        return "红海竞争", "#E0A64B"
    if demand < 55 and competition < 55:
        return "小众待教育", "#8FB3D9"
    return "不建议", "#E06C5A"


def _svg_line_chart(points, p, markers, w=780, h=330, pad=54):
    """价格-利润曲线（纯 SVG，跟随主题）。markers: [(x, label, color)]"""
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    xmin, xmax = min(xs), max(xs)
    if xmax == xmin:
        xmax = xmin + 1
    ymin = min(min(ys), 0.0)
    ymax = max(max(ys), 0.0)
    if ymax == ymin:
        ymax = ymin + 1

    def sx(x):
        return pad + (x - xmin) / (xmax - xmin) * (w - pad * 2)

    def sy(y):
        return h - pad - (y - ymin) / (ymax - ymin) * (h - pad * 2)

    line = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in points)
    zero = sy(max(ymin, min(0.0, ymax)))
    area = f"{sx(xs[0]):.1f},{zero:.1f} " + line + f" {sx(xs[-1]):.1f},{zero:.1f}"

    grid = ""
    for i in range(5):
        y = ymin + (ymax - ymin) * i / 4
        yy = sy(y)
        grid += f'<line x1="{pad}" y1="{yy:.1f}" x2="{w - pad}" y2="{yy:.1f}" stroke="{p["border"]}" stroke-width="1"/>'
        grid += f'<text x="{pad - 8}" y="{yy + 4:.1f}" text-anchor="end" font-size="10" fill="{p["muted"]}">{y:,.0f}</text>'

    mk = ""
    for mx, label, color in markers:
        if mx is None or not (xmin <= mx <= xmax):
            continue
        xx = sx(mx)
        mk += (
            f'<line x1="{xx:.1f}" y1="{pad}" x2="{xx:.1f}" y2="{h - pad}" stroke="{color}" '
            f'stroke-width="1.2" stroke-dasharray="4 4" opacity=".85"/>'
            f'<text x="{xx:.1f}" y="{pad - 8}" text-anchor="middle" font-size="10" fill="{color}">{label}</text>'
        )

    return f"""<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" role="img">
<defs><linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{p['accent']}" stop-opacity=".28"/>
<stop offset="100%" stop-color="{p['accent']}" stop-opacity="0"/>
</linearGradient></defs>
{grid}{mk}
<line x1="{pad}" y1="{zero:.1f}" x2="{w - pad}" y2="{zero:.1f}" stroke="{p['muted']}" stroke-width="1" opacity=".5"/>
<polygon points="{area}" fill="url(#gArea)"/>
<polyline points="{line}" fill="none" stroke="{p['accent']}" stroke-width="2.4" stroke-linejoin="round"/>
</svg>"""


def _svg_bubble_chart(items, p, w=780, h=430, pad=56):
    """需求(x=竞争, y=需求)气泡矩阵，气泡大小 = 毛利。"""
    body = ""
    # 象限底色
    mid = (pad + (w - pad)) / 2
    midy = (pad + (h - pad)) / 2
    body += (
        f'<rect x="{pad}" y="{pad}" width="{mid - pad}" height="{midy - pad}" fill="{p["good"]}" opacity=".05"/>'
        f'<rect x="{mid}" y="{pad}" width="{w - pad - mid}" height="{midy - pad}" fill="{p["warn"]}" opacity=".05"/>'
        f'<rect x="{pad}" y="{midy}" width="{mid - pad}" height="{h - pad - midy}" fill="{p["muted"]}" opacity=".05"/>'
        f'<rect x="{mid}" y="{midy}" width="{w - pad - mid}" height="{h - pad - midy}" fill="{p["bad"]}" opacity=".05"/>'
    )
    labels = [("低竞争 · 高需求", pad + 10, pad + 20), ("高竞争 · 高需求", mid + 10, pad + 20),
              ("低竞争 · 低需求", pad + 10, h - pad - 8), ("高竞争 · 低需求", mid + 10, h - pad - 8)]
    for text, x, y in labels:
        body += f'<text x="{x}" y="{y}" font-size="10" fill="{p["muted"]}" opacity=".8">{text}</text>'

    body += (
        f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="{p["border"]}"/>'
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="{p["border"]}"/>'
        f'<text x="{w / 2}" y="{h - 14}" text-anchor="middle" font-size="10.5" fill="{p["muted"]}">竞争强度 →</text>'
        f'<text x="16" y="{h / 2}" text-anchor="middle" font-size="10.5" fill="{p["muted"]}" transform="rotate(-90 16 {h / 2})">需求 →</text>'
    )

    for it in items:
        comp = max(0.0, min(100.0, _br_num(it.get("competition"))))
        dem = max(0.0, min(100.0, _br_num(it.get("demand"))))
        mar = max(0.0, min(100.0, _br_num(it.get("margin"))))
        x = pad + comp / 100 * (w - pad * 2)
        y = h - pad - dem / 100 * (h - pad * 2)
        r = 11 + mar / 100 * 20
        _, color = _quadrant_label(dem, comp)
        name = _br_txt(it.get("name"))[:14]
        body += (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}" opacity=".22"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="1.6"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>'
            f'<text x="{x:.1f}" y="{y - r - 5:.1f}" text-anchor="middle" font-size="10.5" fill="{p["text"]}">{name}</text>'
        )
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" role="img">{body}</svg>'


# ================= 8. 利润沙盘 =================
with tab7:
    st.markdown("### 💰 利润沙盘")
    st.caption("拖动价格与参数，实时看「预估月利润」曲线 —— 曲线最高点就是最优定价。")

    c1, c2, c3, c4 = st.columns(4)
    sb_cost = c1.number_input("进价成本", min_value=0.0, value=25.0, step=1.0, key="sb_cost")
    sb_ship = c2.number_input("运费 / 件", min_value=0.0, value=8.0, step=0.5, key="sb_ship")
    sb_fee = c3.number_input("平台抽成 %", min_value=0.0, max_value=100.0, value=10.0, step=0.5, key="sb_fee")
    sb_units = c4.number_input("参考月销量（件）", min_value=1, value=300, step=50, key="sb_units")

    c5, c6, c7 = st.columns([1, 1, 1.5])
    sb_price = c5.number_input("当前售价", min_value=0.0, value=72.0, step=1.0, key="sb_price")
    sb_cur = c6.selectbox("币种", currency_list, index=0, key="sb_cur")
    sb_elast = c7.slider("价格敏感度（越高 = 涨价掉量越快）", 0.6, 3.0, 1.4, 0.1, key="sb_elast")

    _base = sb_cost + sb_ship
    _ref = max(sb_price, 1.0)

    def _demand(price):
        return sb_units * (_ref / max(price, 0.01)) ** sb_elast

    def _total(price):
        return (price * (1 - sb_fee / 100) - _base) * _demand(price)

    _lo = max(1.0, _base * 0.8)
    _hi = max(_ref * 2.2, _base * 3.0, _lo + 1)
    _pts = []
    for _i in range(61):
        _bp = _lo + (_hi - _lo) * _i / 60
        _pts.append((_bp, _total(_bp)))
    _best_p, _best_total = max(_pts, key=lambda _t: _t[1])
    _be = _base / (1 - sb_fee / 100) if sb_fee < 100 else None
    _cur_profit = sb_price * (1 - sb_fee / 100) - _base
    _cur_total = _total(sb_price)
    _cur_margin = (_cur_profit / sb_price * 100) if sb_price > 0 else 0.0
    _pal = _br_palette(is_dark, bg_color, text_color, card_bg, border_color)

    st.markdown(
        '<div class="sec"><i class="bullet"></i><span class="t">售价 → 预估月利润</span>'
        '<span class="s">假设销量随价格按弹性衰减</span></div>',
        unsafe_allow_html=True,
    )
    _chart = _svg_line_chart(
        _pts, _pal,
        [
            (_be, "保本价", _pal["warn"]),
            (_best_p, "最优价", _pal["good"]),
            (sb_price, "当前价", _pal["accent"]),
        ],
    )
    st.markdown(f'<div style="padding:8px 4px 0">{_chart}</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="kpi-row">'
        f'<div class="kpi"><div class="k">当前月利润</div>'
        f'<div class="v {"good" if _cur_total >= 0 else "bad"}">{_cur_total:,.0f} <small>{sb_cur}</small></div>'
        f'<div class="d">单件 {_cur_profit:,.2f} × 约 {_demand(sb_price):,.0f} 件</div></div>'
        f'<div class="kpi"><div class="k">保本价</div>'
        f'<div class="v">{(f"{_be:,.2f}" if _be else "—")}</div>'
        '<div class="d">低于此价每件都亏</div></div>'
        f'<div class="kpi"><div class="k">最优价</div>'
        f'<div class="v">{_best_p:,.2f}</div>'
        f'<div class="d">月利润最高 {_best_total:,.0f}</div></div>'
        f'<div class="kpi"><div class="k">当前毛利率</div>'
        f'<div class="v {"good" if _cur_margin >= 0 else "bad"}">{_cur_margin:.1f}%</div>'
        f'<div class="d">抽成 {sb_fee:.1f}%</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("🔬 抽成敏感度（抽成每 +5%，利润怎么变）", expanded=False):
        _rows = ""
        for _f in range(0, 41, 5):
            _pf = sb_price * (1 - _f / 100) - _base
            _pt = _pf * _demand(sb_price)
            _cls = "good" if _pf >= 0 else "bad"
            _rows += (
                f'<tr><td>{_f}%</td><td class="{_cls}">{_pf:,.2f}</td>'
                f'<td class="{_cls}">{_pt:,.0f}</td>'
                f'<td>{"✅ 可做" if _pf >= 0 else "❌ 亏本"}</td></tr>'
            )
        st.markdown(
            '<table style="width:100%;border-collapse:collapse;font-size:13px">'
            '<thead><tr><th style="text-align:left;opacity:.7">平台抽成</th>'
            '<th style="text-align:left;opacity:.7">单件利润</th>'
            '<th style="text-align:left;opacity:.7">月利润</th>'
            '<th style="text-align:left;opacity:.7">结论</th></tr></thead>'
            f"<tbody>{_rows}</tbody></table>",
            unsafe_allow_html=True,
        )

with tab8:
    st.markdown("### 🔍 选品雷达")
    st.caption("输入品类与市场，AI 生成候选产品，并用「需求 × 竞争」矩阵帮你找蓝海。")

    r1, r2, r3 = st.columns([2, 1.3, 1])
    radar_cat = r1.text_input("品类 / 关键词", "宠物用品", key="radar_cat")
    radar_market = r2.selectbox(
        "目标市场",
        ["Malaysia", "Indonesia", "Thailand", "Vietnam", "USA", "Saudi Arabia",
         "Brazil", "UK", "Australia", "Global"],
        index=0, key="radar_market",
    )
    radar_budget = r3.number_input("目标客单价 (USD)", min_value=1.0, value=20.0, step=1.0, key="radar_budget")

    if st.button("🚀 扫描品类机会", key="radar_btn"):
        with st.spinner("AI 正在扫描品类机会…"):
            _raw = call_groq(build_radar_prompt(radar_cat, radar_market, radar_budget), 0.5, max_tokens=1800)
        _data = parse_reverse_json(_raw) if not (isinstance(_raw, str) and _raw.startswith("❌")) else None
        if _data and _data.get("products"):
            st.session_state["radar_data"] = _data
        else:
            st.error(_raw if isinstance(_raw, str) else "AI 返回格式异常，请重试。")

    _radar = st.session_state.get("radar_data")
    if _radar:
        _items = [x for x in _radar.get("products", []) if isinstance(x, dict)]
        _pal = _br_palette(is_dark, bg_color, text_color, card_bg, border_color)
        if _radar.get("summary"):
            st.markdown(
                f'<div style="margin:6px 0 10px;padding:10px 12px;border-left:2px solid {_pal["accent"]};'
                f'background:{_pal["accent_soft"]};border-radius:10px;font-size:12px">'
                f'💡 {_br_txt(_radar.get("summary"))}</div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div style="padding:4px 2px">{_svg_bubble_chart(_items, _pal)}</div>',
            unsafe_allow_html=True,
        )
        _list = ""
        for _it in sorted(_items, key=lambda _x: -_br_num(_x.get("score")))[:8]:
            _sc = _br_num(_it.get("score"))
            _cls = "#4FB28C" if _sc >= 75 else ("#E0A64B" if _sc >= 55 else "#E06C5A")
            _q, _qc = _quadrant_label(_br_num(_it.get("demand")), _br_num(_it.get("competition")))
            _list += (
                f'<div style="display:flex;gap:10px;align-items:flex-start;padding:11px 13px;'
                f'border:1px solid {_pal["border"]};border-radius:12px;background:{_pal["card"]};margin:8px 0">'
                f'<div style="flex:1">'
                f'<div style="font-weight:700;font-size:13px;color:{_pal["text"]}">'
                f'{_br_txt(_it.get("name"))}'
                f'<span style="margin-left:8px;font-size:9.5px;padding:2px 7px;border-radius:999px;'
                f'background:{_qc}22;color:{_qc};border:1px solid {_qc}55">{_q}</span></div>'
                f'<div style="font-size:11px;color:{_pal["muted"]};margin-top:3px">'
                f'需求 {_br_num(_it.get("demand")):.0f} · 竞争 {_br_num(_it.get("competition")):.0f} · '
                f'毛利 {_br_num(_it.get("margin")):.0f}% · 建议价 {_br_txt(_it.get("price_low"))}-'
                f'{_br_txt(_it.get("price_high"))} USD</div>'
                f'<div style="font-size:11px;color:{_pal["muted"]};margin-top:3px">'
                f'💡 {_br_txt(_it.get("reason"))}　⚠ {_br_txt(_it.get("risk"))}</div>'
                f'</div>'
                f'<div style="min-width:44px;text-align:center;padding:4px 8px;border-radius:9px;'
                f'background:{_cls}22;color:{_cls};font-weight:800;font-size:13px">{_sc:.0f}</div>'
                f"</div>"
            )
        st.markdown(_list, unsafe_allow_html=True)
    else:
        st.info("填好品类与市场，点「🚀 扫描品类机会」生成选品雷达。")
