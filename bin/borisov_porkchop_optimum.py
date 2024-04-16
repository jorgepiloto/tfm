from astropy import units as u
from matplotlib import pyplot as plt
import numpy as np

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range


def solve_porkchop(prograde=True):
    # Declare the launch and arrival spans
    N = 200
    launch_span = time_range("2018-03-01", end="2018-12-01", num_values=N, scale="tdb")
    arrival_span = time_range("2019-05-01", end="2020-03-01", num_values=N, scale="tdb")

    # Load the ephemerides for the Earth and 'Oumuamua
    earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
    borisov = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the porkchop plot
    return PorkchopPlotter(
        earth, borisov, launch_span, arrival_span, prograde=prograde
    )

def main():
    # Compute the porkchop plot
    porkchop = solve_porkchop(prograde=True)

    # Get launch energy and time of flight
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 25**2, 11) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_time_of_flight(
        levels=np.linspace(100, 700, 7) * u.day,
        ax=ax
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and time of flight\nEarth - 2I/Borisov direct and prograde transfers between 2016 and 2019")
    plt.savefig(f"fig/static/borisov/direct-detailed-porkchop-tof.png", bbox_inches="tight")

    # Get launch energy and arrival velocity
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 25**2, 11) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_arrival_velocity(
        levels=np.linspace(30, 40, 3) * u.km / u.s,
        ax=ax
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and arrival velocity\nEarth - 2I/Borisov direct and prograde transfers between 2016 and 2032")
    plt.savefig(f"fig/static/borisov/direct-detailed-porkchop-avl.png", bbox_inches="tight")


if __name__ == "__main__":
    main()
