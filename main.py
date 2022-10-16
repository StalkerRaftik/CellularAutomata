from src.automaton import Automaton
from src.algorithms import LifeGame, LifeGameWithoutDeath, LifeGameWithoutDeath2

if __name__ == '__main__':
    automaton_algorithm = LifeGame()

    automaton = Automaton(cell_count=300, max_fps=60)
    automaton.init_pygame()
    automaton.set_algorithm(automaton_algorithm)
    automaton.start()
