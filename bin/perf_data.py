""" Computes the iteration workload for each solver. """

PERFORMANCE_DICTIONARY = {
        "gauss1809": [10.96, 652.24, 8752.05],
        "battin1984": [3.82, 96.34, 769.49],
        "gooding1990": [2.67, 27.92, 771.92],
        "avanzini2008": [4.65, 168.64, 2735.59],
        "arora2013": [2.14, 41.94, 570.63],
        "vallado2013": [24.32, 54.31, 1632.27],
        "izzo2015": [2.33, 47.51, 444.62],
}

for solver_name in PERFORMANCE_DICTIONARY:

    # Unpack the data
    numiter_mean, tpi_mean, tct_mean = PERFORMANCE_DICTIONARY[solver_name]

    # Compute the iteration workload
    iter_workload = numiter_mean * tpi_mean / tct_mean * 100
    print(f"{solver_name.capitalize()} = {iter_workload:.2f}")
