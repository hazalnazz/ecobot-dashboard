from config import SISTEM_GUC, VERIMLILIK_CARPAN, CO2_CARPAN, SURDURULEBILIRLIK_ESIK

def hesapla_karbon_ayakizi(sistem_tipi, sure_dk, kaynak, verimlilik):
    """Günlük enerji tüketimi ve CO2 salımını hesaplar."""
    guc = SISTEM_GUC[sistem_tipi]
    verimlilik_carpani = VERIMLILIK_CARPAN[verimlilik]
    # Günlük enerji tüketimi (kWh)
    enerji_kwh = (guc * sure_dk * verimlilik_carpani) / (1000 * 60)
    # Günlük CO2 salımı (gram)
    co2_salimi = enerji_kwh * CO2_CARPAN[kaynak]
    return enerji_kwh, co2_salimi

def surdurulebilirlik_puani(co2_salimi):
    """Verilen CO2 salımına göre sürdürülebilirlik puanını belirler."""
    for puan, esik in SURDURULEBILIRLIK_ESIK.items():
        if co2_salimi <= esik:
            return puan
    return "F" # Should not happen with float('inf')

def hesapla_zaman_bazli_etki(enerji_kwh_gunluk, co2_salimi_gunluk):
    """Günlük verilere dayanarak haftalık, aylık ve yıllık etkileri hesaplar."""
    zaman_birimleri = ["Günlük", "Haftalık", "Aylık", "Yıllık"]
    carpanlar = [1, 7, 30, 365]

    enerji_verileri = [enerji_kwh_gunluk * carpan for carpan in carpanlar]
    co2_verileri = [co2_salimi_gunluk * carpan for carpan in carpanlar]

    return zaman_birimleri, enerji_verileri, co2_verileri
