# Sistem güç tüketimleri (Watt)
SISTEM_GUC = {
    "Attack UAV": 120,
    "Drone": 100,
    "Industrial Robot Arm": 800,
    "Robot Vacuum Cleaner": 60,
    "Autonomous Electric Car": 2000  # Assuming Tesla Roadster power usage
}

# Model dosya yolları (Proje kök dizinine göreceli)
MODEL_PATHS = {
    "Attack UAV": "models/attack_uav/scene.gltf",
    "Drone": "models/drone/scene.gltf",
    "Industrial Robot Arm": "models/industrial_robot_arm/scene.gltf",
    "Robot Vacuum Cleaner": "models/robot_vacuum_cleaner_low_poly/scene.gltf",
    "Autonomous Electric Car": "models/tesla_roadster_2020/scene.gltf"
}

# Enerji kaynaklarına göre CO2 salım çarpanları (g/kWh)
CO2_CARPAN = {
    "Şebeke Elektriği": 476,
    "Güneş Enerjisi": 45,
    "Batarya": 200,  # Example value, depends on battery production/source
    "Rüzgar Enerjisi": 11,
    "Hibrit (Güneş+Batarya)": 120 # Example value
}

# Verimlilik modlarına göre çarpanlar
VERIMLILIK_CARPAN = {
    "Normal": 1.0,
    "Verimli": 0.8,
    "Yoğun Kullanım": 1.2,
    "Ultra Verimli": 0.6,
    "Maksimum Performans": 1.5
}

# Sürdürülebilirlik puanlama sistemi için eşik değerler (gram CO2/günlük kullanım)
SURDURULEBILIRLIK_ESIK = {
    "A+": 50,
    "A": 100,
    "B": 200,
    "C": 500,
    "D": 1000,
    "E": 2000,
    "F": float('inf')
}

# Static file server URL (Update if you use a different port)
STATIC_SERVER_URL = "http://localhost:8502/" # Ensure this matches streamlit_static_server.py PORT
