"""Computes ISOs density from paper data."""

import astropy.units as u


def main():
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

if __name__ == "__main__":
    main()

% \begin{table}[h]
%     \centering
%     \begin{tabular}{|c|c|c|}
%         \hline
%         \textbf{Study} & \textbf{Density limit ($\text{pc}^{-3}$)} & \textbf{Density limit ($\text{AU}^{-3}$)} \\
%         \hline
%         \cite{gaidos2017} & $1.0 \times 10^{14}$ & $8.5 \times 10^{37}$ \\
%         \cite{jewitt2017} & $8.0 \times 10^{14}$ & $6.8 \times 10^{38}$ \\
%         \cite{portegies2018} & $1.0 \times 10^{14}$ & $8.5 \times 10^{37}$ \\
%         \cite{feng2018} & $4.8 \times 10^{13}$ & $4.1 \times 10^{37}$ \\
%         \cite{fraser2018} & $8.0 \times 10^{14}$ & $6.8 \times 10^{38}$ \\ 
%         \cite{do2018} & $2.0 \times 10^{15}$ & $1.7 \times 10^{39}$ \\ 
%         \hline
%     \end{tabular}
%     \caption{Density limits estimated by different studies. Note that future
%     discoveries and improvements in detection techniques can lead to different
%     estimations. Adapted from \cite{moro2023}.}
%     \label{tab:iso_density_limits}
% \end{table}


