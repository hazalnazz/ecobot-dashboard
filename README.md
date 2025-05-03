# EcoBot - Otonom Sistemler için Sürdürülebilirlik Analiz Aracı

EcoBot, otonom sistemlerin enerji tüketimi ve karbon ayak izini analiz etmek için geliştirilmiş interaktif bir dijital araçtır. Yerel 3D model görselleştirme ile birlikte kapsamlı sürdürülebilirlik analizleri sunar.

![EcoBot Dashboard](https://via.placeholder.com/800x400?text=EcoBot+Dashboard+Local)

## Özellikler

- **Yerel 3D Model Görselleştirme**: Otonom sistemlerin `models` klasöründen yüklenen 360° dönen interaktif 3D modellerini görüntüleme
- **Sürdürülebilirlik Analizi**: Enerji tüketimi ve CO₂ salımı hesaplamaları
- **Sürdürülebilirlik Puanlaması**: A+ dan F'ye kadar sistemlerin çevresel etki derecelendirmesi
- **Karşılaştırmalı Analiz**: Farklı enerji kaynakları ve sistemlerin karşılaştırılması
- **Zaman Bazlı Projeksiyonlar**: Günlük, haftalık, aylık ve yıllık çevresel etki projeksiyonları
- **Optimizasyon Önerileri**: Enerji verimliliğini artırmak için öneriler

## Desteklenen Otonom Sistemler

(Modeller `models` klasöründe bulunur)
- Attack UAV
- Drone
- Industrial Robot Arm
- Robot Vacuum Cleaner
- Autonomous Electric Car (Tesla Roadster 2020)

## Kurulum

1.  Repoyu klonlayın:
    ```bash
    git clone https://github.com/username/ecobot.git
    cd ecobot
    ```

2.  Sanal ortam oluşturun ve bağımlılıkları yükleyin:
    ```bash
    python -m venv .venv
    # Linux/macOS
    source .venv/bin/activate
    # Windows
    # .venv\Scripts\activate

    # Projeyi düzenlenebilir modda kurun
    pip install -e .
    ```

3.  **Streamlit Uygulamasını Başlatın:**
    ```bash
    streamlit run main.py
    ```

    Uygulama şimdi tarayıcınızda açılmalıdır.

## Kullanım

1.  Uygulama açıldığında, sol kenar çubuğundan bir otonom sistem seçin.
2.  Seçilen sistemin 3D modelini "3D Model" sekmesinde inceleyin.
3.  Kenar çubuğunda günlük kullanım süresini, enerji kaynağını ve verimlilik modunu ayarlayın.
4.  "Analiz", "Karşılaştırma" ve "Projeksiyon" sekmelerindeki sonuçları görüntüleyin.
5.  "Analiz" sekmesindeki optimizasyon önerilerini inceleyin.

## Sorun Giderme (Troubleshooting)

**3D Modeller Yüklenmiyor / Hata Veriyor:**

1.  **Statik Sunucu Çalışıyor mu?**: `streamlit_static_server.py` betiğinin ayrı bir terminalde çalıştığından ve hata vermediğinden emin olun. Durmuşsa tekrar başlatın.
2.  **Doğru Port Kullanılıyor mu?**: `streamlit_static_server.py` betiğinin kullandığı port (varsayılan: 8502) ile `config.py` dosyasındaki `STATIC_SERVER_URL` içinde belirtilen portun aynı olduğunu kontrol edin.
3.  **Model Dosyaları Mevcut mu?**: `models` klasöründe, `config.py` içinde belirtilen yollarda (`MODEL_PATHS`) `.gltf` dosyalarının bulunduğunu doğrulayın. `python check_models.py` komutunu çalıştırarak temel bir kontrol yapabilirsiniz.
4.  **Tarayıcı Konsolunu Kontrol Edin**: Tarayıcınızda F12 tuşuna basarak geliştirici konsolunu açın. 'Console' ve 'Network' sekmelerinde 404 (Not Found), CORS veya başka hatalar olup olmadığına bakın. 404 hatası genellikle sunucunun çalışmadığı veya dosya yolunun yanlış olduğu anlamına gelir.
5.  **URL'yi Doğrudan Deneyin**: Tarayıcı konsolunda veya `model_viewer.py` içindeki hata mesajında görünen model URL'sini (örn. `http://localhost:8502/models/attack_uav/scene.gltf`) kopyalayıp doğrudan tarayıcınızın adres çubuğuna yapıştırın. Model dosyasının içeriğini mi görüyorsunuz yoksa bir hata mı alıyorsunuz?

## Teknolojiler

- **Streamlit**: Web arayüzü
- **Plotly**: Veri görselleştirme
- **Three.js**: 3D model görüntüleme (istemci tarafı)
- **Pandas**: Veri işleme
- **Python http.server**: Yerel 3D model sunumu

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasını inceleyebilirsiniz. (Not: Henüz bir LICENSE dosyası eklenmemiş.)

## Katkıda Bulunma

Katkıda bulunmak için lütfen bir pull request oluşturun veya bir issue açın.

## 3D Model Kredileri

Tüm 3D modeller CC-BY-4.0 lisansı altında kullanılmıştır. Her bir modelin spesifik lisans bilgileri için ilgili `models/[model_adı]/license.txt` dosyasına bakınız. Modellerin doğru şekilde yüklenebilmesi için `streamlit_static_server.py` betiğinin çalışıyor olması gerekmektedir.
