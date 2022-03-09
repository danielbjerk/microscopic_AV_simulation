import simulation
import scenario
import toml



if __name__ == "__main__":

    config_path = "../config.toml"
    scenario_path = ""  # TODO: decide format

    dict_config = toml.load(config_path)
    dict_sim_config = dict_config["simulation"]

    dict_scen_config = toml.load(scenario_path)
    scen = scenario.Scenario(dict_scen_config)

    sim = simulation.Simulation(scen, dict_sim_config)

    b_stop_sim = False
    while not b_stop_sim:
        sim.update()

        # Metric.measure(sim.state)
        
        # Plot here?