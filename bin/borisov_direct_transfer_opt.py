from astropy import units as u
from astropy.time import Time
import matplotlib.pyplot as plt

from poliastro.frames import Planes
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from poliastro.twobody.sampling import EpochsArray
from poliastro.maneuver import Maneuver
from poliastro.ephem import Ephem
from poliastro.plotting.misc import plot_solar_system
from poliastro.util import time_range


# Build the ephemerides
earth_ephem = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
borisov_ephem = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)

# Define the desired times
at_launch = Time("2018-07-11", scale="tdb")
at_arrival = Time("2019-10-27", scale="tdb")
epochs = time_range(at_launch, end=at_arrival, num_values=1000, scale="tdb")

# Build associated orbits
earth = Orbit.from_ephem(Sun, earth_ephem, epoch=at_launch)
borisov = Orbit.from_ephem(Sun, borisov_ephem, epoch=at_arrival)

# Compute the transfer maneuver
lambert = Maneuver.lambert(earth, borisov)
print(f"Total cost: {lambert.get_total_cost()}")
print(f"Total time: {lambert.get_total_time().to(u.day)}")
for _, dv in lambert.impulses:
    print(f"Impulses: {dv.to(u.km / u.s)}")
    print(f"Cost: {(sum(impulse ** 2 for impulse in dv) ** 0.5).to(u.km/u.s)}")
transfer, _ = earth.apply_maneuver(lambert, intermediate=True)

# Model the transfer orbit as an ephem
transfer_ephem = transfer.to_ephem(strategy=EpochsArray(epochs))

view_and_limits = {
    "xy": [[-3, 3], [-3, 3]],
    "xz": [[-0.2, 3], [-0.2, 1]],
    "yz": [[-0.2, 3], [-0.2, 1]],
}

for view, (xlim, ylim) in view_and_limits.items():
    plotter = plot_solar_system(epoch=at_launch, outer=False,
                                length_scale_units=u.AU,
                                plane=Planes.EARTH_ECLIPTIC, view=view)
    plotter.plot_ephem(transfer_ephem, label="Transfer orbit", color="red")
    oumuamua_lines, _ = plotter.plot_coordinates(borisov_ephem.sample(epochs),
                                                 position=borisov_ephem.rv(at_arrival)[0],
                                                 label="2I/Borisov at arrival", color="black")
    oumuamua_lines.set_linestyle("--")

    plotter.backend.ax.set_xlim(xlim)
    plotter.backend.ax.set_ylim(ylim)
    if view != "xy":
        plotter.backend.ax.legend().remove()

    plt.savefig(f"fig/static/borisov/direct-optimum-transfer-{view}.png", bbox_inches="tight")
