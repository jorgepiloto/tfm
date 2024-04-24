from astropy import units as u
from astropy.time import Time
import matplotlib.pyplot as plt

from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.bodies import Sun, Earth
from poliastro.plotting import OrbitPlotter
from poliastro.plotting.orbit.backends import Matplotlib2D
from poliastro.util import time_range



earth = Ephem.from_csv("bin/ephem/earth.csv", plane=Planes.EARTH_ECLIPTIC)
moon = Ephem.from_csv("bin/ephem/moon.csv", plane=Planes.EARTH_ECLIPTIC)
l1 = Ephem.from_csv("bin/ephem/semb-l1.csv", plane=Planes.EARTH_ECLIPTIC)
l2 = Ephem.from_csv("bin/ephem/semb-l2.csv", plane=Planes.EARTH_ECLIPTIC)
l4 = Ephem.from_csv("bin/ephem/semb-l4.csv", plane=Planes.EARTH_ECLIPTIC)
l5 = Ephem.from_csv("bin/ephem/semb-l5.csv", plane=Planes.EARTH_ECLIPTIC)

points_and_labels = {
    l1: ["L1", (0.972, -0.00475)],
    l2: ["L2", (0.991, -0.00501)],
    l4: ["L4", (0.5018, 0.8531)],
    l5: ["L5", (0.4791, -0.8501)],
}

start = Time("2024-01-01", scale="tdb")
end = Time("2025-01-01", scale="tdb")
epochs = time_range(start, end=end, num_values=1000, scale="tdb")

plotter = OrbitPlotter(plane=Planes.EARTH_ECLIPTIC, length_scale_units=u.AU)
plotter.set_body_frame(Earth)
plotter.set_attractor(Sun)
plotter.plot_coordinates(earth.sample(epochs), position=earth.rv(start)[0],
                         label=f"Earth at 2024-01-01", color="blue")
plotter.plot_coordinates(moon.sample(epochs), position=moon.rv(start)[0],
                         label=f"Moon at 2024-01-01", color="gray")

for lpoint, (label, position) in points_and_labels.items():
    lines, _ = plotter.plot_coordinates(lpoint.sample(epochs),
                             position=lpoint.rv(start)[0], label=label,
                             color="red")
    lines.set_visible(False)
    if label in ["L1", "L2"]:
        plotter.backend.ax.annotate(label, position, (position[0],
                                                      position[1] + 0.001), color="red")
    else:
        plotter.backend.ax.annotate(label, position, (position[0],
                                                      position[1] + 0.05), color="red")

# TODO: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/zoom_inset_axes.html
x1, x2, y1, y2 = 0.97, 0.993, -0.01, 0.0075
axins = plotter.backend.ax.inset_axes(
    [0.05, 0.55, 0.47, 0.47],
    xlim=(x1, x2), ylim=(y1, y2), 
    xticks=[],
    yticks=[],
    xticklabels=[], 
    yticklabels=[],)

zoom_backend = Matplotlib2D(ax=axins)
zoom_plotter = OrbitPlotter(backend=zoom_backend, plane=Planes.EARTH_ECLIPTIC, length_scale_units=u.AU)
zoom_plotter.set_body_frame(Earth)
zoom_plotter.set_attractor(Sun)

lines, marker = zoom_plotter.plot_coordinates(earth.sample(epochs),
                                              position=earth.rv(start)[0],
                                              label=f"Earth at 2024-01-01", color="blue")
del lines

zoom_plotter.plot_coordinates(moon.sample(epochs), position=moon.rv(start)[0],
                              label="Moon at 2024-01-01", color="gray")

for lpoint, (label, position) in points_and_labels.items():
    lines, _ =zoom_plotter.plot_coordinates(lpoint.sample(epochs),
                             position=lpoint.rv(start)[0],
                             color="red")
    lines.set_visible(False)
    if label in ["L1", "L2"]:
        zoom_plotter.backend.ax.annotate(label, position, (position[0],
                                                      position[1] + 0.001), color="red")

    earth_position = (0.98181, -0.00494)
    zoom_plotter.backend.ax.annotate(
            "Earth", 
            earth_position,
            (earth_position[0], earth_position[1] - 0.002),
            color="blue"
    )
    moon_position = (0.98336, -0.00273)
    zoom_plotter.backend.ax.annotate(
            "Moon", 
            moon_position,
            (moon_position[0], moon_position[1] - 0.002),
            color="gray"
    )





axins.set_xlim(0.97, 0.993)
axins.set_ylim(-0.01, 0.0075)
axins.legend().remove()

plotter.backend.ax.indicate_inset_zoom(axins, edgecolor="black")
plt.savefig("fig/static/lagrange_points.png", bbox_inches="tight")
