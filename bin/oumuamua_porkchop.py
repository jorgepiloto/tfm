from astropy import units as u
from astropy.time import Time
from matplotlib import pyplot as plt
import numpy as np

from poliastro.bodies import Earth, Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range


def main():

    N = 75
    launch_span = time_range("2016-01-01", end="2028-01-01", num_values=N)
    arrival_span = time_range("2032-01-01", end="2035-01-01", num_values=N)

    oumuamua_ephem = Ephem.from_horizons("'Oumuamua", launch_span)
    oumuamua = Orbit.from_ephem(Sun, oumuamua_ephem, Time("2016-01-01"))

    _, ax = plt.subplots(figsize=(16, 8))
    porkchop = PorkchopPlotter(
        Earth, oumuamua, launch_span, arrival_span, ax=ax,
    )
    porkchop.plot(
        c3_levels=np.linspace(0, 12e3, 13) * u.km ** 2 / u.s ** 2,
        tof_levels=np.linspace(0, 20, 21) * u.year,
        plot_c3_lines=False,
        plot_tof_lines=True,
        plot_dv_lines=False,
        plot_av_lines=False,
        title="Earth - 2I/Oumuamua transfers for years 2016 - 2028\nLaunch energy $C_3$ and required time of flight"
    )
    plt.savefig("fig/static/oumuamua/direct-transfer-porkchop.png", bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
