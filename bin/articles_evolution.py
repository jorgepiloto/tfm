""" Number of articles evolution during the last centuries """

from datetime import datetime
from glob import glob

import matplotlib.pyplot as plt
import numpy as np


def get_article_name_and_date(article):
    """ Retrieves the author and date of the article """

    # Get the filename, author and name
    filename = article[4:]
    date = filename[0:4]
    author = filename[5 : (len(filename) - 4)].capitalize()

    return author, date

def plot_timeline(authors, dates):
    """ Returns a timeline """

    namedates = []
    for author, date in zip(authors, dates):
        namedates.append(f"{author}")

    # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y") for d in dates]

    #Choose some nice levels
    #levels = np.tile([-5, 5, -4, 4, -3, 3, -2, 2, -1, 1], int(np.ceil(len(dates) / 6)))[
    #   : len(dates)
    #]
    levels = np.tile(
        [20, -20, 19, -19, 18, -18, 17, -17, 16, -16, 15, -15, 14, -14, -13, 13, -12, 12, -11, 11, -10, 10, -9, 9, -8, 8, -7, 7, -6, 6, -5, 5, -4, 4, -3, 3, -2, 2, -1, 1],
        int(np.ceil(len(dates) / 6)),
    )[: len(dates)]

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(10, 6))
    #ax.set(title="Published articles about Lamber's problem during the last decades")

    markerline, stemline, baseline = ax.stem(
        dates, levels, linefmt="C3-", basefmt="k-", use_line_collection=True
    )

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(["top", "bottom"])[(levels > 0).astype(int)]
    for d, l, text, va in zip(dates, levels, namedates, vert):
        ax.annotate(
            text,
            xy=(d, l),
            xytext=(-3, np.sign(l) * 3),
            textcoords="offset points",
            va=va,
            ha="center",
            bbox=dict(boxstyle="square", ec="black", color="white"),
        )

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)
    ax.set_xlabel("Year of publication")
    plt.subplots_adjust(left=0.1, right=0.9)
    plt.savefig("fig/lambert_articles.png", bbox_inches='tight')


if __name__ == "__main__":

    # Allocate author and years set
    author_set, date_set = [], []

    # Iterate over each article of the collection
    for article in glob("art/*.pdf"):
        author, year = get_article_name_and_date(article)
        if int(year) < 1950:
            continue
        author_set.append(author)
        date_set.append(year)

    # Start by creating the
    plot_timeline(author_set, date_set)

# Resources
# https://stackoverflow.com/questions/59944182/how-to-create-a-visualization-for-events-along-a-timeline
