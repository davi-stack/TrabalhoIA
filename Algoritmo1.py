import random
import numpy as np






class AntColony:
    #numero de cidades, nivel de feromonio, taxa de evaporação, alpha, beta, Q, numero de formigas, numero de iterações
    # Q é a quantidade de feromônio depositado por cada formiga
    # alpha e beta são parâmetros que controlam a importância do feromônio e da distância, respectivamente
    # alpha = 1.0 e beta = 2.0 são valores comuns
    # evaporação do feromônio é um processo que ocorre em cada iteração, onde uma fração do feromônio é removida de todas as arestas
    def __init__(self, num_cities, pheromone_level=1.0, evaporation_rate=0.1, alpha=1.0, beta=2.0, Q=1.0, num_ants=10, iterations=100):
        self.num_cities = num_cities
        self.pheromone_level = pheromone_level
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.num_ants = num_ants
        self.iterations = iterations

        # Inicialização da matriz de distâncias e matriz de feromônio
        self.distance_matrix = np.zeros((num_cities, num_cities))
        self.pheromone_matrix = np.ones((num_cities, num_cities)) * pheromone_level

        # Melhor tour encontrado
        self.best_tour_length = float('inf')
        self.best_tour = []

    def set_distance_matrix(self, distances):
        self.distance_matrix = np.array(distances)

    def initialize_ants(self):
        #array de formigas, criada com uma quantidade num_ants(10) de formigas, que começa em um lugar aleatório e tamanho de percorrido tour 0
        self.ants = [{'tour': [random.randint(0, self.num_cities - 1)], 'tour_length': 0.0} for _ in range(self.num_ants)]
    
    def move_ants(self):
        for ant in self.ants:
            #O [False]*num_cities cria um array de booleanos com o tamanho de num_cities, onde todos os valores são False
            visited = [False] * self.num_cities
            #A cidade inicial é visitada
            visited[ant['tour'][0]] = True

            for _ in range(self.num_cities - 1):
                current_city = ant['tour'][-1]
                next_city = self.select_next_city(ant, visited)
                ant['tour'].append(next_city)
                ant['tour_length'] += self.distance_matrix[current_city][next_city]
                visited[next_city] = True

            # Atualizar o comprimento do tour para incluir o retorno à cidade inicial
            ant['tour_length'] += self.distance_matrix[ant['tour'][-1]][ant['tour'][0]]

    def select_next_city(self, ant, visited):
        current_city = ant['tour'][-1]
        total_probability = 0.0
        probabilities = [0.0] * self.num_cities

        for i in range(self.num_cities):
            if not visited[i]:
                # Cálculo da probabilidade de ir para a cidade i
                probabilities[i] = (self.pheromone_matrix[current_city][i] ** self.alpha) * (1.0 / self.distance_matrix[current_city][i] ** self.beta)
                total_probability += probabilities[i]

        # Escolha da próxima cidade baseada nas probabilidades calculadas
        random_value = random.uniform(0, total_probability)
        cumulative_probability = 0.0
        for i in range(self.num_cities):
            if not visited[i]:
                cumulative_probability += probabilities[i]
                if cumulative_probability >= random_value:
                    return i

    def update_pheromone(self):
        # Evaporação do feromônio
        self.pheromone_matrix *= (1.0 - self.evaporation_rate)

        # Atualização do feromônio depositado pelas formigas
        for ant in self.ants:
            for i in range(self.num_cities - 1):
                city1, city2 = ant['tour'][i], ant['tour'][i + 1]
                self.pheromone_matrix[city1][city2] += self.Q / ant['tour_length']
                self.pheromone_matrix[city2][city1] += self.Q / ant['tour_length']

    def solve(self):
        for _ in range(self.iterations):
            self.initialize_ants()
            self.move_ants()
            self.update_pheromone()

            # Verificação do melhor tour encontrado até o momento
            for ant in self.ants:
                if ant['tour_length'] < self.best_tour_length:
                    self.best_tour_length = ant['tour_length']
                    self.best_tour = ant['tour']

        return self.best_tour, self.best_tour_length

# Exemplo de uso
if __name__ == "__main__":

    # Definição das distâncias entre as cidades
    # distances = [
    #     [0, 10, 15, 20],
    #     [10, 0, 35, 25],
    #     [15, 35, 0, 30],
    #     [20, 25, 30, 0]
    # ]
    distances = [
        [0, 7, 9, 16, 13, 14, 27, 3],
        [7, 0, 10, 17, 14, 15, 28, 4],
        [9, 10, 0, 7, 6, 7, 20, 6],
        [16, 17, 7, 0, 7, 6, 19, 13],
        [13, 14, 6, 7, 0, 1, 14, 10],
        [14, 15, 7, 6, 1, 0, 13, 9],
        [27, 28, 20, 19, 14, 13, 0, 24],
        [3, 4, 6, 13, 10, 9, 24, 0]
    ]
    num_cities = len(distances)
    ant_colony = AntColony(num_cities)
    ant_colony.set_distance_matrix(distances)
    best_tour, best_tour_length = ant_colony.solve()

    print("Melhor tour encontrado:", best_tour)
    print("Comprimento do melhor tour:", best_tour_length)
    