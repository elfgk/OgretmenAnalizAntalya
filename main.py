import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

ihtiyac_df = pd.read_excel("ihtiyac_data.xlsx")
fazla_df = pd.read_excel("norm_fazlasi.xlsx")

# Branşlar listesi
branşlar = fazla_df['Branşı'].unique().tolist()

# Fazla öğretmen sayısını hesaplama
fazla_ogretmen = fazla_df.groupby('Branşı').size().reset_index(name='fazla_sayisi')

# Branşa göre ihtiyaçların toplamını hesaplama
branş_ihtiyac_df = ihtiyac_df.groupby('branş', as_index=False)['ihtiyac'].sum()

# Fazla öğretmen ve ihtiyaç verisini birleştirme
merged_df = pd.merge(branş_ihtiyac_df, fazla_ogretmen, left_on='branş', right_on='Branşı', how='left')
merged_df['fazla_sayisi'] = merged_df['fazla_sayisi'].fillna(0)
merged_df['kalan_ihtiyac'] = merged_df['ihtiyac'] - merged_df['fazla_sayisi']
merged_df['kalan_ihtiyac'] = merged_df['kalan_ihtiyac'].apply(lambda x: max(x, 0))
merged_df['ucretli_ihtiyaci'] = merged_df['kalan_ihtiyac']

# Hizmet bölgelerine göre toplam ihtiyaç hesaplama
hizmet_bolgesi_ihtiyac_df = ihtiyac_df.groupby('hizmet_bolgesi', as_index=False)['ihtiyac'].sum()

# Fazla öğretmen verisini hizmet bölgesine göre gruplayarak hesapla
fazla_bolgesi_df = fazla_df.groupby('HizmetPuanı').size().reset_index(name='fazla_sayisi')

# Verileri birleştir
merged_bolge_df = pd.merge(hizmet_bolgesi_ihtiyac_df, fazla_bolgesi_df, left_on='hizmet_bolgesi', right_on='HizmetPuanı', how='left')

# Fazla öğretmen olmayan bölgeler için 0 atama
merged_bolge_df['fazla_sayisi'] = merged_bolge_df['fazla_sayisi'].fillna(0)

# Kalan ihtiyaçları hesaplama
merged_bolge_df['kalan_ihtiyac'] = merged_bolge_df['ihtiyac'] - merged_bolge_df['fazla_sayisi']
merged_bolge_df['kalan_ihtiyac'] = merged_bolge_df['kalan_ihtiyac'].apply(lambda x: max(x, 0))

# Hizmet bölgesine göre kalan ihtiyaçları sırala
merged_bolge_df_sorted = merged_bolge_df.sort_values(by='kalan_ihtiyac', ascending=True)


def hizmet_bolgesine_gore_eksik_ogretmen(branş):
    # Seçilen branşın verilerini filtrele
    branş_ihtiyac_df = ihtiyac_df[ihtiyac_df['branş'] == branş]
    
    # Her bir hizmet bölgesinde ihtiyaçları grupla
    hizmet_bolgesi_ihtiyac_df = branş_ihtiyac_df.groupby('hizmet_bolgesi', as_index=False)['ihtiyac'].sum()
    
    # Grafik oluşturma
    fig, ax = plt.subplots(figsize=(10, 6))
    hizmet_bolgesi_ihtiyac_df.plot(kind='bar', x='hizmet_bolgesi', y='ihtiyac', ax=ax, color='green')
    ax.set_title(f"{branş} Branşı İçin Hizmet Bölgelerinde İhtiyaç Dağılımı")
    ax.set_ylabel("İhtiyaç Sayısı")
    ax.set_xlabel("Hizmet Bölgesi")
    plt.tight_layout()
    
    # Grafik döndürme
    return hizmet_bolgesi_ihtiyac_df[['hizmet_bolgesi', 'ihtiyac']], fig



# Ücretli öğretmen hesaplama fonksiyonu
def ucretli_ogretmenler(branş):
    # Seçilen branşın verilerini çekme
    branş_veri = merged_df[merged_df['branş'] == branş]
    
    if branş_veri.empty:
        return "Bu branş için veri bulunamadı.", None
    
    ihtiyac = int(branş_veri['ihtiyac'].values[0])
    fazla_sayisi = int(branş_veri['fazla_sayisi'].values[0])
    ucretli_ihtiyaci = int(branş_veri['ucretli_ihtiyaci'].values[0])
    
    # Grafik oluşturma
    fig, ax = plt.subplots()
    ax.bar(['İhtiyaç', 'Fazla Sayısı', 'Ücretli İhtiyacı'], [ihtiyac, fazla_sayisi, ucretli_ihtiyaci], color=['blue', 'orange', 'green'])
    ax.set_title(f"{branş} Branşı Analizi")
    ax.set_ylabel("Sayı")
    ax.set_xlabel("Kategoriler")
    plt.tight_layout()
    
    return (f"Seçilen Branş: {branş}\n\n"
            f"İhtiyaç: {ihtiyac}\n"
            f"Fazla Sayısı: {fazla_sayisi}\n"
            f"Ücretli İhtiyacı: {ucretli_ihtiyaci}"), fig

