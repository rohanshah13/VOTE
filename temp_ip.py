import numpy as np
import pandas as pd
import os
import argparse
import json
from ortools.linear_solver import pywraplp

def main():
	solver = pywraplp.Solver.CreateSolver('SCIP')
	
	x = solver.IntVar(0,1,'temp')

	constraint = solver.RowConstraint(0,2,'')

	constraint.SetCoefficient(x,3)

	objective = solver.Objective()
	objective.SetCoefficient(x,5)

	objective.SetMaximization()

	status = solver.Solve()

	if status == pywraplp.Solver.OPTIMAL:
		print('Objective Value = ', solver.Objective().Value())



if __name__ == '__main__':
	main()