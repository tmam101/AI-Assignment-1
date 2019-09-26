from KenKenSolver import KenKenSolver
import time

kenken = KenKenSolver()
kenken.get_input()
# start_time = time.time()
# kenken.backtrack(0)
# print("--- %s seconds ---" % (time.time() - start_time))
kenken.localSearch()
# kenken.bestBacktracking(0)
