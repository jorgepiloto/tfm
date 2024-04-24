from astropy import units as u
from astropy.time import Time
import matplotlib.pyplot as plt

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.bodies import Sun, Earth
from poliastro.plotting import OrbitPlotter
from poliastro.plotting.misc import plot_solar_system
from poliastro.plotting.orbit.backends import Matplotlib2D
from poliastro.util import time_range



l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)

start = Time("2024-01-01", scale="tdb")
end = Time("2025-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

plotter = plot_solar_system(epochs[0], plane=Planes.EARTH_ECLIPTIC, outer=False)
plotter.show()
