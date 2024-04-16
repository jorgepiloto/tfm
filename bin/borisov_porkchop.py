from astropy import units as u
from matplotlib import pyplot as plt
import numpy as np

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range


def solve_porkchop(prograde=True):
    # Declare the launch and arrival spans
    N = 150
    launch_span = time_range("2016-01-01", end="2028-01-01", num_values=N, scale="tdb")
    arrival_span = time_range("2032-01-01", end="2035-01-01", num_values=N, scale="tdb")

    # Load the ephemerides for the Earth and 'Oumuamua
    earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
    borisov = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the porkchop plot
    return PorkchopPlotter(
        earth, borisov, launch_span, arrival_span, prograde=prograde
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
        porkchop.ax.set_title(f"Launch energy $C_3$ and time of flight\nEarth - 2I/Borisov direct and {inclination} transfers between 2016 and 2032")
        plt.savefig(f"fig/static/borisov/direct-{inclination}-transfer-porkchop.png", bbox_inches="tight")

def solve_launch_velocity():
    for prograde in [True, False]:
        porkchop = solve_porkchop(prograde)
        inclination = "prograde" if prograde else "retrograde"
        _, ax = plt.subplots(1, 1, figsize=(16, 8))
        porkchop.plot_launch_energy(
            levels=np.linspace(0, 12e3, 13) * u.km ** 2 / u.s ** 2,
            plot_contour_lines=False,
            ax=ax,
        )
        porkchop.plot_arrival_velocity(
            levels=np.linspace(20, 50, 4) * u.km / u.s,
            ax=ax
        )
        porkchop.plot_arrival_velocity(
            levels=np.linspace(0, 15, 6) * u.km / u.s,
            ax=ax
        )
        porkchop.ax.set_title(f"Launch energy $C_3$ and arrival velocity\nEarth - 2I/Borisov direct and {inclination} transfers between 2016 and 2032")
        plt.savefig(f"fig/static/borisov/direct-{inclination}-transfer-porkchop-avl.png", bbox_inches="tight")

if __name__ == "__main__":
    solve_launch_energy()
    solve_launch_velocity()
