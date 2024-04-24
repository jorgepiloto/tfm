from astropy import units as u
from astropy.time import Time
from astropy.constants import G
import numpy as np
import matplotlib.pyplot as plt

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.bodies import Sun, Earth, Moon
from poliastro.plotting import OrbitPlotter
from poliastro.plotting.orbit.backends import Matplotlib2D
from poliastro.util import time_range



earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
moon = Ephem.from_csv("bin/ephem/moon.csv", plane=Planes.EARTH_ECLIPTIC)
l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)

start = Time("2010-01-01", scale="tdb")
end = Time("2035-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

def escape_velocity(k, r):
    return (2 * k / r) ** 0.5

def center_of_mass(r1, m1, r2, m2):
    return (r1 * m1 + r2 * m2) / (m1 + m2)

def distance_between(r1, r2):
    return np.linalg.norm(r1 - r2)


escape_velocities = []
for epoch in epochs:
    earth_r, earth_v = earth.rv(epoch)
    moon_r, moon_v = moon.rv(epoch)
    l2_r, l2_v = l2.rv(epoch)
    
    earth_m = Earth.mass
    moon_m = Moon.mass
    total_m = earth_m + moon_m
    total_k = G * total_m
    
    barycenter_r = center_of_mass(earth_r, earth_m, moon_r, moon_m)
    delta_r = np.linalg.norm(distance_between(l2_r, barycenter_r))
    
    v_escape = escape_velocity(total_k, delta_r).to(u.km / u.s)
    escape_velocities.append(v_escape.to_value(u.km / u.s))

mean_escape_velocity = np.mean(escape_velocities) * u.km / u.s
print(f"Mean escape velocity: {mean_escape_velocity:.2f}")
