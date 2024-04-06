import random

class Ant:
  def __init__(self, origin, destination, pheromone_table, distance_table):
    self.origin = origin
    self.destination = destination
    self.current_node = origin
    self.memory = {}
    self.pheromone_table = pheromone_table
    self.distance_table = distance_table

  def move(self):
    # Calculate the probabilities of moving to each neighbor.
    neighbors = self.get_neighbors()
    probabilities = []
    for neighbor in neighbors:
      pheromone = self.pheromone_table[self.current_node][neighbor]
      distance = self.distance_table[self.current_node][neighbor]
      probability = pheromone / distance
      probabilities.append(probability)

    # Choose the next node to move to.
    next_node = random.choices(neighbors, probabilities)[0]

    # Update the memory.
    self.memory[self.current_node] = self.pheromone_table[self.current_node][next_node]

    # Move to the next node.
    self.current_node = next_node

  def get_neighbors(self):
    neighbors = []
    for i in range(len(self.pheromone_table)):
      if self.pheromone_table[self.current_node][i] > 0:
        neighbors.append(i)
    return neighbors

  def is_at_destination(self):
    return self.current_node == self.destination


class AntColonyOptimization:
  def __init__(self, number_of_ants, pheromone_table, distance_table, evaporation_rate, alpha, beta):
    self.number_of_ants = number_of_ants
    self.pheromone_table = pheromone_table
    self.distance_table = distance_table
    self.evaporation_rate = evaporation_rate
    self.alpha = alpha
    self.beta = beta

  def solve(self):
    # Initialize the ants.
    ants = []
    for i in range(self.number_of_ants):
      ant = Ant(0, 1, self.pheromone_table, self.distance_table)
      ants.append(ant)

    # Iterate until all ants have reached their destination.
    while not all(ant.is_at_destination() for ant in ants):
      # Move each ant.
      for ant in ants:
        ant.move()

    # Update the pheromone table.
    for ant in ants:
      for i in range(len(self.pheromone_table)):
        for j in range(len(self.pheromone_table)):
          if i != j:
            self.pheromone_table[i][j] *= (1 - self.evaporation_rate)
            self.pheromone_table[i][j] += ant.memory[i]

    # Return the best solution.
    best_solution = None
    for ant in ants:
      if best_solution is None or ant.memory[0] < best_solution:
        best_solution = ant.memory[0]
    return best_solution

def main():
  # Example usage.
  pheromone_table = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  distance_table = [[1, 2, 3],
                     [4, 5, 6],
                       [7, 8, 9]]

  aco = AntColonyOptimization(10, pheromone_table, distance_table, 0.1, 1, 1)
  solution = aco.solve()

  print(solution)

if __name__ == "__main__":
  main()

# A solução do algo
