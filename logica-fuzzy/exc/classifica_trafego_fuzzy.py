import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variaveis de entrada
quantidade = ctrl.Antecedent(np.arange(0, 251, 1), 'quantidade')
velocidade = ctrl.Antecedent(np.arange(0, 81, 1), 'velocidade')

# Variaveis de saida
trafego = ctrl.Consequent(np.arange(0, 101, 1), 'trafego')

# 1. Determinando o grau de pertinência das entradas para cada conjunto fuzzy

# Quantidade de veículos
quantidade['poucos'] = fuzz.trimf(quantidade.universe, [0, 0, 100])
quantidade['medio'] = fuzz.trimf(quantidade.universe, [50, 100, 200])
quantidade['muitos'] = fuzz.trimf(quantidade.universe, [150, 250, 250])

# Velocidade média
velocidade['baixa'] = fuzz.trimf(velocidade.universe, [0, 0, 30])
velocidade['media'] = fuzz.trimf(velocidade.universe, [20, 40, 60])
velocidade['alta'] = fuzz.trimf(velocidade.universe, [50, 80, 80])

# Nível de tráfego
trafego['leve'] = fuzz.trimf(trafego.universe, [0, 0, 50])
trafego['moderado'] = fuzz.trimf(trafego.universe, [25, 50, 75])
trafego['congestinado'] = fuzz.trimf(trafego.universe, [50, 100, 100])

# 2. Regras fuzzy para inferir o nível de tráfego de cada cenário.
regra1 = ctrl.Rule(quantidade['poucos'] & velocidade['alta'], trafego['leve'])
regra2 = ctrl.Rule(quantidade['medio'] & velocidade['media'], trafego['moderado'])
regra3 = ctrl.Rule(quantidade['muitos'] & velocidade['baixa'], trafego['congestinado'])
regra4 = ctrl.Rule(quantidade['medio'] & velocidade['baixa'], trafego['moderado'])
regra5 = ctrl.Rule(quantidade['muitos'] & velocidade['media'], trafego['congestinado'])

# Sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
simulador = ctrl.ControlSystemSimulation(sistema_controle)

# Cenários de trafégo
cenarios = [
    {'quantidade': 30, 'velocidade': 60},
    {'quantidade': 80, 'velocidade': 40},
    {'quantidade': 200, 'velocidade': 10},
    {'quantidade': 150, 'velocidade': 20}
]

# Calculo dos resultados para cada cenário
for i, cenario in enumerate(cenarios, 1):
    print(f"\nCenário {i}: {cenario['quantidade']} carros, {cenario['velocidade']} km/h")
    
    # Definir entradas
    simulador.input['quantidade'] = cenario['quantidade']
    simulador.input['velocidade'] = cenario['velocidade']
    
    # Computar o resultado
    simulador.compute()
    
    # 4. Resultados numéricos que representa o nível do tráfego (defuzzicação)
    nivel_trafego = simulador.output['trafego']
    print(f"Nível de tráfego (valor numérico): {nivel_trafego:.2f}")
