from astropy import units as u
from astropy.time import Time

from matplotlib import pyplot as plt

from poliastro.frames import Planes
from poliastro.ephem import Ephem
from poliastro.plotting.misc import plot_solar_system

oumuamua = Ephem.from_csv("bin/ephem/oumuamua.csv", plane=Planes.EARTH_ECLIPTIC)
discovery = Time("2017-10-19", scale="tdb")

view_and_limits = {
    "xy": [[-2, 2], [-2, 2]],
    "xz": [[-1.5, 1.5], [-0.5, 1]],
    "yz": [[-1.5, 1.5], [-0.5, 1]],
}

for view, (xlim, ylim) in view_and_limits.items():
    plotter = plot_solar_system(epoch=discovery, outer=False,
                                length_scale_units=u.AU,
                                plane=Planes.EARTH_ECLIPTIC, view=view)
    borisov_orbit_lines, _ = plotter.plot_ephem(oumuamua, epoch=discovery,
                                                color="black",
                                                label="1I/'Oumuamua at its discovery")
    borisov_orbit_lines.set_linestyle("--")

    plotter.backend.ax.set_xlim(xlim)
    plotter.backend.ax.set_ylim(ylim)
    if view != "xy":
        plotter.backend.ax.legend().remove()
    plt.savefig(f"fig/static/oumuamua/orbit_{view}.png", bbox_inches="tight")
