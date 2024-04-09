from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun, Earth
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.frames import Planes
from poliastro.plotting.misc import plot_solar_system
from poliastro.twobody.sampling import EpochsArray
from poliastro.plotting.orbit import OrbitPlotter
from poliastro.util import time_range
from poliastro.maneuver import Maneuver
from matplotlib import pyplot as plt


# Compute ephemeris
epochs = time_range("2017-06-17", end="2032-01-01", scale="tdb")
earth_ephem = Ephem.from_body(Earth, epochs=epochs)
borisov_ephem = Ephem.from_horizons("C/2019 Q4", epochs)

# Declare launch and arrival dates
launch_date = Time("2017-06-17", scale="tdb")
arrival_date = Time("2032-01-01", scale="tdb")

# Compute Earth and 2I/Borisov orbits at launch and arrival
earth_at_launch = Orbit.from_ephem(Sun, earth_ephem, epoch=launch_date)
earth_at_arrival = Orbit.from_ephem(Sun, earth_ephem, epoch=arrival_date)
borisov_at_launch = Orbit.from_ephem(Sun, borisov_ephem, epoch=launch_date)
borisov_at_arrival = Orbit.from_ephem(Sun, borisov_ephem, epoch=arrival_date)

# Compute the transfer orbit
maneuver = Maneuver.lambert(earth_at_launch, borisov_at_arrival)
transfer_orbit, _ = earth_at_launch.apply_maneuver(maneuver, intermediate=True)

plotter = plot_solar_system(epoch=launch_date, outer=True, plane=Planes.EARTH_EQUATOR, length_scale_units=u.AU)
plotter.plot_ephem(transfer_orbit.to_ephem(strategy=EpochsArray(epochs)),
                   label="Transfer orbit", color="red")
plotter.plot_ephem(borisov_ephem, epoch=arrival_date, label="2I/Borisov at arrival", color="black")
plotter.backend.ax.set_xlim(-52, 15)
plotter.backend.ax.set_ylim(-32, 32)
plt.savefig("fig/static/borisov/direct-optimum-transfer.png", bbox_inches="tight")
plt.show()
