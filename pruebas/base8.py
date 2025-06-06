import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

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

# 0Reglas difusas mejoradas
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

# Función para calcular la vida útil estimada de cada pieza
def calcular_vida_util_pieza(valor_normalizado):
    return round((1 - valor_normalizado) * 104)  # 104 semanas es el máximo

# Función principal para hacer predicción e identificar piezas críticas
def predecir_mantenimiento(datos):
    datos_normalizados = {
        "kilometraje": normalizar(datos['kilometraje'], 0, 1000000),
        "temperatura_motor": normalizar(datos['temperatura_motor'], 80, 95),
        "horas_operacion": normalizar(datos['horas_operacion'], 0, 3000),
        "historial_eventos": normalizar(datos['historial_eventos'], 0, 5),
        "rpm": normalizar(datos['rpm'], 500, 5000),
        "masas_homocineticas": normalizar(datos['masas_homocineticas'], 0, 10),
        "desgaste_frenos": normalizar(datos['desgaste_frenos'], 0, 10)
    }
    
    for key, value in datos_normalizados.items():
        prediccion_mantenimiento.input[key] = value
    
    prediccion_mantenimiento.compute()
    vida_util = round(prediccion_mantenimiento.output['vida_util_piezas'] * 104)  # Convertir de [0,1] a semanas

    # Identificar piezas críticas y calcular su vida útil individual
    piezas_criticas = {}
    for pieza, valor in datos_normalizados.items():
        vida_util_pieza = calcular_vida_util_pieza(valor)
        if valor > 0.8:  # Si el desgaste es alto
            piezas_criticas[pieza] = vida_util_pieza

    # Mostrar resultados
    print(f"\n🔧 Vida útil estimada general: {vida_util} semanas")

    if piezas_criticas:
        print("⚠️ Las siguientes piezas requieren más atención:")
        for pieza, vida in piezas_criticas.items():
            print(f"- {pieza.replace('_', ' ').capitalize()} tiene aproximadamente {vida} semanas de vida útil.")
    else:
        print("✅ No hay piezas críticas detectadas.")

    return vida_util, piezas_criticas

# Datos de prueba
datos_prueba = {
    "kilometraje":300000,  # Ajustado dentro de la vida útil de 500,000 - 1,000,000 km 120000,
    "temperatura_motor":90,  # Rango óptimo entre 80°C y 95°C
    "horas_operacion": 2500,  # Ajustado a la media de operación anual
    "historial_eventos":2,  # Considerando una media de eventos por año
    "rpm": 1500,  # Valor medio dentro del rango óptimo
    "masas_homocineticas":  5,  # Desgaste estimado según inspección cada 40,000 km
    "desgaste_frenos": 4  # Considerando revisión cada 20,000 km
}

# Ejecutar la predicción
if __name__ == "__main__":
    predecir_mantenimiento(datos_prueba)
