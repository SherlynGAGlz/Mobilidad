import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Definición de variables difusas normalizadas # cambiarlas como las primeras
kilometraje = ctrl.Antecedent(np.linspace(0, 100, 1), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.linspace(0, 100, 1), 'temperatura_motor')
horas_operacion = ctrl.Antecedent(np.linspace(0, 100, 1), 'horas_operacion')
historial_eventos = ctrl.Antecedent(np.linspace(0, 100, 1), 'historial_eventos')
rpm = ctrl.Antecedent(np.linspace(0, 100, 1), 'rpm')
masas_homocineticas = ctrl.Antecedent(np.linspace(0, 100, 1), 'masas_homocineticas')
desgaste_frenos = ctrl.Antecedent(np.linspace(0, 100, 1), 'desgaste_frenos')
vida_util_piezas = ctrl.Consequent(np.linspace(0, 100, 1), 'vida_util_piezas')

# Función para normalizar datos
def normalizar(valor, min_val, max_val):
    return max(0, min(1, (valor - min_val) / (max_val - min_val)))  # Asegurar que esté entre 0 y 1

# Definir funciones de membresía y aqui se ponen cuantas variables tendra
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

# Funciones para calcular la vida útil estimada
def calcular_vida_util_pieza(valor_normalizado):
    return max(1, round((1 - valor_normalizado) * 104))  # Asegurar que no sea negativo ni cero

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
    vida_util = max(1, round(prediccion_mantenimiento.output['vida_util_piezas'] * 104))  # Asegurar que no sea negativo ni cero

    # Identificar piezas críticas y calcular su vida útil
    piezas_criticas = {}
    for pieza, valor in datos_normalizados.items():
        if pieza in ['masas_homocineticas', 'desgaste_frenos', 'temperatura_motor', 'rpm']:
            vida_util_pieza = calcular_vida_util_pieza(valor)
            if valor > 0.8:
                piezas_criticas['frenos' if pieza == 'desgaste_frenos' else pieza] = vida_util_pieza

    # Mostrar resultados
    print(f"\n🔧 Vida útil estimada general: {vida_util} semanas")
    
    if piezas_criticas:
        print("⚠️ Las siguientes piezas requieren más atención:")
        for pieza, vida in piezas_criticas.items():
            print(f"- {pieza.replace('_', ' ').capitalize()} tiene aproximadamente {vida} semanas de vida útil.")
        
        print("\n🔍 Explicación de la predicción:")
        for pieza in piezas_criticas:
            factores = []
            if pieza == 'masas_homocineticas':
                factores.append("alto desgaste detectado en inspecciones")
            if pieza == 'frenos':
                factores.append("reducción en la eficiencia de frenado")
            if pieza == 'temperatura_motor':
                factores.append("sobrecalentamiento prolongado")
            if pieza == 'rpm':
                factores.append("uso frecuente de altas revoluciones")
            
            print(f"- {pieza.replace('_', ' ').capitalize()} necesita mantenimiento debido a: {', '.join(factores)}.")
    else:
        print("✅ No hay piezas críticas detectadas.")
    
    return vida_util, piezas_criticas

datos_prueba = {
    "kilometraje": 300000,  # Ajustado dentro de la vida útil de 500,000 - 1,000,000 km
    "temperatura_motor": 90,  # Rango óptimo entre 80°C y 95°C
    "horas_operacion": 2500,  # Ajustado a la media de operación anual
    "historial_eventos": 2,  # Considerando una media de eventos por año
    "rpm": 1500,  # Valor medio dentro del rango óptimo
    "masas_homocineticas": 5,  # Desgaste estimado según inspección cada 40,000 km
    "desgaste_frenos": 4  # Considerando revisión cada 20,000 km
}
# Datos de prueba 1: Estado óptimo
datos_prueba_1 = {
    "kilometraje": 150000,  # Dentro de la vida útil
    "temperatura_motor": 85,  # Rango óptimo
    "horas_operacion": 1000,  # Menos horas de operación
    "historial_eventos": 1,  # Pocos eventos
    "rpm": 2000,  # Dentro del rango óptimo
    "masas_homocineticas": 2,  # Bajo desgaste
    "desgaste_frenos": 1  # Bajo desgaste
}

# Datos de prueba 2: Estado crítico
datos_prueba_2 = {
    "kilometraje": 9000650,  # Alto kilometraje
    "temperatura_motor": 6455,  # Temperatura alta
    "horas_operacion": 364654650,  # Muchas horas de operación
    "historial_eventos": 5,  # Muchos eventos
    "rpm": 3000,  # RPM elevadas
    "masas_homocineticas": 8,  # Alto desgaste
    "desgaste_frenos": 9  # Alto desgaste
}

# Datos de prueba 3: Estado intermedio
datos_prueba_3 = {
    "kilometraje": 56465405,  # Kilometraje moderado
    "temperatura_motor": 88,  # Rango óptimo
    "horas_operacion": 2000,  # Horas de operación moderadas
    "historial_eventos": 6,  # Eventos moderados
    "rpm": 226500,  # Dentro del rango óptimo
    "masas_homocineticas": 6,  # Desgaste moderado
    "desgaste_frenos": 5  # Desgaste moderado
}

# Ejecutar la predicción para cada conjunto de datos
if __name__ == "__main__":
    print("Datos de prueba 1:")
    predecir_mantenimiento(datos_prueba_1)
    
    print("\nDatos de prueba 2:")
    predecir_mantenimiento(datos_prueba_2)
    
    print("\nDatos de prueba 3:")
    predecir_mantenimiento(datos_prueba_3)
    print("Datos_prueba:")
    predecir_mantenimiento(datos_prueba)
# Ejecutar la predicción
if __name__ == "__main__":
    predecir_mantenimiento(datos_prueba)