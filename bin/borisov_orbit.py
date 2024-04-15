from astropy import units as u
from astropy.time import Time

from matplotlib import pyplot as plt

from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.plotting.misc import plot_solar_system

borisov = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)
discovery = Time("2019-08-30", scale="tdb")

plotter = plot_solar_system(epoch=discovery, outer=False, length_scale_units=u.AU, plane=Planes.EARTH_ECLIPTIC)
borisov_orbit_lines, _ = plotter.plot_ephem(borisov, epoch=discovery, color="black", label="2I/Borisov")
borisov_orbit_lines.set_linestyle("--")

plotter.backend.ax.set_xlim(-3, 3)
plotter.backend.ax.set_ylim(-3, 3)
plt.savefig("fig/static/borisov/orbit.png", bbox_inches="tight")
plotter.show()
