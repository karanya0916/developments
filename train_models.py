import os
os.environ['KERAS_HOME'] = os.path.abspath('.keras')
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.makedirs('.keras', exist_ok=True)
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

os.makedirs('ml_models', exist_ok=True)
np.random.seed(42)

print("==========================================================")
print("1. TRAINING SCIKIT-LEARN CONSTRUCTION COST ESTIMATOR MODEL")
print("==========================================================")
# Generate realistic training dataset based on CPWD Plinth Area Rates and Telangana/Warangal Market Rates
# Features: [built_up_area, floors, quality_tier_code, building_type_code, location_tier_code]
# quality_tier: 1=Standard (₹1600-1850/sqft), 2=Premium (₹2100-2400/sqft), 3=Luxury (₹2600-3200/sqft)
n_samples = 1200
built_up_area = np.random.uniform(800, 6000, n_samples)
floors = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.25, 0.45, 0.20, 0.07, 0.03])
quality_tier = np.random.choice([1, 2, 3], size=n_samples, p=[0.4, 0.45, 0.15])
building_type = np.random.choice([0, 1, 2], size=n_samples, p=[0.6, 0.3, 0.1]) # 0: Villa/House, 1: Duplex, 2: Commercial
location_tier = np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3]) # 0: Warangal/Tier-2, 1: Hyderabad/Metro

# Realistic baseline rate per sqft
base_rates = {1: 1750, 2: 2250, 3: 2850}
rate_per_sqft = np.array([base_rates[q] for q in quality_tier])
# Floor height complexity factor
floor_factor = 1.0 + (floors - 1) * 0.04
# Type factor
type_factor = np.where(building_type == 1, 1.05, np.where(building_type == 2, 1.12, 1.0))
# Location factor (metro vs urban town)
loc_factor = np.where(location_tier == 1, 1.10, 1.0)
# Noise
noise = np.random.normal(0, 0.03, n_samples)

total_cost = built_up_area * rate_per_sqft * floor_factor * type_factor * loc_factor * (1.0 + noise)

# Cost component splits (Civil ~55%, Finishing ~22%, MEP ~12%, Labour ~11%)
civil_cost = total_cost * 0.55 * (1 + np.random.normal(0, 0.02, n_samples))
finishing_cost = total_cost * 0.22 * (1 + np.random.normal(0, 0.02, n_samples))
mep_cost = total_cost * 0.12 * (1 + np.random.normal(0, 0.02, n_samples))
labour_cost = total_cost * 0.11 * (1 + np.random.normal(0, 0.02, n_samples))

X_cost = np.column_stack([built_up_area, floors, quality_tier, building_type, location_tier])
y_cost = np.column_stack([total_cost, civil_cost, finishing_cost, mep_cost, labour_cost])

X_train, X_test, y_train, y_test = train_test_split(X_cost, y_cost, test_size=0.2, random_state=42)

cost_model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
cost_model.fit(X_train, y_train)

y_pred = cost_model.predict(X_test)
r2 = r2_score(y_test[:, 0], y_pred[:, 0])
mae = mean_absolute_error(y_test[:, 0], y_pred[:, 0])
print(f"Cost Model Evaluation -> R2 Score: {r2:.4f}, MAE: ₹{mae:,.2f}")

joblib.dump(cost_model, 'ml_models/cost_estimator.pkl')


print("\n==========================================================")
print("2. TRAINING SCIKIT-LEARN MATERIAL REQUIREMENT FORECASTER")
print("==========================================================")
# Indian Standard rule of thumb take-offs:
# Cement: ~0.40 - 0.45 bags per sq.ft
# Steel: ~3.5 - 4.5 kg per sq.ft (0.0038 tons/sqft)
# Sand: ~1.8 - 2.2 cu.ft or ~0.07 tons per sq.ft
# Coarse Aggregate: ~1.2 - 1.5 cu.ft or ~0.05 brass per sq.ft
# Bricks: ~8 - 10 bricks per sq.ft of built-up area
# Paint: ~0.15 - 0.18 liters per sq.ft

cement_bags = built_up_area * (0.42 + 0.02 * (quality_tier - 1)) * (1 + np.random.normal(0, 0.03, n_samples))
steel_tons = built_up_area * (0.0038 + 0.0004 * (floors > 2)) * (1 + np.random.normal(0, 0.03, n_samples))
sand_tons = built_up_area * 0.072 * (1 + np.random.normal(0, 0.03, n_samples))
bricks_count = built_up_area * (8.8 + 0.4 * (floors - 1)) * (1 + np.random.normal(0, 0.03, n_samples))
paint_liters = built_up_area * 0.16 * (1 + np.random.normal(0, 0.03, n_samples))

y_material = np.column_stack([cement_bags, steel_tons, sand_tons, bricks_count, paint_liters])
X_mat_train, X_mat_test, y_mat_train, y_mat_test = train_test_split(X_cost, y_material, test_size=0.2, random_state=42)

material_model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
material_model.fit(X_mat_train, y_mat_train)

y_mat_pred = material_model.predict(X_mat_test)
mat_r2 = r2_score(y_mat_test, y_mat_pred, multioutput='uniform_average')
print(f"Material Forecast Model Evaluation -> Average R2 Score: {mat_r2:.4f}")

joblib.dump(material_model, 'ml_models/material_forecaster.pkl')


