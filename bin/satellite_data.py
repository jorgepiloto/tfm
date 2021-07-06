""" Manages satellite database """

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_total_launches_per_year(DATA, min_year=None, max_year=2020, ax=None):
    """ Returns a plot of total launches per year """

    # Check if axes available
    if not ax:
        _, ax = plt.subplots(1, 1, figsize=(10,5))
        ax.set_title(f"Number of launches between {min_year}-{max_year}")
        ax.set_xlabel("Date of launch")
        ax.set_ylabel("Number of launches")

    # Get a collection of launches, minimum, maximum
    launch_dates = DATA["Date of Launch"]
    if not min_year:
        min_year = DATA["Date of Launch"].min().year
    if not max_year:
        max_year = DATA["Date of Launch"].max().year

    # Allocate arrays
    launch_years = np.linspace(min_year, max_year, (max_year - min_year) + 1, dtype=int)
    launches = np.zeros_like(launch_years)

    # Iterate over each year of launch
    for i, launch_year in enumerate(launch_years):
        for date in launch_dates:

            # If both years are equal, increase counter by one unit
            if date.year == launch_year:
                launches[i] += 1

    # Append data to plots
    ax.plot(launch_years, launches, "-k", label="Total launches per year")
    ax.set_xticks(launch_years[launch_years % 5 == 0])

    return ax


def plot_total_launches_per_purpose(
    DATA,
    purpose_set,
    min_year=None,
    max_year=2020,
    ax=None,
    color_set=None,
):
    """ Returns a graphical representation of missions per purpose """

    # Check if axes available
    if not ax:
        _, ax = plt.subplots(1, 1)
        ax.set_title("Launches per mission type between {min_year}-{max_year}")
        ax.set_xlabel("Launching year")
        ax.set_xlabel("Launching year")

    # Get a collection of launches, minimum, maximum
    launch_dates = DATA["Date of Launch"]
    if not min_year:
        min_year = DATA["Date of Launch"].min().year
    if not max_year:
        max_year = DATA["Date of Launch"].max().year

    # Allocate final array
    launch_years = np.linspace(min_year, max_year, (max_year - min_year) + 1, dtype=int)
    launches_per_purpose = np.zeros((len(launch_years), 1 + len(purpose_set)))
    launches_per_purpose[:, 0] = launch_years

    # Get missions by purpose
    all_missions = DATA["Purpose"]

    # Iterate over each one of the purposes
    for i, purpose in enumerate(purpose_set):

        # Filter missions by year
        valid_missions_date = DATA["Date of Launch"][all_missions == purpose]

        for date in valid_missions_date:
            in_row = launches_per_purpose[:, 0] == date.year
            launches_per_purpose[in_row, i + 1] += 1

        ax.plot(
            launch_years,
            launches_per_purpose[:, i + 1],
            color=color_set[i],
            label=f"{purpose}",
        )

    return ax


if __name__ == "__main__":

    # Read the Excel database file
    DATA = pd.read_excel("dat/satellite_database.xls")

    # Plot satellites as of per year launch
    min_year = 1990
    ax = plot_total_launches_per_year(DATA, min_year)

    purpose_set = [
        "Earth Observation",
        "Communications",
        "Space Science",
    ]
    color_set = ["Blue", "Red", "Green"]
    ax = plot_total_launches_per_purpose(
        DATA, purpose_set=purpose_set, min_year=min_year, color_set=color_set, ax=ax
    )
    ax.legend(shadow=True)
    plt.savefig("fig/sat_evolution.png", bbox_inches='tight')
