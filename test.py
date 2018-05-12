from builder import Builder
from solver import Solver
print("Initial Solution ")

newbuilder = Builder()
newbuilder.display()
print("Actual  Puzzle||| Note:Might have multiple solutions")

newbuilder.build_puzzle()
newbuilder.display()

print("Solved Solution:")

solver = Solver(newbuilder)
solver.display()

