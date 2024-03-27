"""Utilities module for downloading and using JPL ephemerides."""

import httpx


JPL_HORIZONS_API = "https://ssd.jpl.nasa.gov/api/horizons.api"
"""The URL of the JPL Horizons API."""


def assemble_jpl_query(command, start_time, stop_time):
    common_parameters = {
        "format": "text",
        "COMMAND": f"'DES={command};'",  # Official indicator for Oumuamua
        "OBJ_DATA": "NO",               # Do not include header data
        "MAKE_EPHEM": "YES",            # Generate ephemerides for the query
        "EPHEM_TYPE": "VECTOR",         # Request only vector data
    }

    ephemerides_parameters = {
        "CENTER": "500@10",             # Generate ephemerides w.r.t Sun's center
        "START_TIME": start_time,     # Start time for the ephemerides
        "STOP_TIME": stop_time,      # Stop time for the ephemerides
        "STEP_SIZE": "1d",              # Step size is 1 day
        "REF_SYSTEM": "ICRF",           # Reference system is ICRF
        "VEC_TABLE": "2",               # Request only state vector
        "OUT_UNITS": "KM-S",            # Output units in Kilometers and seconds
        "CAL_FORMAT": "JD",             # Dates must be in Julian Date
        "CSV_FORMAT": "YES",            # Apply CSV formatting
    }

    return common_parameters | ephemerides_parameters


async def query_jpl_horizons(command, start_time, stop_time) -> str:
    """Query JPL Horizons System with desired parameters.

    Parameters
    ----------
    params : dict
        Dictionary relating parameters and their values.

    Returns
    -------
    str
        Ephemerides data in string format.

    Notes
    -----
    For a complete list of valid parameters refer to https://ssd-api.jpl.nasa.gov/doc/horizons.html.
    
    """
    async with httpx.AsyncClient() as client:
        parameters = assemble_jpl_query(command, start_time, stop_time)
        response = await client.get(JPL_HORIZONS_API, params=parameters)
        if response.status_code == 200:
            return response.text
        else:
            raise RuntimeError("Failed to retrieve data.")

borisov_ephem = query_jpl_horizons("C/2019 Q4", "2019-01-01", "2020-01-01")
