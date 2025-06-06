import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import requests

# Placeholder para la API de Samsara
SAMSARA_API_KEY = "TU_API_KEY_AQUI"  # <-- Reemplaza con la clave real
VEHICLE_ID = "TU_VEHICULO_ID"  # <-- Reemplaza con el ID real

# Definición de variables difusas normalizadas
kilometraje = ctrl.Antecedent(np.linspace(0, 1, 100), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.linspace(0, 1, 100), 'temperatura_motor')
horas_operacion = ctrl.Antecedent(np.linspace(0, 1, 100), 'horas_operacion')
historial_eventos = ctrl.Antecedent(np.linspace(0, 1, 100), 'historial_eventos')
rpm = ctrl.Antecedent(np.linspace(0, 1, 100), 'rpm')
masas_homocineticas = ctrl.Antecedent(np.linspace(0, 1, 100), 'masas_homocineticas')
desgaste_frenos = ctrl.Antecedent(np.linspace(0, 1, 100), 'desgaste_frenos')
vida_util_piezas = ctrl.Consequent(np.linspace(0, 1, 100), 'vida_util_piezas')

# Función para normalizar datos
def normalizar(valor, min_val, max_val):
    return (valor - min_val) / (max_val - min_val)

# Definir funciones de membresía
kilometraje.automf(5)
temperatura_motor.automf(5)
horas_operacion.automf(5)
historial_eventos.automf(5)
rpm.automf(5)
masas_homocineticas.automf(5)
desgaste_frenos.automf(5)
vida_util_piezas.automf(5)

# Reglas difusas mejoradas
reglas = [
    ctrl.Rule(kilometraje['poor'] | temperatura_motor['good'] | horas_operacion['good'] | 
              historial_eventos['good'] | rpm['good'] | masas_homocineticas['poor'] | desgaste_frenos['good'], 
              vida_util_piezas['poor']),
    
    ctrl.Rule(kilometraje['mediocre'] | temperatura_motor['average'] | horas_operacion['average'] | 
              historial_eventos['average'] | rpm['average'] | masas_homocineticas['mediocre'] | desgaste_frenos['average'], 
              vida_util_piezas['mediocre']),
    
    ctrl.Rule(kilometraje['average'] & temperatura_motor['average'] & horas_operacion['average'] & 
              historial_eventos['average'] & rpm['average'] & masas_homocineticas['average'] & desgaste_frenos['average'], 
              vida_util_piezas['average']),
    
    ctrl.Rule(kilometraje['good'] & temperatura_motor['mediocre'] & horas_operacion['mediocre'] & 
              historial_eventos['mediocre'] & rpm['mediocre'] & masas_homocineticas['good'] & desgaste_frenos['mediocre'], 
              vida_util_piezas['good']),
    
    ctrl.Rule(kilometraje['good'] & temperatura_motor['poor'] & horas_operacion['poor'] & 
              historial_eventos['poor'] & rpm['poor'] & masas_homocineticas['good'] & desgaste_frenos['poor'], 
              vida_util_piezas['good'])
]


# Controlador difuso
sistema_ctrl = ctrl.ControlSystem(reglas)
prediccion_mantenimiento = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función principal para hacer predicción
def predecir_mantenimiento(datos):
    datos_normalizados = {
        "kilometraje": normalizar(datos['kilometraje'], 0, 500000),
        "temperatura_motor": normalizar(datos['temperatura_motor'], 50, 150),
        "horas_operacion": normalizar(datos['horas_operacion'], 0, 20000),
        "historial_eventos": normalizar(datos['historial_eventos'], 0, 10),
        "rpm": normalizar(datos['rpm'], 500, 5000),
        "masas_homocineticas": normalizar(datos['masas_homocineticas'], 0, 10),
        "desgaste_frenos": normalizar(datos['desgaste_frenos'], 0, 10)
    }
    
    for key, value in datos_normalizados.items():
        prediccion_mantenimiento.input[key] = value
    
    prediccion_mantenimiento.compute()
    vida_util = prediccion_mantenimiento.output['vida_util_piezas'] * 104  # Convertir de [0,1] a semanas
    print(f"Vida útil estimada: {vida_util:.2f} semanas")
    return vida_util

# Datos de prueba
datos_prueba = {
    "kilometraje": 120000, "temperatura_motor": 95, "horas_operacion": 10000,
    "historial_eventos": 5, "rpm": 2500, "masas_homocineticas": 5, "desgaste_frenos": 5
}

# Ejecutar la predicción
if __name__ == "__main__":
    predecir_mantenimiento(datos_prueba)
