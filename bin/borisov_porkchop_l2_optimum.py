from astropy import units as u
from matplotlib import pyplot as plt
import numpy as np

from poliastro.bodies import Sun
from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.frames import Planes
from poliastro.twobody.sampling import EpochsArray
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range
from poliastro.maneuver import Maneuver
from poliastro.plotting.misc import plot_solar_system


def solve_porkchop(prograde=True):
    # Declare the launch and arrival spans
    N = 200
    launch_span = time_range("2018-04-01", end="2018-10-01", num_values=N, scale="tdb")
    arrival_span = time_range("2019-09-01", end="2020-01-01", num_values=N, scale="tdb")

    # Load the ephemerides for the L2 and 'Oumuamua
    l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
    borisov = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the escape velocity
    escape_velocity = 0.73 * u.km / u.s

    # Compute the porkchop plot
    return PorkchopPlotter(
        l2, borisov, launch_span, arrival_span, prograde=prograde, escape_velocity=escape_velocity
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
        levels=[0, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 650] * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_time_of_flight(
        levels=np.linspace(100, 700, 7) * u.day,
        ax=ax,
        use_years=False,
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and time of flight\nL2 - 1I/'Oumuamua direct and prograde optimum transfer")
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
    plt.savefig(f"fig/static/borisov/l2-direct-detailed-porkchop-tof.png", bbox_inches="tight")
    plt.show()

    # Get launch energy and arrival velocity
    _, ax = plt.subplots(1, 1, figsize=(16, 8))
    porkchop.plot_launch_energy(
        levels=[0, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 650] * u.km ** 2 / u.s ** 2,
        plot_contour_lines=True,
        ax=ax,
    )
    porkchop.plot_arrival_velocity(
        levels=[20, 25, 30, 35] * u.km / u.s,
        ax=ax
    )
    porkchop.ax.set_title(f"Detailed launch energy $C_3$ and arrival velocity\nL2 - 1I/'Oumuamua direct and prograde optimum transfer")
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
    plt.savefig(f"fig/static/borisov/l2-direct-detailed-porkchop-avl.png", bbox_inches="tight")
    plt.show()

    # Compute optimum transfer orbit
    l2_ephem = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
    borisov_ephem = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)

    # Define the desired times
    at_launch = porkchop.launch_date_at_c3_launch_min
    at_arrival = porkchop.arrival_date_at_c3_launch_min
    epochs = time_range(at_launch, end=at_arrival, num_values=1000, scale="tdb")

    # Build associated orbits
    l2 = Orbit.from_ephem(Sun, l2_ephem, epoch=at_launch)
    borisov = Orbit.from_ephem(Sun, borisov_ephem, epoch=at_arrival)

    # Compute the transfer maneuver
    lambert = Maneuver.lambert(l2, borisov)
    print(f"Total cost: {lambert.get_total_cost():.2f}")
    print(f"Total time: {lambert.get_total_time().to(u.day):.2f}")
    for _, dv in lambert.impulses:
        print(f"Impulses: {dv.to(u.km / u.s)}")
        print(f"Cost: {(sum(impulse ** 2 for impulse in dv) ** 0.5).to(u.km/u.s):.2f}")
    transfer, _ = l2.apply_maneuver(lambert, intermediate=True)

    # Model the transfer orbit as an ephem
    transfer_ephem = transfer.to_ephem(strategy=EpochsArray(epochs))

    view_and_limits = {
        "xy": [[-3, 3], [-3, 3]],
        "xz": [[-0.8, 2.5], [-0.2, 1]],
        "yz": [[-1.6, 1.7], [-0.2, 1]],
    }

    for view, (xlim, ylim) in view_and_limits.items():
        plotter = plot_solar_system(epoch=at_launch, outer=False,
                                    length_scale_units=u.AU,
                                    plane=Planes.EARTH_ECLIPTIC, view=view)
        plotter.plot_ephem(transfer_ephem, label="Transfer orbit", color="red")
        borisov_lines, _ = plotter.plot_coordinates(borisov_ephem.sample(epochs),
                                 position=borisov_ephem.rv(at_arrival)[0],
                                 label="2I/Borisov at arrival", color="black")
        borisov_lines.set_linestyle("--")

        plotter.backend.ax.set_xlim(xlim)
        plotter.backend.ax.set_ylim(ylim)
        if view != "xy":
            plotter.backend.ax.legend().remove()
        plt.savefig(f"fig/static/borisov/l2-direct-optimum-transfer-{view}.png", bbox_inches="tight")
        plt.show()

if __name__ == "__main__":
    main()
