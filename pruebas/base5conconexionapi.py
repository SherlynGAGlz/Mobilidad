import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import requests

# Placeholder para la API de Samsara (Sustituir con la API real)
SAMSARA_API_KEY = "YOUR_SAMSARA_API_KEY"  # <-- PLACEHOLDER
VEHICLE_ID = "YOUR_VEHICLE_ID"  # <-- PLACEHOLDER

def obtener_datos_samsara():
    url = f"https://api.samsara.com/v1/vehicles/{VEHICLE_ID}/stats"
    headers = {"Authorization": f"Bearer {SAMSARA_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Variables de entrada
kilometraje = ctrl.Antecedent(np.arange(0, 500000, 1000), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.arange(50, 150, 1), 'temperatura_motor')
horas_operacion = ctrl.Antecedent(np.arange(0, 20000, 100), 'horas_operacion')

# Variable de salida
mantenimiento = ctrl.Consequent(np.arange(0, 100, 1), 'mantenimiento')

# Funciones de membresía para kilometraje
kilometraje['bajo'] = fuzz.trimf(kilometraje.universe, [0, 0, 100000])
kilometraje['medio'] = fuzz.trimf(kilometraje.universe, [80000, 200000, 300000])
kilometraje['alto'] = fuzz.trimf(kilometraje.universe, [250000, 500000, 500000])

# Funciones de membresía para temperatura del motor
temperatura_motor['baja'] = fuzz.trimf(temperatura_motor.universe, [50, 50, 80])
temperatura_motor['media'] = fuzz.trimf(temperatura_motor.universe, [70, 90, 110])
temperatura_motor['alta'] = fuzz.trimf(temperatura_motor.universe, [100, 130, 150])

# Funciones de membresía para horas de operación
horas_operacion['pocas'] = fuzz.trimf(horas_operacion.universe, [0, 0, 5000])
horas_operacion['moderadas'] = fuzz.trimf(horas_operacion.universe, [4000, 10000, 15000])
horas_operacion['muchas'] = fuzz.trimf(horas_operacion.universe, [12000, 20000, 20000])

# Función de membresía para el mantenimiento
mantenimiento['bajo'] = fuzz.trimf(mantenimiento.universe, [0, 0, 30])
mantenimiento['medio'] = fuzz.trimf(mantenimiento.universe, [20, 50, 80])
mantenimiento['alto'] = fuzz.trimf(mantenimiento.universe, [70, 100, 100])

# Definir reglas difusas
rule1 = ctrl.Rule(kilometraje['alto'] | temperatura_motor['alta'] | horas_operacion['muchas'], mantenimiento['alto'])
rule2 = ctrl.Rule(kilometraje['medio'] | temperatura_motor['media'] | horas_operacion['moderadas'], mantenimiento['medio'])
rule3 = ctrl.Rule(kilometraje['bajo'] | temperatura_motor['baja'] | horas_operacion['pocas'], mantenimiento['bajo'])

# Controlador difuso
mantenimiento_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
mantenimiento_sim = ctrl.ControlSystemSimulation(mantenimiento_ctrl)

def predecir_mantenimiento(km, temp, horas):
    mantenimiento_sim.input['kilometraje'] = km
    mantenimiento_sim.input['temperatura_motor'] = temp
    mantenimiento_sim.input['horas_operacion'] = horas
    mantenimiento_sim.compute()
    return mantenimiento_sim.output['mantenimiento']

# Ejemplo de uso con datos simulados
datos_samsara = obtener_datos_samsara()
if datos_samsara:
    km_actual = datos_samsara.get('odometer', 0)
    temp_actual = datos_samsara.get('engineTemperature', 90)
    horas_actuales = datos_samsara.get('engineHours', 5000)
else:
    km_actual, temp_actual, horas_actuales = 150000, 95, 7000  # Valores de prueba

resultado = predecir_mantenimiento(km_actual, temp_actual, horas_actuales)
print(f"Nivel de mantenimiento necesario: {resultado:.2f}%")
