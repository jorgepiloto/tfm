from astropy import units as u
from astropy.time import Time
from matplotlib import pyplot as plt
from labellines import labelLines
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
    launch_span = time_range("2016-10-01", end="2017-10-01", num_values=N, scale="tdb")
    arrival_span = time_range("2017-09-12", end="2018-01-15", num_values=N, scale="tdb")

    # Load the ephemerides for the Earth and 'Oumuamua
    earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
    oumuamua = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)

    # Compute the escape velocity
    escape_velocity = 11.2 * u.km / u.s

    # Compute the porkchop plot
    return PorkchopPlotter(
        earth, oumuamua, launch_span, arrival_span, prograde=prograde, escape_velocity=escape_velocity
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
        levels=[0, 200, 250, 300, 350, 400, 450, 500, 600, 650] * u.km ** 2 / u.s ** 2,
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
        levels=[0, 200, 250, 300, 350, 400, 450, 500, 600, 650] * u.km ** 2 / u.s ** 2,
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
    discovery_line = porkchop.ax.axvline(x=discovery.to_datetime(),
                                         color='black', linewidth=3,
                                         label="Discovery of Oumuamua")
    labelLines([discovery_line], align=True, fontsize=14, backgroundcolor="white")
    plt.savefig(f"fig/static/oumuamua/direct-detailed-porkchop-avl.png", bbox_inches="tight")

    # Compute optimum transfer orbit
    earth_ephem = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
    oumuamua_ephem = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)

    # Define the desired times
    at_launch = porkchop.launch_date_at_c3_launch_min
    at_arrival = porkchop.arrival_date_at_c3_launch_min
    epochs = time_range(at_launch, end=at_arrival, num_values=1000, scale="tdb")

    # Build associated orbits
    earth = Orbit.from_ephem(Sun, earth_ephem, epoch=at_launch)
    oumuamua = Orbit.from_ephem(Sun, oumuamua_ephem, epoch=at_arrival)

    # Compute the transfer maneuver
    lambert = Maneuver.lambert(earth, oumuamua)
    print(f"Total cost: {lambert.get_total_cost():.2f}")
    print(f"Total time: {lambert.get_total_time().to(u.day):.2f}")
    for _, dv in lambert.impulses:
        print(f"Impulses: {dv.to(u.km / u.s)}")
        print(f"Cost: {(sum(impulse ** 2 for impulse in dv) ** 0.5).to(u.km/u.s):.2f}")
    transfer, _ = earth.apply_maneuver(lambert, intermediate=True)

    # Model the transfer orbit as an ephem
    transfer_ephem = transfer.to_ephem(strategy=EpochsArray(epochs))

    view_and_limits = {
        "xy": [[-2, 2], [-2, 2]],
        "xz": [[-1.5, 1.5], [-0.5, 1]],
        "yz": [[-1.5, 1.5], [-0.5, 1]],
    }

    for view, (xlim, ylim) in view_and_limits.items():
        plotter = plot_solar_system(epoch=at_launch, outer=False,
                                    length_scale_units=u.AU,
                                    plane=Planes.EARTH_ECLIPTIC, view=view)
        plotter.plot_ephem(transfer_ephem, label="Transfer orbit", color="red")
        oumuamua_lines, _ = plotter.plot_coordinates(oumuamua_ephem.sample(epochs), position=oumuamua_ephem.rv(at_arrival)[0], label="1I/'Oumuamua at arrival", color="black")
        oumuamua_lines.set_linestyle("--")

        plotter.backend.ax.set_xlim(xlim)
        plotter.backend.ax.set_ylim(ylim)
        if view != "xy":
            plotter.backend.ax.legend().remove()
        plt.savefig(f"fig/static/oumuamua/direct-optimum-transfer-{view}.png", bbox_inches="tight")

if __name__ == "__main__":
    main()
