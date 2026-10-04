Dijital Pazarlama Analitiği ve Bütçe Optimizasyonu Dashboard'u

Reklam harcaması, gelir ve dönüşüm verisini temizleyen, ROI / CPA / dönüşüm oranı gibi
metrikleri hesaplayan ve sonucu **tek dosyalık, interaktif bir web dashboard'una** dönüştüren
uçtan uca bir veri analitiği projesi. Medya planlama kararlarını varsayımlara değil veriye
dayandırmak için hazırlandı.

> **Canlı demo:** GitHub Pages'i açtıktan sonra `https://<kullanici-adi>.github.io/<repo-adi>/` adresinde yayınlanır (aşağıya bakın).

Özellikler

- **KPI kartları:** Gelir, harcama, ROI ve dönüşüm oranı; önceki döneme göre değişimle birlikte.
- **Canlı filtreler:** Dönem, platform, sektör ve ülke seçimine göre tüm grafikler anında güncellenir.
- **Kanal analizi:** Platform bazında ROI ve CPA.
- **Haftalık trafik trendi:** Platformlara göre tıklama eğilimi.
- **Harcama–gelir ilişkisi:** Kampanya türüne göre dağılım grafiği ve OLS doğrusal trend (eğim ve R²).
- **Sektör × platform ısı haritası:** Hangi sektör hangi kanalda daha iyi dönüştürüyor?
- **Coğrafi fırsatlar:** CPA'sı en düşük 10 ülke.
- **Bütçe strateji tablosu:** Sıralanabilir, aranabilir; ROI dörtte birliklerine göre *Artır / Koru / Azalt* önerisi.
- **Otomatik çıkarımlar** ve **CSV dışa aktarma**, yazdırma desteği, mobil uyumlu tasarım.

Proje yapısı

```
├── build_dashboard.py          # Veriyi temizler/doğrular ve docs/index.html üretir
├── generate_sample_data.py     # Aynı şemada sentetik örnek veri üretir
├── templates/dashboard.html    # Dashboard arayüzü (HTML + CSS + JS, Chart.js)
├── data/                       # CSV dosyası buraya
├── docs/index.html            # Üretilen dashboard (GitHub Pages bu klasörü yayınlar)
└── requirements.txt
```

Kurulum ve çalıştırma

```bash
pip install -r requirements.txt

# 1) Kendi CSV'nizi data/global_ads_performance_dataset.csv olarak koyun
#    (yoksa örnek veri üretin)
python generate_sample_data.py

# 2) Dashboard'u üretin
python build_dashboard.py

# 3) docs/index.html dosyasını tarayıcıda açın
```

Farklı bir dosya için: `python build_dashboard.py --csv data/verim.csv --out docs/index.html`

Beklenen veri şeması

| Sütun | Açıklama | Zorunlu |
|---|---|---|
| `date` | Tarih (YYYY-MM-DD) | ✅ |
| `platform` | Reklam kanalı | ✅ |
| `campaign_type` | Kampanya türü | ✅ |
| `industry` | Sektör | ✅ |
| `country` | Ülke | ✅ |
| `ad_spend` | Reklam harcaması | ✅ |
| `clicks` | Tıklama | ✅ |
| `conversions` | Dönüşüm | ✅ |
| `revenue` | Gelir | ✅ |
| `impressions` | Gösterim (CTR için) | ❌ |

> Not: Repodaki örnek veri **sentetiktir**; gerçek bir kampanyayı temsil etmez. Gerçek veri setinizle çalıştırdığınızda sonuçlar ona göre değişir.

Metrik tanımları

| Metrik | Formül |
|---|---|
| Dönüşüm oranı | dönüşüm ÷ tıklama × 100 |
| ROI | (gelir − harcama) ÷ harcama × 100 |
| CPA | harcama ÷ dönüşüm |
| CTR | tıklama ÷ gösterim × 100 |

Tüm oran metrikleri **satır ortalaması yerine toplamlar üzerinden (ağırlıklı)** hesaplanır; küçük harcamalı satırların sonucu çarpıtması engellenir.

İlk sürüme göre düzeltilen hatalar

1. `display()` yalnızca Jupyter'de çalışır; script olarak çalıştırınca hata veriyordu. Artık Jupyter'e bağımlılık yok.
2. `ad_spend = 0` veya `clicks = 0` olan satırlarda sıfıra bölme (`inf`/`NaN`) ortalamaları bozuyordu. Bu satırlar temizleniyor, bölmeler güvenli yapılıyor.
3. ROI ve CPA'nın **satır ortalaması** alınması yanıltıcıydı; ağırlıklı hesaba geçildi.
4. `trendline='ols'` için `statsmodels` gerekiyordu ve kurulu değilse çöküyordu. Trend artık dashboard içinde hesaplanıyor, ek bağımlılık yok.
5. "Gelecek tahmini" ifadesi hatalıydı: OLS çizgisi bir **ilişki göstergesidir**, tahmin modeli değildir. Metinler düzeltildi, R² eklendi.
6. Eksik sütun, bozuk tarih, negatif/yinelenen satır ve `dönüşüm > tıklama` gibi veri sorunları için doğrulama ve temizlik günlüğü eklendi.
7. "En iyi 5 strateji" listesi çok düşük hacimli kombinasyonlara körü körüne güveniyordu; öneriler artık ROI dörtte birliklerine göre ve harcama hacmiyle birlikte gösteriliyor.

GitHub Pages ile yayınlama

1. Projeyi GitHub'a yükleyin.
2. **Settings → Pages → Build and deployment**: *Deploy from a branch*, branch `main`, klasör `/docs`.
3. Birkaç dakika sonra dashboard yayında olur.

Kullanılan teknolojiler

Python (pandas, numpy) · HTML/CSS/JavaScript · Chart.js

Sınırlamalar

- Dashboard grafikleri Chart.js'i CDN'den yükler; ilk açılışta internet bağlantısı gerekir.
- Veri HTML dosyasına gömülür; çok büyük veri setlerinde (yüz binlerce satır) dosya boyutu artar.
- Öneriler tarihsel performansa dayanır; bütçe değişikliklerini küçük adımlarla ve A/B testle doğrulayın.

Lisans

MIT, dilediğiniz gibi kullanabilirsiniz.
Uygulama Görselleri:
<img width="1365" height="630" alt="image" src="https://github.com/user-attachments/assets/092b266b-e3e1-4650-bcef-23aa4929bb97" />
<img width="1365" height="636" alt="image" src="https://github.com/user-attachments/assets/1472f086-b8a2-4a9d-9729-7cbddd442b65" />
<img width="1365" height="634" alt="image" src="https://github.com/user-attachments/assets/1f10a844-938e-41d4-bd1c-9327d3f634fb" />
<img width="1365" height="635" alt="image" src="https://github.com/user-attachments/assets/c41e4a24-7fc6-4a6a-abe0-0ca6aa3fc080" />
<img width="1365" height="635" alt="image" src="https://github.com/user-attachments/assets/60244c20-ea62-4bf5-980b-44c9b0f75905" />
<img width="1365" height="632" alt="image" src="https://github.com/user-attachments/assets/b3573c71-a1fe-4579-b5e4-a83ce3e4b137" />
