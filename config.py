# Average continuous power demand (Watts)
SISTEM_GUC = {          # kWh/saat
    "UCAV": 40000,
    "Drone": 150,
    "Industrial Robot Arm": 3000,
    "Robot Vacuum Cleaner": 60,
    "Autonomous Electric Car": 18000
}

# Model dosya yolları (GitHub raw URLs)
MODEL_PATHS = {
    "UCAV": "https://raw.githubusercontent.com/hazalnazz/ecobot-dashboard/main/models/attack_uav/scene.gltf",
    "Drone": "https://raw.githubusercontent.com/hazalnazz/ecobot-dashboard/main/models/drone/scene.gltf",
    "Industrial Robot Arm": "https://raw.githubusercontent.com/hazalnazz/ecobot-dashboard/main/models/industrial_robot_arm/scene.gltf",
    "Robot Vacuum Cleaner": "https://raw.githubusercontent.com/hazalnazz/ecobot-dashboard/main/models/robot_vacuum_cleaner_low_poly/scene.gltf",
    "Autonomous Electric Car": "https://raw.githubusercontent.com/hazalnazz/ecobot-dashboard/main/models/tesla_roadster_2020/scene.gltf"
}

# Enerji kaynaklarına göre CO2 salım çarpanları (g/kWh)
CO2_CARPAN = {
    "Şebeke Elektriği":         391,    # Turkey 2024 average
    "Güneş Enerjisi":           20,     # Utility‑scale PV median (10–36 g)
    "Batarya":                  100,    # Mid‑range Li‑ion storage (9–135 g/kWh delivered)
    "Rüzgar Enerjisi":          7,      # Modern on‑shore wind (5–8 g)
    "Hibrit (Güneş+Batarya)":   60      # Simple 50 % PV + 50 % storage blend
}

# Efficiency‑mode multipliers (kept, but renamed for clarity)
VERIMLILIK_CARPAN = {
    "Normal": 1.0,
    "Verimli": 0.8,
    "Ultra Verimli": 0.6,
    "Yoğun Kullanım": 1.2,
    "Maksimum Performans": 1.5
}

# Daily‑emission label thresholds (g CO₂ / gün)
SURDURULEBILIRLIK_ESIK = {
    "A+": 30,
    "A": 80,
    "B": 150,
    "C": 400,
    "D": 800,
    "E": 1600,
    "F": float("inf")
}