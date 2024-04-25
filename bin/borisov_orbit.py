from astropy import units as u
from astropy.time import Time

from matplotlib import pyplot as plt

from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.plotting.misc import plot_solar_system

borisov = Ephem.from_csv("bin/ephem/borisov.csv", plane=Planes.EARTH_ECLIPTIC)
discovery = Time("2019-08-30", scale="tdb")

view_and_limits = {
    "xy": [[-3, 3], [-3, 3]],
    "xz": [[-0.2, 3], [-0.2, 1.2]],
    "yz": [[-1.6, 1.7], [-0.2, 1]],
}

for view, (xlim, ylim) in view_and_limits.items():
    plotter = plot_solar_system(epoch=discovery, outer=False,
                                length_scale_units=u.AU,
                                plane=Planes.EARTH_ECLIPTIC, view=view)
    borisov_orbit_lines, _ = plotter.plot_ephem(borisov, epoch=discovery,
                                                color="black", label="2I/Borisov at its discovery")
    borisov_orbit_lines.set_linestyle("--")
    plotter.backend.ax.set_xlim(xlim)
    plotter.backend.ax.set_ylim(ylim)
    if view != "xy":
        plotter.backend.ax.legend().remove()
    plt.savefig(f"fig/static/borisov/orbit_{view}.png", bbox_inches="tight")
