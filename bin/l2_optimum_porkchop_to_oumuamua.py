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
    launch_span = time_range("2016-10-01", end="2017-10-01", num_values=N, scale="tdb")
    arrival_span = time_range("2017-09-12", end="2018-04-01", num_values=N, scale="tdb")

    # Load the ephemerides for the Earth and 'Oumuamua
    l2 = Ephem.from_csv("bin/ephem/semb-l4.csv", plane=Planes.EARTH_ECLIPTIC)
    oumuamua = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the porkchop plot
    return PorkchopPlotter(
        l2, oumuamua, launch_span, arrival_span, prograde=prograde
    )

def main():
    # Compute the porkchop plot
    porkchop = solve_porkchop(prograde=True)

    print(f"Minimum energy: {porkchop.c3_launch_min:.2f}")
    print(f"Launch date: {porkchop.launch_date_at_c3_launch_min}")
    print(f"Arrivla date: {porkchop.arrival_date_at_c3_launch_min}")

    # Get launch energy and time of flight
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 25**2, 11) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_time_of_flight(
        levels=np.linspace(100, 700, 7) * u.day,
        ax=ax,
        use_years=False,
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and time of flight\nEarth - 1I/'Oumuamua direct and prograde transfers between 2016 and 2019")
    porkchop.ax.plot(
            porkchop.launch_date_at_c3_launch_min.to_datetime(),
            porkchop.arrival_date_at_c3_launch_min.to_datetime(),
            "ko", markersize=15
    )
    porkchop.ax.plot(
            porkchop.launch_date_at_c3_launch_min.to_datetime(),
            porkchop.arrival_date_at_c3_launch_min.to_datetime(),
            color="red", marker="x", mew=2, label="Lowest energy transfer"
    )
    discovery = Time("2017-10-19", scale="tdb")
    discovery_line = porkchop.ax.axvline(x=discovery.to_datetime(),
                                         color='black', linewidth=3,
                                         label="Discovery of Oumuamua")
    labelLines([discovery_line], align=True, fontsize=14, backgroundcolor="white")
    plt.savefig(f"fig/static/oumuamua/direct-detailed-porkchop-tof.png", bbox_inches="tight")

    # Get launch energy and arrival velocity
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=np.linspace(0, 25**2, 11) * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_arrival_velocity(
        levels=[20, 25, 30, 35] * u.km / u.s,
        ax=ax
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and arrival velocity\nEarth - 1I/'Oumuamua direct and prograde transfers between 2016 and 2032")
    porkchop.ax.plot(
            porkchop.launch_date_at_c3_launch_min.to_datetime(),
            porkchop.arrival_date_at_c3_launch_min.to_datetime(),
            "ko", markersize=15
    )
    porkchop.ax.plot(
            porkchop.launch_date_at_c3_launch_min.to_datetime(),
            porkchop.arrival_date_at_c3_launch_min.to_datetime(),
            color="red", marker="x", mew=2, label="Lowest energy transfer"
    )
    #plt.savefig(f"fig/static/oumuamua/direct-detailed-porkchop-avl.png", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
