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

start = Time("2034-01-01", scale="tdb")
end = Time("2035-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

coordinates = {
    "x": [],
    "y": [],
    "z": [],
}
velocities = {
    "vx": [],
    "vy": [],
    "vz": [],
}

epoch = start
delta_time = 1 * u.day
while epoch <= end:

    sun_r, _ = sun.rv(epoch)
    earth_r, earth_v = earth.rv(epoch)
    n = np.cross(earth_r, earth_v) / np.linalg.norm(np.dot(earth_r, earth_v))

    _, l2, *_ = lagrange_points_vec(Sun.mass, sun_r, Earth.mass, earth_r, n)
    coordinates["x"].append(l2[0])
    coordinates["y"].append(l2[1])
    coordinates["z"].append(l2[2])
    units = l2.unit
    epoch += delta_time

"""
for ith_state in range(1, len(coordinates)):
    r0 = np.asarray([
            coordinates["x"][ith_state - 1].to_value(u.km),
            coordinates["y"][ith_state - 1].to_value(u.km),
            coordinates["z"][ith_state - 1].to_value(u.km),
    ])
    rf = np.asarray([
            coordinates["x"][ith_state].to_value(u.km),
            coordinates["y"][ith_state].to_value(u.km),
            coordinates["z"][ith_state].to_value(u.km),
    ])
    v0, _ = izzo(Sun.k.to_value(u.km**3/u.s**2) , r0,
                 rf, (1 * u.day).to_value(u.s), 0, prograde=True,
                lowpath=True, numiter=35, rtol=1e-7)
    velocities["vx"].append(v0[0])
    velocities["vy"].append(v0[1])
    velocities["vz"].append(v0[2])
"""

l2_coordinates = CartesianRepresentation(
    x=coordinates["x"],
    y=coordinates["y"],
    z=coordinates["z"],
    unit=units,
)





plotter = OrbitPlotter(plane=Planes.EARTH_ECLIPTIC)
plotter.set_body_frame(Earth)
plotter.set_attractor(Sun)
earth_lines, _ = plotter.plot_coordinates(earth.sample(epochs),
                                             position=earth.rv(end)[0],
                                             label="Earth at end", color="navy")
plotter.plot_coordinates(l2_coordinates, label="L2", color="red")
plotter.show()
