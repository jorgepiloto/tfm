from astropy import units as u
from astropy.time import Time
from matplotlib import pyplot as plt
import numpy as np

from poliastro.bodies import Earth, Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range


def solve_porkchop(prograde):
    N = 75
    launch_span = time_range("2016-01-01", end="2028-01-01", num_values=N, scale="tdb")
    arrival_span = time_range("2032-01-01", end="2035-01-01", num_values=N, scale="tdb")

    borisov_ephem = Ephem.from_horizons("C/2019 Q4", launch_span)
    borisov = Orbit.from_ephem(Sun, borisov_ephem, Time("2016-01-01", scale="tdb"))

    return PorkchopPlotter(
        Earth, borisov, launch_span, arrival_span, prograde=prograde
    )

def solve_launch_energy():
    for prograde in [True, False]:
        porkchop = solve_porkchop(prograde)
        inclination = "prograde" if prograde else "retrograde"
        _, ax = plt.subplots(1, 1, figsize=(16, 8))
        porkchop.plot_launch_energy(
            levels=np.linspace(0, 12e3, 13) * u.km ** 2 / u.s ** 2,
            plot_contour_lines=False,
            ax=ax,
        )
        porkchop.plot_time_of_flight(
            levels=np.linspace(0, 20, 21) * u.year,
            ax=ax
        )
        porkchop.ax.set_title(f"Launch energy $C_3$ for Earth - 2I/Borisov\nDirect {inclination} transfer between 2016 and 2032")
        plt.savefig(f"fig/static/borisov/direct-{inclination}-transfer-porkchop.png", bbox_inches="tight")
        #porkchop.show()

if __name__ == "__main__":
    solve_launch_energy()
