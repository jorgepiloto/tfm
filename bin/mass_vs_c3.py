from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
from labellines import labelLines
from scipy.optimize import curve_fit

def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

def main():
    rocket_params = {
        # See: https://www.researchgate.net/publication/293081475_Mission_opportunities_to_trans-neptunian_objects_-_Part_III_orbital_capture_low-thrust_trajectories_and_vehicle_radiation_environment_during_jovian_flyby
        'Atlas V 501': {
            'c3': [0, 10, 20, 30, 40, 50, 70],
            'payload': [3000, 2000, 1800, 1300, 1000, 800, 100]
        },
        'Atlas V 401': {
            'c3': [0, 10, 20, 30, 40, 50, 70, 80, 90],
            'payload': [3500, 2900, 2500, 1900, 1500, 1000, 800, 500, 400]
        },
        'Atlas V 521': {
            'c3': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'payload': [4500, 3800, 3200, 2300, 2000, 1500, 1300, 900, 700, 500, 200]
        },
        'Atlas V 551': {
            'c3': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'payload': [6200, 5200, 4300, 3800, 3000, 2600, 2000, 1500, 1200, 900, 700]
        },
        'Atlas V 551 w/Star 48': {
            'c3': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'payload': [6200, 5250, 4350, 4000, 3300, 2800, 2500, 2100, 1800, 1500, 1200]
        },
        'Delta IV HLV': {
            'c3': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'payload': [10000, 9000, 7300, 6000, 5000, 4200, 3600, 3000, 2500,
                        1800, 1400]
        },
    }

    _, ax = plt.subplots(figsize=(10, 6))
    for rocket, params in rocket_params.items():
        c3, payload = params['c3'], params['payload']
        
        # Fit exponential curve to the data
        popt, _ = curve_fit(exponential_decay, c3, payload)
        
        # Generate interpolated values using the fitted curve
        c3_interp = np.linspace(min(c3), max(c3), 1000)
        payload_interp = exponential_decay(c3_interp, *popt)
        
        ax.plot(c3_interp, payload_interp, label=rocket, lw=2.5)

    ax.set_title('Payload mass at given C3 for modern launchers')
    ax.set_xlabel(r'C3 launch (km$^2$/s$^2$)')
    ax.set_ylabel('Payload mass (kg)')
    ax.set_xlim(0, 100)
    ax.set_ylim(500, 10000)
    labelLines(ax.get_lines(), align=True, fontsize=10, backgroundcolor="white")
    ax.legend(shadow=True)
    ax.grid(True)
    plt.savefig('fig/static/payload_vs_c3.png', bbox_inches='tight')

if __name__ == '__main__':
    main()
