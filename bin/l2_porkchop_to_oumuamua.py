from astropy import units as u
from astropy.time import Time
from matplotlib import pyplot as plt
import numpy as np

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range


def solve_porkchop(prograde=True):
    # Declare the launch and arrival spans
    N = 250
    launch_span = time_range("2016-01-01", end="2028-01-01", num_values=N, scale="tdb")
    arrival_span = time_range("2017-01-01", end="2035-01-01", num_values=N, scale="tdb")

    # Load the ephemerides for the Earth and 'Oumuamua
    l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
    oumuamua = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the porkchop plot
    return PorkchopPlotter(
        l2, oumuamua, launch_span, arrival_span, prograde=prograde
    )

def solve_launch_energy(porkchop, inclination):
    porkchop = solve_porkchop(prograde)
    inclination = "prograde" if prograde else "retrograde"
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 10e3, int(1001)) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=False,
        ax=ax,
    )
    porkchop.c3_colorbar.set_ticks(np.linspace(0, 10e3, 11).astype(int))
    porkchop.c3_colorbar.set_ticklabels(np.linspace(0, 10e3, 11).astype(int))
    porkchop.plot_time_of_flight(
        levels=[1, 2, 5, 10, 15] * u.year,
        ax=ax,
        use_years=True,
    )
    porkchop.ax.set_title(f"Launch energy $C_3$ and time of flight\nEarth - 1I/'Oumuamua direct and {inclination} transfers between 2016 and 2028")
    #plt.savefig(f"fig/static/oumuamua/direct-{inclination}-transfer-porkchop.png", bbox_inches="tight")
    plt.show()

def solve_arrival_velocity(porkchop, inclination):
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 10e3, int(1001)) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=False,
        ax=ax,
    )
    porkchop.c3_colorbar.set_ticks(np.linspace(0, 10e3, 11).astype(int))
    porkchop.c3_colorbar.set_ticklabels(np.linspace(0, 10e3, 11).astype(int))
    porkchop.plot_arrival_velocity(
        levels=[2, 6, 10, 15, 20, 30, 60] * u.km / u.s,
        ax=ax
    )
    porkchop.ax.set_title(f"Launch energy $C_3$ and arrival velocity\nEarth - 1I/'Oumuamua direct and {inclination} transfers between 2016 and 2028")
    #plt.savefig(f"fig/static/oumuamua/direct-{inclination}-transfer-porkchop-avl.png", bbox_inches="tight")


if __name__ == "__main__":
    for prograde in [True, False]:
        porkchop = solve_porkchop(prograde)
        inclination = "prograde" if prograde else "retrograde"
        solve_launch_energy(porkchop, inclination)
        solve_arrival_velocity(porkchop, inclination)
