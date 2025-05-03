from config import SISTEM_GUC, VERIMLILIK_CARPAN, CO2_CARPAN, SURDURULEBILIRLIK_ESIK

def hesapla_karbon_ayakizi(sistem_tipi: str,
                            sure_dk: float,
                            kaynak: str,
                            verimlilik: str,
                            sistem_guc_watt_modu: bool = True):
    """
    Verilen sistem için enerji tüketimi ve CO₂ salımını hesapla.

    Parametreler
    ------------
    sistem_tipi : SISTEM_GUC anahtarı
    sure_dk     : Çalışma süresi (dakika)
    kaynak      : CO2_CARPAN anahtarı
    verimlilik  : VERIMLILIK_CARPAN anahtarı
    sistem_guc_watt_modu : True ise SISTEM_GUC değerlerini Watt,
                           False ise kWh/saat kabul eder.
    """
    guc = SISTEM_GUC[sistem_tipi]
    verim = VERIMLILIK_CARPAN[verimlilik]

    if sistem_guc_watt_modu:                 # --- Eski Watt sözlüğünü korumak için
        enerji_kwh = (guc * sure_dk * verim) / (1000 * 60)
    else:                                    # --- Yeni kWh/saat sözlüğü
        enerji_kwh = guc * (sure_dk / 60) * verim

    co2_salimi = enerji_kwh * CO2_CARPAN[kaynak]
    return enerji_kwh, co2_salimi


def surdurulebilirlik_puani(co2_salimi: float) -> str:
    """CO₂ miktarını etikete çevirir (A+ … F)."""
    # Eşikler zaten artan sırada tanımlı, yine de garantileyelim:
    for puan, esik in sorted(SURDURULEBILIRLIK_ESIK.items(), key=lambda x: x[1]):
        if co2_salimi <= esik:
            return puan
    return "F"   # teorik olarak erişilmez (float('inf') yüzünden)


def hesapla_zaman_bazli_etki(enerji_kwh_gunluk: float,
                             co2_salimi_gunluk: float):
    """Günlük değerlerden hafta / ay / yıl projeksiyonu oluşturur."""
    zaman_birimleri = ["Günlük", "Haftalık", "Aylık", "Yıllık"]
    carp = [1, 7, 30, 365]

    enerji = [enerji_kwh_gunluk * c for c in carp]
    co2    = [co2_salimi_gunluk * c for c in carp]

    return zaman_birimleri, enerji, co2