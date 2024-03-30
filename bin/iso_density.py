"""Computes ISOs density from paper data."""

import astropy.units as u


def iso_density():
    """Main function."""
    data = {
        "Gaidos 2017": 1.0e14 * u.pc**-3,
        "Jewitt 2017": 8.0e14 * u.pc**-3,
        "Portegies 2018": 1.0e14 * u.pc**-3,
        "Feng 2018": 4.8e13 * u.pc**-3,
        "Fraser 2018": 8.0e14 * u.pc**-3,
        "Do 2018": 2.0e15 * u.pc**-3,
    }
    for paper, value_pc in data.items():
        value_au = value_pc.to(u.au**-3)
        print(f"{paper}: {value_pc:.1e} = {value_au:.1e}")


def oort_cloud_distance():
    """Compute the distance of the Oort cloud."""
    oort_cloud_distance = 100_000 * u.au
    print(oort_cloud_distance.to(u.lyr))


if __name__ == "__main__":
    iso_density()
    oort_cloud_distance()
