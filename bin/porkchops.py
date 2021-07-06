""" Generates a cool pork-chop for Perseverance 2020 mission """

import astropy.units as u
import matplotlib.pyplot as plt
from astropy.time import Time
from matplotlib.lines import Line2D
from poliastro.bodies import Earth, Mars
from poliastro.plotting.porkchop import PorkchopPlotter
from poliastro.util import time_range

def build_porkchop():
    # Define launch and arrival time spans
    # TODO: porkchop resolution defined as low to improve compilation time
    launch_span = time_range("2020-03-01", end="2020-10-01", periods=int(150))
    arrival_span = time_range("2020-10-01", end="2021-05-01", periods=int(150))

    # Build the pork-chop
    _, ax = plt.subplots(1,1,figsize=(8,8))
    porkchop = PorkchopPlotter(Earth, Mars, launch_span, arrival_span, ax=ax)
    dv_dpt, dv_arr, c3dpt, c3arr, tof = porkchop.porkchop()
    ax = porkchop.ax

    # Generate custom legend
    legend_elements = [
        Line2D([0], [0], color="r", linestyle="--", lw=4, label="Days of flight"),
        Line2D([0], [0], color="navy", linestyle="--", lw=4, label="Arrival velocity km/s"),
    ]

    mission_elements = []

    # Missions
    missions_set = {
        "Perseverance": [Time("2020-07-30"), Time("2021-02-18"), "blue"],
        "Tianwen-1": [Time("2020-07-23"), Time("2021-02-10"), "red"],
        "Hope Mars": [Time("2020-07-19"), Time("2021-02-09"), "darkorange"],
    }

    # Plot mission launch date
    for mission in missions_set:
        launch_date = missions_set[mission][0].to_datetime()
        arrival_date = missions_set[mission][1].to_datetime()
        color = missions_set[mission][-1]
        ax.plot(launch_date, arrival_date, "ko", markersize=10)
        ax.plot(launch_date, arrival_date, color=color, marker="x", mew=2, label=mission)
        mission_elements.append(
            Line2D(
                [],
                [],
                color=color,
                marker="x",
                mew=2,
                markersize=10,
                linestyle=None,
                linewidth=0,
                label=mission,
            )
        )


    leg1 = ax.legend(handles=legend_elements, shadow=True)
    leg2 = ax.legend(handles=mission_elements, loc="lower right", shadow=True)
    ax.add_artist(leg1)
    ax.set_xlabel("Launch date")
    ax.set_ylabel("Arrival date")
    ax.set_title(
        f"Earth - Mars for year 2020-2021, C3 launch",
    )


    plt.savefig("fig/porkchop.png", bbox_inches='tight')
