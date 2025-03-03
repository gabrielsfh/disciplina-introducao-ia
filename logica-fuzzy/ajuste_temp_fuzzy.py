import numpy as np
import skfuzzy as fuzz

# Universo de saída (temperaturas possíveis)
x_temp = np.arange(10, 31, 1)

# Conjuntos fuzzy
frio = fuzz.trimf(x_temp, [10, 15, 20]) # min, centróide, max
morno = fuzz.trimf(x_temp, [18, 22, 25])
quente = fuzz.trimf(x_temp, [22, 28, 30])

# Graus de pertencimento para 20°C, verificar os valores de pertencimentos para escolher os centroides
pert_frio = fuzz.interp_membership(x_temp, frio, 20)  # 0.3
pert_morno = fuzz.interp_membership(x_temp, morno, 20) # 0.7
pert_quente = fuzz.interp_membership(x_temp, quente, 20) # 0.0

# Definição dos graus de pertencimento e valores centrais (hardcoded)
valores = np.array([15, 22])  # Convertido para array NumPy
pertinencias = np.array([pert_frio, pert_morno])  # Convertido para array NumPy

# Deffuzificação
# Aplicando a fórmula do centro de gravidade (centroid)
resultado_defuzz = fuzz.defuzz(valores, pertinencias, 'centroid')
print(f"Temperatura ajustada: {resultado_defuzz:.2f}°C")
