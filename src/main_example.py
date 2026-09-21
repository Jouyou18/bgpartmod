"""Minimal example: run the reference biogeochemical configuration and plot the results.

Run from the repository root:  python src/main_example.py
"""
import os

import matplotlib.pyplot as plt

from src.config_model import base_config
from src.config_system import path_config as path_cfg
from src.core import model, phys
from src.utils import plotting as plotres
from src.utils import simulation_manager as sim_manager


def run_reference():
    """Kerimoglu et al. (2022) biogeochemistry, 30 days, synthetic light and temperature."""
    setup = phys.Setup(tmax=30., dt=1e-2, dt2=1e-3)
    return model.Model(base_config.Kerimoglu2022, setup=setup, name='reference_run')


def run_with_modified_parameter():
    """Same configuration with one parameter changed, to compare against the reference."""
    from src.utils import config_tools as cfg

    config = cfg.deep_update(base_config.Kerimoglu2022,
                             {'Phy': {'parameters': {'mu_max': 3.5}}})
    setup = phys.Setup(tmax=30., dt=1e-2, dt2=1e-3)
    return model.Model(config, setup=setup, name='lower_mu_max')


if __name__ == '__main__':
    reference = run_reference()
    simulations = [reference, run_with_modified_parameter()]

    # Reference run: full save (config, setup, results.npy, model.pkl) + one row appended to
    # Simulations/Simulations_log.csv. The timestamped name ties log row, folder and figure together.
    sim_name = sim_manager.save_simulation(
        reference,
        base_name='reference_run',
        sim_type=sim_manager.SimulationTypes.REFERENCES_SIMULATION,
        user_notes='main_example.py: Kerimoglu 2022 reference, 30 d')

    # observations=None: no observation overlay (plot_results otherwise loads a default dataset).
    os.makedirs(path_cfg.FIGURE_PATH, exist_ok=True)
    plotres.plot_results(simulations, ['Phy_C', 'Phy_Chl', 'NO3_concentration', 'DIP_concentration'],
                         observations=None,
                         save=True, filename=sim_name, fnametimestamp=False)

    print(f'\nSimulation : {sim_name}')
    print(f'  saved in : {os.path.join(path_cfg.REFERENCES_SIMULATION_DIR, sim_name)}')
    print(f'  log      : {path_cfg.LOG_FILE}')
    print(f'  figure   : {os.path.join(path_cfg.FIGURE_PATH, sim_name)}.png')
    print(f"  reload   : sim_manager.load_simulation('{sim_name}')")
    plt.show()
