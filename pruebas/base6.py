import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import requests

# Placeholder para la API de Samsara
SAMSARA_API_KEY = "TU_API_KEY_AQUI"  # <-- Reemplaza con la clave real
VEHICLE_ID = "TU_VEHICULO_ID"  # <-- Reemplaza con el ID real

# Definición de variables difusas
kilometraje = ctrl.Antecedent(np.arange(0, 500000, 1000), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.arange(50, 150, 1), 'temperatura_motor')
horas_operacion = ctrl.Antecedent(np.arange(0, 20000, 100), 'horas_operacion')
vida_util_piezas = ctrl.Consequent(np.arange(0, 24, 1), 'vida_util_piezas')  # en meses

# Funciones de membresía para Kilometraje
kilometraje['bajo'] = fuzz.trimf(kilometraje.universe, [0, 0, 100000])
kilometraje['medio'] = fuzz.trimf(kilometraje.universe, [50000, 150000, 300000])
kilometraje['alto'] = fuzz.trimf(kilometraje.universe, [200000, 500000, 500000])

# Funciones de membresía para Temperatura del Motor
temperatura_motor['baja'] = fuzz.trimf(temperatura_motor.universe, [50, 60, 80])
temperatura_motor['media'] = fuzz.trimf(temperatura_motor.universe, [70, 90, 110])
temperatura_motor['alta'] = fuzz.trimf(temperatura_motor.universe, [100, 130, 150])

# Funciones de membresía para Horas de Operación
horas_operacion['bajo'] = fuzz.trimf(horas_operacion.universe, [0, 5000, 10000])
horas_operacion['medio'] = fuzz.trimf(horas_operacion.universe, [8000, 12000, 18000])
horas_operacion['alto'] = fuzz.trimf(horas_operacion.universe, [15000, 20000, 20000])

# Funciones de membresía para Vida Útil en meses
vida_util_piezas['corta'] = fuzz.trimf(vida_util_piezas.universe, [0, 3, 6])
vida_util_piezas['media'] = fuzz.trimf(vida_util_piezas.universe, [4, 8, 12])
vida_util_piezas['larga'] = fuzz.trimf(vida_util_piezas.universe, [10, 18, 24])

# Reglas difusas
regla1 = ctrl.Rule(kilometraje['alto'] | temperatura_motor['alta'] | horas_operacion['alto'], vida_util_piezas['corta'])
regla2 = ctrl.Rule(kilometraje['medio'] & temperatura_motor['media'] & horas_operacion['medio'], vida_util_piezas['media'])
regla3 = ctrl.Rule(kilometraje['bajo'] & temperatura_motor['baja'] & horas_operacion['bajo'], vida_util_piezas['larga'])

# Controlador difuso
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3])
prediccion_mantenimiento = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función para obtener datos desde Samsara
def obtener_datos_samsara():
    url = f"https://api.samsara.com/v1/vehicles/{VEHICLE_ID}/stats"
    headers = {"Authorization": f"Bearer {SAMSARA_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            datos = response.json()
            return {
                "kilometraje": datos.get("odometerMeters", 0) / 1000,  # Convertir a km
                "temperatura_motor": datos.get("engineTemperatureCelsius", 90),
                "horas_operacion": datos.get("engineHours", 0),
            }
        else:
            print("Error al obtener datos de Samsara")
            return None
    except Exception as e:
        print(f"Error en la solicitud a Samsara: {e}")
        return None

# Función principal para hacer predicción
def predecir_mantenimiento():
    datos = obtener_datos_samsara()
    if datos is None:
        datos = {"kilometraje": 120000, "temperatura_motor": 95, "horas_operacion": 10000}  # Datos simulados
    
    prediccion_mantenimiento.input['kilometraje'] = datos['kilometraje']
    prediccion_mantenimiento.input['temperatura_motor'] = datos['temperatura_motor']
    prediccion_mantenimiento.input['horas_operacion'] = datos['horas_operacion']
    
    prediccion_mantenimiento.compute()
    vida_util = prediccion_mantenimiento.output['vida_util_piezas']
    semanas = int(vida_util * 4)
    print(f"Vida útil estimada: {vida_util:.2f} meses ({semanas} semanas)")
    return vida_util, semanas

# Ejecutar la predicción
if __name__ == "__main__":
    predecir_mantenimiento()