def clear():
    
    return '', None


def en_fazla_hizmet_puani_ogretmeni_bul():
    # Hizmet puanlarına göre en yüksek olanı bul
    max_hizmet_puani = fazla_df['HizmetPuanı'].max()

    # En yüksek hizmet puanına sahip öğretmen ve branşını bul
    en_yuksek_puan_ogretmen = fazla_df[fazla_df['HizmetPuanı'] == max_hizmet_puani]

    # Sonuçları döndür
    if not en_yuksek_puan_ogretmen.empty:
        return f"En fazla hizmet puanına sahip öğretmen: {en_yuksek_puan_ogretmen['Adı'].values[0]}\nBranşı: {en_yuksek_puan_ogretmen['Branşı'].values[0]}\nHizmet Puanı: {max_hizmet_puani}"
    else:
        return "Veri bulunamadı."


# Hizmet puanına göre sıralama 
def hizmet_puanina_gore_sirala(branş):
    branş_df = fazla_df[fazla_df['Branşı'] == branş]
    
    # Hizmet puanına göre sıralama
    branş_df_sorted = branş_df.sort_values(by='HizmetPuanı', ascending=False)
    
    # Sonuçları döndür
    return branş_df_sorted[['Adı', 'HizmetPuanı']]



def kac_okul_var():
    
    egitim_seviyeleri = ['anaokulu', 'ilkokul', 'ortaokul', 'lise']
    
    # Eğitim seviyelerine göre kurumları sayma
    kurum_sayisi = {}
    for egitim_seviyesi in egitim_seviyeleri:
        # Eğitim seviyesine göre filtreleme
        filtrelenmis_kurumlar = ihtiyac_df[ihtiyac_df['okul'].str.contains(egitim_seviyesi, case=False, na=False)]
        kurum_sayisi[egitim_seviyesi] = filtrelenmis_kurumlar.shape[0]

    # Pasta grafiği için verileri hazırlama
    labels = list(kurum_sayisi.keys())
    sizes = list(kurum_sayisi.values())

    # Grafik başlığı
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_title('Eğitim Seviyelerine Göre Kurum Dağılımı')

    # Pasta grafiği oluşturma
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.axis('equal')  # Dairesel 

    # Sonuçları formatlı bir şekilde döndürme
    sonuc = "Eğitim Seviyelerine Göre Kurum Sayıları:\n"
    for egitim_seviyesi, sayi in kurum_sayisi.items():
        sonuc += f"{egitim_seviyesi.capitalize()}: {sayi} kurum\n"
    
    return sonuc, fig




def birinci_hizmet_bolgesi_okullari(branş):
    # Hizmet bölgesi 4 olan ve belirtilen branşa uyan okulları filtrele
    birinci_hizmet_bolgesi_okullari = ihtiyac_df[
        (ihtiyac_df['hizmet_bolgesi'] == 1) & (ihtiyac_df['branş'] == branş)
    ]['okul']
    
    # DataFrame'e dönüştür
    birinci_hizmet_bolgesi_df = pd.DataFrame(birinci_hizmet_bolgesi_okullari, columns=['okul'])
    
    # Sonucu döndür
    return dorduncu_hizmet_bolgesi_df


   
def ikinci_hizmet_bolgesi_okullari():
    # 1. hizmet bölgesine ait okulları filtreleyip, sadece okul isimlerini almak
    ikinci_hizmet_bolgesi_okullari = ihtiyac_df[ihtiyac_df['hizmet_bolgesi'] == 2]['okul']
    ikinci_hizmet_bolgesi_df = pd.DataFrame(ikinci_hizmet_bolgesi_okullari)
    return  ikinci_hizmet_bolgesi_df


def ucuncu_hizmet_bolgesi_okullari():
    # 1. hizmet bölgesine ait okulları filtreleyip, sadece okul isimlerini almak
    ucuncu_hizmet_bolgesi_okullari = ihtiyac_df[ihtiyac_df['hizmet_bolgesi'] == 3]['okul']
    ucuncu_hizmet_bolgesi_df = pd.DataFrame(ucuncu_hizmet_bolgesi_okullari)

    # Tüm satır ve sütunların görünmesini sağlama
    pd.set_option('display.max_rows', None)  # Tüm satırları göster
    pd.set_option('display.max_columns', None)  # Tüm sütunları göster
    return  ucuncu_hizmet_bolgesi_df

def dorduncu_hizmet_bolgesi_okullari(branş):
    # Hizmet bölgesi 4 olan ve belirtilen branşa uyan okulları filtrele
    dorduncu_hizmet_bolgesi_okullari = ihtiyac_df[
        (ihtiyac_df['hizmet_bolgesi'] == 4) & (ihtiyac_df['branş'] == branş)
    ]['okul']
    
    # DataFrame'e dönüştür
    dorduncu_hizmet_bolgesi_df = pd.DataFrame(dorduncu_hizmet_bolgesi_okullari, columns=['okul'])
    
    # Sonucu döndür
    return dorduncu_hizmet_bolgesi_df
