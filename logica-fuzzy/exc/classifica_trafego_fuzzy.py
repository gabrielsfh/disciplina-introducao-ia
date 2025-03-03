import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Variaveis de entrada
quantidade = ctrl.Antecedent(np.arange(0, 251, 1), 'quantidade')
velocidade = ctrl.Antecedent(np.arange(0, 121, 1), 'velocidade')

# Variaveis de saida
trafego = ctrl.Consequent(np.arange(0, 101, 1), 'trafego')

# 1. Determinando o grau de pertinência das entradas para cada conjunto fuzzy

# Quantidade de veículos
quantidade['poucos'] = fuzz.trimf(quantidade.universe, [0, 25, 75])
quantidade['medio'] = fuzz.trimf(quantidade.universe, [50, 125, 200])
quantidade['muitos'] = fuzz.trimf(quantidade.universe, [150, 200, 250])

# Velocidade média
velocidade['baixa'] = fuzz.trimf(velocidade.universe, [0, 10, 30])
velocidade['media'] = fuzz.trimf(velocidade.universe, [20, 50, 80])
velocidade['alta'] = fuzz.trimf(velocidade.universe, [50, 80, 120])

# Nível de tráfego
trafego['leve'] = fuzz.trimf(trafego.universe, [0, 15, 30])
trafego['moderado'] = fuzz.trimf(trafego.universe, [20, 40, 60])
trafego['congestinado'] = fuzz.trimf(trafego.universe, [50, 75, 100])

# 2. Regras fuzzy para inferir o nível de tráfego de cada cenário.
regra1 = ctrl.Rule(quantidade['poucos'] & velocidade['alta'], trafego['leve'])
regra2 = ctrl.Rule(quantidade['medio'] & velocidade['media'], trafego['moderado'])
regra3 = ctrl.Rule(quantidade['muitos'] & velocidade['baixa'], trafego['congestinado'])
regra4 = ctrl.Rule(quantidade['medio'] & velocidade['baixa'], trafego['moderado'])
regra5 = ctrl.Rule(quantidade['muitos'] & velocidade['media'], trafego['congestinado'])

# Sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
simulador = ctrl.ControlSystemSimulation(sistema_controle)

# Cenários de tráfego
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

# 3. Representando os conjuntos fuzzy em gráficos triangulares ou trapezoidais.
def plot_fuzzy_sets():
    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    
    axes[0].plot(quantidade.universe, quantidade['poucos'].mf, label='Poucos')
    axes[0].plot(quantidade.universe, quantidade['medio'].mf, label='Médio')
    axes[0].plot(quantidade.universe, quantidade['muitos'].mf, label='Muitos')
    axes[0].set_title('Quantidade de Veículos')
    axes[0].legend()
    
    axes[1].plot(velocidade.universe, velocidade['baixa'].mf, label='Baixa')
    axes[1].plot(velocidade.universe, velocidade['media'].mf, label='Média')
    axes[1].plot(velocidade.universe, velocidade['alta'].mf, label='Alta')
    axes[1].set_title('Velocidade Média')
    axes[1].legend()
    
    axes[2].plot(trafego.universe, trafego['leve'].mf, label='Leve')
    axes[2].plot(trafego.universe, trafego['moderado'].mf, label='Moderado')
    axes[2].plot(trafego.universe, trafego['congestinado'].mf, label='Congestionado')
    axes[2].set_title('Nível de Tráfego')
    axes[2].legend()
    
    plt.get_current_fig_manager().set_window_title('Conjuntos fuzzy')
    plt.tight_layout()
    
    # Salvando e mostrando o gráfico
    plt.savefig('fuzzy_sets.png')  
    plt.show()

plot_fuzzy_sets()
