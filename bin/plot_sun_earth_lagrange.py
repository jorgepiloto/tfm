from astropy import units as u
from astropy.time import Time

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.bodies import Sun, Earth
from poliastro.plotting import OrbitPlotter
from poliastro.util import time_range



earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
moon = Ephem.from_csv("bin/ephem/moon.csv", plane=Planes.EARTH_ECLIPTIC)
l1 = Ephem.from_csv("bin/ephem/semb-l1.csv", plane=Planes.EARTH_ECLIPTIC)
l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
l4 = Ephem.from_csv("bin/ephem/semb-l4.csv", plane=Planes.EARTH_ECLIPTIC)
l5 = Ephem.from_csv("bin/ephem/semb-l5.csv", plane=Planes.EARTH_ECLIPTIC)

points_and_labels = [
    (l1, "L1"),
    (l2, "L2"),
    (l4, "L4"),
    (l5, "L5"),
]

start = Time("2024-01-01", scale="tdb")
end = Time("2025-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

plotter = OrbitPlotter(plane=Planes.EARTH_ECLIPTIC, length_scale_units=u.AU)
plotter.set_body_frame(Earth)
plotter.set_attractor(Sun)
plotter.plot_coordinates(earth.sample(epochs), position=earth.rv(start)[0], label="Earth", color="blue")
plotter.plot_coordinates(moon.sample(epochs), position=moon.rv(start)[0], label="Moon", color="gray")

for lpoint, label in points_and_labels:
    plotter.plot_coordinates(lpoint.sample(epochs),
                             position=lpoint.rv(start)[0], label=label,
                             color="red")


# TODO: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/zoom_inset_axes.html
x1, x2, y1, y2 = 0.97, 0.993, -0.01, 0.075
axins = plotter.backend.ax.inset_axes(
    [0.5, 0.5, 0.47, 0.47],
    xlim=(x1, x2), ylim=(y1, y2), xticklabels=[], yticklabels=[])
axins.imshow(Z2, extent=extent, origin="lower")

ax.indicate_inset_zoom(axins, edgecolor="black")


plotter.show()
