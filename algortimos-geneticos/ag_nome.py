import random 

class Individuo():
    def __init__(self, geracao = 0):
        self.fitness: int = 0
        self.geracao: int = geracao
        self.cromossomo: list = []

        for i in range(len(target)):
            self.cromossomo.append(random.choice(chars))
        
    def avaliacao(self):
        valor = 0 

        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == target[i]:
                valor += 1
        
        self.fitness = valor
    
    def crossover(self, outro_individuo):
        ponto_corte = round(random.random() * len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:ponto_corte] + self.cromossomo[ponto_corte::]
        filho2 = self.cromossomo[0:ponto_corte] + outro_individuo.cromossomo[ponto_corte::]

        filhos = [Individuo(self.geracao +1), Individuo(self.geracao + 1)]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2

        return filhos

    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random.random() < taxa_mutacao:
                self.cromossomo[i] = random.choice(chars)

        return self


class AlgoritmoGenetico():
    
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
    
    def InicializaPopulacao(self):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo())
        
        self.melhor_solucao = self.populacao[0]
        self.melhor_pai = self.populacao[0]
    
    def ordenaPop(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.fitness,
                                reverse = True)
    
    def melhorIndividuo(self, individuo):
        if individuo.fitness > self.melhor_solucao.fitness:
            self.melhor_solucao = individuo
    
    def somaFitness(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.fitness
        
        return soma 

    def selecionaPai(self, somaFitness):
        pai = -1
        valor_sorteado = random.random() * somaFitness
        soma = 0 
        i = 0

        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].fitness
            pai += 1
            i += 1
        
        return pai

    def visualizaGeracao(self):
        melhor = self.populacao[0]
        print(f"Geração: {self.populacao[0].geracao} - Cromossomo: {''.join(melhor.cromossomo)} -  Valor: {melhor.fitness}")
    
    def resolver(self, taxa_mutacao, numero_geracoes):
        self.InicializaPopulacao()

        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordenaPop()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.fitness)

        self.visualizaGeracao()

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.somaFitness()
            nova_pop = []

            for individuo_gerado in range(0, self.tamanho_populacao, 2):
                pai1 = self.selecionaPai(soma_avaliacao)
                pai2 = self.selecionaPai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_pop.append(filhos[0].mutacao(taxa_mutacao))
                nova_pop.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_pop)

            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordenaPop()
            self.visualizaGeracao()

            melhor_encontrada = self.populacao[0]
            self.lista_solucoes.append(melhor_encontrada.fitness)

            self.melhorIndividuo(melhor_encontrada)
        
        print(f"Melhor solução -> Geração: {self.melhor_solucao.geracao} - Fitness: {self.melhor_solucao.fitness} - Cromossomo: {''.join(self.melhor_solucao.cromossomo)}")


        print(f"Nome final: {''.join(self.melhor_solucao.cromossomo)}")

if __name__=="__main__":
    chars: str = "abcdefghihgjlmnopqtrstyuizx"
    target: str = "Gabriel"
    taxa_mutacao = 0.01
    geracoes = 100
    tam_pop = 100
    ag = AlgoritmoGenetico(tam_pop)

    ag.resolver(taxa_mutacao, geracoes)