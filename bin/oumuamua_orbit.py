from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.plotting.misc import plot_solar_system
from poliastro.util import time_range
import matplotlib.pyplot as plt


discovery=Time("2017-10-19", scale="tdb")
epochs = time_range("2014-01-01", end="2022-01-01")
oumuamua_ephem = Ephem.from_horizons("'Oumuamua", epochs)
oumuamua = Orbit.from_ephem(Sun, oumuamua_ephem, epoch=discovery)

plotter = plot_solar_system(epoch=discovery, outer=False, length_scale_units=u.AU)
plotter.plot(oumuamua, label="1I/'Oumuamua", color="black")
plotter.backend.ax.set_xlim(-2, 2)
plotter.backend.ax.set_ylim(-2, 2)
plt.savefig("fig/static/oumuamua/orbit.png", bbox_inches="tight")
