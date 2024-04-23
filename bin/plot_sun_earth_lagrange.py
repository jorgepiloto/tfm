from astropy.coordinates import CartesianRepresentation
import numpy as np
from astropy import units as u
from astropy.time import Time

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.bodies import Sun, Earth
from poliastro.plotting.misc import plot_solar_system
from poliastro.plotting import OrbitPlotter
from poliastro.util import time_range
from poliastro.core.iod import izzo

from poliastro.threebody.restricted import lagrange_points_vec


sun = Ephem.from_csv("bin/ephem/sun.csv", plane=Planes.EARTH_ECLIPTIC)
earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
moon = Ephem.from_csv("bin/ephem/moon.csv", plane=Planes.EARTH_ECLIPTIC)
l1 = Ephem.from_csv("bin/ephem/semb-l1.csv", plane=Planes.EARTH_ECLIPTIC)
l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
l4 = Ephem.from_csv("bin/ephem/semb-l4.csv", plane=Planes.EARTH_ECLIPTIC)
l5 = Ephem.from_csv("bin/ephem/semb-l5.csv", plane=Planes.EARTH_ECLIPTIC)

start = Time("2010-01-01", scale="tdb")
end = Time("2011-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

plotter = OrbitPlotter(plane=Planes.EARTH_ECLIPTIC, length_scale_units=u.AU)
plotter.set_body_frame(Earth)
plotter.set_attractor(Sun)
plotter.plot_coordinates(earth.sample(epochs), position=earth.rv(start)[0], label="Earth", color="blue")
plotter.plot_coordinates(moon.sample(epochs), position=moon.rv(start)[0], label="Moon", color="gray")
plotter.plot_coordinates(l1.sample(epochs), position=l1.rv(start)[0], label="L1", color="green")
plotter.plot_coordinates(l2.sample(epochs), position=l2.rv(start)[0], label="L2", color="green")
plotter.plot_coordinates(l4.sample(epochs), position=l4.rv(start)[0], label="L4", color="red")
plotter.plot_coordinates(l5.sample(epochs), position=l5.rv(start)[0], label="L5", color="red")
#plotter.backend.ax.set_xlim(0, 1.003)
#plotter.backend.ax.set_ylim(-0.4, 0.4)


plotter.show()
