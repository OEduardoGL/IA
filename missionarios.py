class State:
    def __init__(self, missionaries_left, cannibals_left, boat_on_left, previous=None): 
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_on_left = boat_on_left
        self.previous = previous
        # previous = estado anterior que levou a esse estado

# Método para verificar se dois estados são iguais
    def __eq__(self, other):
        return (self.missionaries_left == other.missionaries_left and
                self.cannibals_left == other.cannibals_left and
                self.boat_on_left == other.boat_on_left)

# Metodo para verificar se o estado é valido. (de modo que os canibais não comam os missionários)
    def is_valid(self):
        if self.missionaries_left < 0 or self.cannibals_left < 0 or self.missionaries_left > 3 or self.cannibals_left > 3:
            return False
        if (self.missionaries_left > 0 and self.missionaries_left < self.cannibals_left) or (self.missionaries_left < 3 and self.missionaries_left > 3 - self.cannibals_left):
            return False
        return True

# Método para gerar todos os estados possíveis a partir do estado atual
    def generate_successors(self):
        if self.boat_on_left:
            for i in range(3):
                for j in range(3):
                    if i + j > 0 and i + j < 3:
                        new_state = State(self.missionaries_left - i, self.cannibals_left - j, False, self)
                        if new_state.is_valid():
                            yield new_state
        else:
            for i in range(3):
                for j in range(3):
                    if i + j > 0 and i + j < 3:
                        new_state = State(self.missionaries_left + i, self.cannibals_left + j, True, self)
                        if new_state.is_valid():
                            yield new_state

#   Busca em Largura
def bfs(start, goal):
    queue = []
    visited_states = []
    queue.append(start)
    while queue:
        current_state = queue.pop(0)
        if current_state == goal:
            return current_state
        for successor in current_state.generate_successors():
            if not any(successor == state for state in queue) and not any(successor == state for state in visited_states):
                queue.append(successor)
                successor.previous = current_state
                visited_states.append(successor)
    return None

def main():
    start = State(3, 3, True)
    goal = State(0, 0, False)
    solution = bfs(start, goal)
    if solution is None:
        print("Nenhuma solução encontrada.")
        return
    path = []
    while solution:
        path.append(solution)
        solution = solution.previous
    path.reverse()
    for state in path:
        print("Missionários na margem á esquerda: {}\nCanibais na margem á esquerda: {}\nBarco na margem á esquerda: {}\n".format(state.missionaries_left, state.cannibals_left, state.boat_on_left))

if __name__ == "__main__":
    main()