print("\n==========================================================")
print("3. TRAINING SCIKIT-LEARN PROJECT DELAY RISK CLASSIFIER")
print("==========================================================")
# Features: [schedule_variance_percent, workforce_attendance_rate, material_shortage_count, rain_days_forecast, open_critical_tasks]
n_risk = 800
sched_var = np.random.uniform(-10, 40, n_risk) # positive means behind schedule
wf_rate = np.random.uniform(0.5, 1.0, n_risk) # 1.0 = 100% attendance
shortages = np.random.poisson(lam=1.5, size=n_risk)
rain_days = np.random.randint(0, 10, n_risk)
crit_tasks = np.random.randint(0, 5, n_risk)

# Risk score formula
risk_score = (
    sched_var * 1.5 +
    (1.0 - wf_rate) * 50 +
    shortages * 8 +
    rain_days * 3 +
    crit_tasks * 6
)

# Classes: 0: Low Risk, 1: Moderate Risk, 2: High Risk
delay_labels = np.zeros(n_risk, dtype=int)
delay_labels[risk_score > 35] = 1
delay_labels[risk_score > 65] = 2

X_risk = np.column_stack([sched_var, wf_rate, shortages, rain_days, crit_tasks])
X_risk_train, X_risk_test, y_risk_train, y_risk_test = train_test_split(X_risk, delay_labels, test_size=0.2, random_state=42)

risk_model = GradientBoostingClassifier(n_estimators=80, random_state=42)
risk_model.fit(X_risk_train, y_risk_train)

risk_acc = accuracy_score(y_risk_test, risk_model.predict(X_risk_test))
print(f"Delay Risk Classifier Accuracy: {risk_acc * 100:.2f}%")

joblib.dump(risk_model, 'ml_models/delay_risk_model.pkl')


print("\n==========================================================")
print("4. BUILDING & TRAINING TENSORFLOW/KERAS STAGE CLASSIFIER")
print("==========================================================")
# Deep learning model for Construction Site Image Analysis
# Stages: 0: Foundation, 1: RCC_Framing, 2: Masonry, 3: Finishing_Exterior, 4: Site_Safety
stage_classes = ['Foundation', 'RCC_Framing', 'Masonry', 'Finishing_Exterior', 'Site_Safety']

# Create synthetic visual feature dataset (64x64x3 RGB images representing stage patterns)
img_size = 64
n_images = 600
X_imgs = np.zeros((n_images, img_size, img_size, 3), dtype=np.float32)
y_stage = np.zeros(n_images, dtype=np.int32)

for i in range(n_images):
    c = i % 5
    y_stage[i] = c
    # Distinct texture/color signatures per construction stage
    if c == 0:  # Foundation: Earthy brown/mud & excavation grey
        base = np.random.normal(0.4, 0.1, (img_size, img_size, 3))
        base[:, :, 0] += 0.2  # Red/brown earth
    elif c == 1: # RCC Framing: Concrete grey with dark vertical rebar grid
        base = np.random.normal(0.5, 0.08, (img_size, img_size, 3))
        base[::8, :, :] *= 0.3 # Rebar/beam lines
        base[:, ::8, :] *= 0.3
    elif c == 2: # Masonry: Brick red / terracotta pattern with mortar lines
        base = np.random.normal(0.55, 0.08, (img_size, img_size, 3))
        base[:, :, 0] += 0.35 # Red brick hue
        base[::6, :, :] = 0.8 # Mortar lines
    elif c == 3: # Finishing / Exterior: Clean ivory/navy/glass modern facade
        base = np.random.normal(0.7, 0.05, (img_size, img_size, 3))
        base[:20, :, 2] += 0.25 # Blue sky / window reflection
        base[30:50, 10:40, 0] += 0.2 # Wood accent
    else: # Site Safety: High-visibility neon yellow/orange & helmet signage
        base = np.random.normal(0.3, 0.1, (img_size, img_size, 3))
        base[20:44, 20:44, 0] = 0.95 # Safety orange / yellow
        base[20:44, 20:44, 1] = 0.85

    X_imgs[i] = np.clip(base + np.random.normal(0, 0.05, (img_size, img_size, 3)), 0.0, 1.0)

X_img_train, X_img_test, y_stage_train, y_stage_test = train_test_split(X_imgs, y_stage, test_size=0.2, random_state=42)

# CNN Architecture
model = keras.Sequential([
    layers.Input(shape=(img_size, img_size, 3)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(5, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())
history = model.fit(
    X_img_train, y_stage_train,
    epochs=12,
    batch_size=32,
    validation_data=(X_img_test, y_stage_test),
    verbose=1
)

test_loss, test_acc = model.evaluate(X_img_test, y_stage_test, verbose=0)
print(f"TensorFlow CNN Stage Classifier Test Accuracy: {test_acc * 100:.2f}%")

model_path = 'ml_models/construction_stage_classifier.keras'
model.save(model_path)
print(f"Saved TensorFlow model to {model_path}")

# Save class labels and metadata
metadata = {
    'stage_classes': stage_classes,
    'input_size': [img_size, img_size, 3],
    'accuracy': float(test_acc),
    'loss': float(test_loss),
    'trained_date': '2026-11-24'
}
with open('ml_models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\nAll Scikit-Learn and TensorFlow models trained, evaluated, and saved successfully!")
