from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.plotting.misc import plot_solar_system
from poliastro.util import time_range
from matplotlib import pyplot as plt


discovery=Time("2019-08-30", scale="tdb")
epochs = time_range("2014-01-01", end="2022-01-01")
borisov_ephem = Ephem.from_horizons("C/2019 Q4", epochs)
borisov = Orbit.from_ephem(Sun, borisov_ephem, epoch=discovery)

plotter = plot_solar_system(epoch=discovery, outer=False, length_scale_units=u.AU)
plotter.plot(borisov, label="2I/Borisov", color="black")
plotter.backend.ax.set_xlim(-3, 3)
plotter.backend.ax.set_ylim(-3, 3)
plt.savefig("fig/static/borisov/orbit.png", bbox_inches="tight")
