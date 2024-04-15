from astropy import units as u
from astropy.time import Time

from matplotlib import pyplot as plt

from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.plotting.misc import plot_solar_system

oumuamua = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)
discovery = Time("2017-10-19", scale="tdb")

plotter = plot_solar_system(epoch=discovery, outer=False, length_scale_units=u.AU, plane=Planes.EARTH_ECLIPTIC)
borisov_orbit_lines, _ = plotter.plot_ephem(oumuamua, epoch=discovery, color="black", label="1I/'Oumuamua")
borisov_orbit_lines.set_linestyle("--")

plotter.backend.ax.set_xlim(-2, 2)
plotter.backend.ax.set_ylim(-2, 2)
plt.savefig("fig/static/oumuamua/orbit.png", bbox_inches="tight")
plotter.show()
