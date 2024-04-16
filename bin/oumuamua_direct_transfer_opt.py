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
oumuamua_ephem = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)

# Define the desired times
#at_launch = Time("2016-02-28 19:58:23", scale="tdb")
#at_arrival = Time("2032-02-06 18:41:04", scale="tdb")
at_launch = Time("2017-08-15", scale="tdb")
at_arrival = Time("2032-05-13", scale="tdb")
epochs = time_range(at_launch, end=at_arrival, num_values=1000, scale="tdb")

# Build associated orbits
earth = Orbit.from_ephem(Sun, earth_ephem, epoch=at_launch)
oumuamua = Orbit.from_ephem(Sun, oumuamua_ephem, epoch=at_arrival)

# Compute the transfer maneuver
lambert = Maneuver.lambert(earth, oumuamua)
transfer, _ = earth.apply_maneuver(lambert, intermediate=True)

# Model the transfer orbit as an ephem
transfer_ephem = transfer.to_ephem(strategy=EpochsArray(epochs))


# Visualize the transfer
plotter = plot_solar_system(epoch=at_launch, outer=True, length_scale_units=u.AU, plane=Planes.EARTH_ECLIPTIC)
plotter.plot_ephem(transfer_ephem, label="Transfer orbit", color="red")
oumuamua_lines, _ = plotter.plot_coordinates(oumuamua_ephem.sample(epochs), position=oumuamua_ephem.rv(at_arrival)[0], label="1I/'Oumuamua at arrival", color="black")
oumuamua_lines.set_linestyle("--")

# Display the plot
plt.savefig("fig/static/oumuamua/direct-optimum-transfer.png", bbox_inches="tight")
plotter.show()
