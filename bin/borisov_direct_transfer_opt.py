from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun, Earth
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.plotting.misc import plot_solar_system
from poliastro.plotting.orbit import OrbitPlotter
from poliastro.util import time_range
from poliastro.maneuver import Maneuver
from matplotlib import pyplot as plt


# Compute ephemeris
epochs = time_range("2017-05-01", end="2033-01-01", scale="tdb")
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

#plotter = plot_solar_system(epoch=launch_date, outer=False, length_scale_units=u.AU)
plotter = OrbitPlotter(length_scale_units=u.AU)
plotter.plot_body_orbit(Earth, launch_date, label="Earth at launch", color="blue")
plotter.plot_ephem(transfer_orbit.to_ephem(), label="Transfer orbit", color="red")
#plotter.plot_ephem(earth_ephem, label="Earth at launch", color="blue")
plotter.plot_ephem(borisov_ephem, label="2I/Borisov", color="black")
#plotter.backend.ax.set_xlim(-3, 3)
#plotter.backend.ax.set_ylim(-3, 3)
plt.savefig("fig/static/borisov/direct-optimum-transfer.png", bbox_inches="tight")
plt.show()
