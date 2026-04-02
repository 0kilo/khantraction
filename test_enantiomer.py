import numpy as np
from analysis.phase_g.phase_g_chirality_analysis import PhaseGChiralitySolver

solver = PhaseGChiralitySolver()
# Right-Handed
sol1 = solver.solve(0.5, np.pi/8, np.pi/8, np.pi/8)
m1 = sol1.y[8, -1]
chi1 = solver.get_chirality_density(np.pi/8, np.pi/8, np.pi/8)

# Left-Handed (phi -> phi + pi/2)
sol2 = solver.solve(0.5, np.pi/8, np.pi/8 + np.pi/2, np.pi/8)
m2 = sol2.y[8, -1]
chi2 = solver.get_chirality_density(np.pi/8, np.pi/8 + np.pi/2, np.pi/8)

print(f"Right-Handed: mass={m1}, chi={chi1}")
print(f"Left-Handed: mass={m2}, chi={chi2}")
