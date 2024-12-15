# Öğretmen Analiz Uygulaması

Bu proje, öğretmen ihtiyaçlarını ve norm fazlası durumu analiz ederek, özellikle Antalya ilindeki öğretmen dengesizliklerini anlamaya yardımcı olmak ücin geliştirilmiştir. Proje, çeşitli hizmet bölgeleri ve branşlar üzerinden analiz yaparak ihtiyaç duyulan öğretmenlerin belirlenmesine yardımcı olur.

## Özellikler

*Branş bazlı analiz*: Her branşa göre fazla öğretmen ve ihtiyaç sayılarını hesaplar.

*Hizmet bölgesi analizi*: Çeşitli hizmet bölgelerindeki öğretmen ihtiyaçlarını analiz eder.

*Grafiksel analizler*: Branşlar ve bölgeler bazında ihtiyaç ve fazla öğretmen verilerini görsel olarak sunar.

*Kurum sayıları analizi*: Anaokulu, ilkokul, ortaokul ve lise bazında kurum sayılarını sunar.

*En yüksek hizmet puanı analizi*: Hizmet puanına göre öğretmenlerin sıralamasını yapar.

### Kullanılan Teknolojiler

*Python*

*pandas*

*matplotlib*

*gradio*

*Excel*

### Gereksinimler

Projeyi çalıştırmak için aşağıdaki paketlerin yüklenmiş olması gerekmektedir:

```bash
pip install pandas matplotlib gradio openpyxl
```

### Kurulum

*Projeyi klonlayın*:
```bash
git clone https://github.com/elfgk/OgretmenAnalizAntalya.git
cd OgretmenAnalizAntalya
```

*Gerekli Python kütüphanelerini yükleyin*:
```bash
pip install -r requirements.txt
```

*Veri dosyalarını projenin ana dizinine yerleştirin*:

ihtiyac_data.xlsx

norm_fazlasi.xlsx

*Uygulamayı başlatın*:
```bash
python main.py
```

*Gradio Arayüzüne Erişim*:
Komut satırında verilen URL'yi tarayıcınızda açarak arayüze erişin.

### Kullanım

Ana Fonksiyonlar

*Hizmet Bölgesi Bazlı Eksik Öğretmen Analizi*:

Seçilen branşa göre hizmet bölgelerinde öğretmen ihtiyaçlarını listeler ve bir grafik oluşturur.

*Üretli Öğretmen Sayısı Analizi*:

Seçilen branş için toplam ihtiyaç, fazla sayısı ve üretli ihtiyacı gösterir.

*Eğitim Seviyelerine Göre Kurum Analizi*:

Anaokulu, ilkokul, ortaokul ve lise bazında kurum sayılarını bir pasta grafiği üzerinde sunar.

*Hizmet Puanı Analizi*:

Hizmet puanlarına göre en yüksek puana sahip öğretmeni ve sıralamalarını gösterir.

### Katkı

Katkıda bulunmak için lütfen bir "Pull Request" oluşturun. 



