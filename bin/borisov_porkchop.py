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
    launch_span = time_range("2016-01-01", end="2028-01-01", num_values=N, scale="tdb")
    arrival_span = time_range("2032-01-01", end="2035-01-01", num_values=N, scale="tdb")

    borisov_ephem = Ephem.from_horizons("C/2019 Q4", launch_span)
    borisov = Orbit.from_ephem(Sun, borisov_ephem, Time("2016-01-01", scale="tdb"))

    _, ax = plt.subplots(figsize=(16, 8))
    porkchop = PorkchopPlotter(
        Earth, borisov, launch_span, arrival_span, ax=ax,
    )
    porkchop.plot(
        c3_levels=np.linspace(0, 12e3, 13) * u.km ** 2 / u.s ** 2,
        tof_levels=np.linspace(0, 20, 21) * u.year,
        dv_levels=np.linspace(0, 60, 11) * u.km / u.s,
        plot_c3_lines=False,
        plot_tof_lines=True,
        plot_dv_lines=False,
        plot_av_lines=False,
        title="Earth - 2I/Borisov transfers for years 2016 - 2028\nLaunch energy $C_3$ and required time of flight"
    )
    plt.savefig("fig/static/borisov/direct-transfer-porkchop.png", bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
