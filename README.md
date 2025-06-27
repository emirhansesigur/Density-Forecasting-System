# 🎮 Yoğunluk Tahmin Sistemi - Game Factory (Özdilek)  
Makine Öğrenmesi Tabanlı Ziyaretçi Yoğunluğu Tahmin ve Yönetim Sistemi

## 📌 Proje Hakkında

Bu proje, Özdilek Holding çatısı altında faaliyet gösteren **Game Factory Antalya** şubesindeki eğlence alanlarında kullanıcı yoğunluğunu tahmin etmek amacıyla geliştirilmiştir. Yaklaşık **3.5 yıllık gerçek veri** kullanılarak, ziyaretçi trafiği tahmin edilmekte ve bu sayede işletmenin operasyonel verimliliği artırılmaktadır.

Projenin temel hedefleri:
- Kullanıcı yoğunluğunu saatlik ve günlük tahmin etmek
- Kaynakları daha verimli kullanmak
- Müşteri deneyimini iyileştirmek
- Veri temelli karar mekanizmaları kurmak

## 🧠 Kullanılan Makine Öğrenmesi Algoritmaları

Aşağıdaki algoritmalar test edilmiş, performans karşılaştırmaları yapılmıştır:

- ✅ **Random Forest Regressor** (En başarılı model)
- XGBoost
- LightGBM
- CatBoost
- Gradient Boosting
- Linear Regression

Model başarısı; `MAE`, `RMSE`, `R²` metrikleriyle değerlendirilmiştir.

## 🔍 Özellik Mühendisliği (Feature Engineering)

Veri seti hem içsel hem de dışsal değişkenlerle zenginleştirildi:

**Zaman temelli değişkenler:**
- Saat, gün, ay, yıl
- Haftanın günü, hafta sonu mu
- Tatil öncesi mi
- Mevsim bilgisi
- Saat grubu (sabah, öğle, akşam)

**Dışsal değişkenler (API üzerinden alınan):**
- Sıcaklık (°C)
- Nem (%)
- Yağış miktarı (mm)

Bu özellikler sayesinde modelin öngörü gücü anlamlı ölçüde artırıldı.

## 🔧 Backend (API) Geliştirme

Makine öğrenmesi modeli `joblib` ile `.pkl` formatında kaydedildi. **FastAPI** ile REST API servisi oluşturuldu.

### API Uç Noktaları

| Endpoint | Açıklama |
|----------|----------|
| `POST /api/predictUsersByHour` | Belirli bir tarih-saat için tahmin döner |
| `POST /api/predictUsersByDay`  | Bir gün içindeki saatlik tahminleri topluca döner |

**Open-meteo** API kullanılarak geleceğe yönelik hava durumu verileri entegre edilmiştir. Bu sayede model dışsal çevre etkilerini de dikkate alarak tahmin yapar.

## 🌐 Frontend (Arayüz)

HTML, CSS ve JavaScript kullanılarak sade ve kullanıcı dostu bir arayüz geliştirildi.

### Ekranlar:
- 📊 **Günlük Tahmin**: Saat bazlı tahmin grafiği ve istatistik özetleri
- 📅 **Haftalık Tahmin**: Tüm haftaya ait ziyaretçi tahminlerini tablo halinde sunar

Mobil uyumlu tasarımı sayesinde farklı cihazlardan rahatlıkla erişilebilir.

## 🛠️ Kullanılan Teknolojiler

| Kategori | Teknolojiler |
|---------|--------------|
| Backend | FastAPI, Joblib, Open-meteo API |
| ML | Scikit-learn, XGBoost, LightGBM, CatBoost |
| Data | Pandas, NumPy, Matplotlib, Seaborn |
| Geliştirme | JupyterLab, Postman, VS Code |
| Frontend | HTML, CSS, JavaScript |


## 🧪 Nasıl Test Edilir?

1. Sanal ortamın oluşturulması ve gerekliliklerin yüklenmesi

```bash
python -m venv venv

.\venv\Scripts\activate 

pip install -r requirements.txt 
```

2. Backend kodlarının çalıştırılması
```bash
python -m uvicorn app.main:app --reload
```

3. frontend kodlarının çalıştırılması:
```bash
cd frontend

python -m http.server 5500
```

## 💻 Geliştiriciler

👩🏼‍💻 [Esranur Sevilmiş](https://github.com/esranursevilmis)

👨🏻‍💻 [Emirhan Ahmet Sesigür](https://github.com/emirhansesigur)


