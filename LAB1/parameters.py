import numpy as np

window_dim = 1000
x_coord = 0
y_coord = 1
z_coord = 2
object_file = "files/f16.obj"
verticies_file = "files/verticies.obj"
dot_number = 10
scale = 5
N_cubbic_coeff = 1/6 * np.array([[-1, 3, -3, 1],
                                 [3, -6, 3, 0],
                                 [-3, 0, 3, 0],
                                 [1, 4, 1, 0]])
t_cubbic_coeff = lambda t: np.array([t**3, t**2, t, 1])
matrix_deriv_coeff = lambda t: np.array([3*t**2, 2*t, 1, 0])
s_vec = np.array([0, 0, 1])

p_t_derivative = lambda t: np.array([t**2, t, 1])
N_cubbic_coeff_derivative = \
    1/2 * np.array([[-1, 3, -3, 1],
                    [2, -4, 2, 0],
                    [-1, 0, 1, 0]])
