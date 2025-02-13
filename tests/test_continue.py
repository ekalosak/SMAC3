import os
import shutil
from io import StringIO

import pytest

from smac import BlackBoxFacade, HyperparameterOptimizationFacade, Scenario


def test_continue_same_scenario(rosenbrock):
    for facade in [BlackBoxFacade]:
        # That should work: We did not optimize in the first run
        scenario = Scenario(rosenbrock.configspace, n_trials=10)
        smac = facade(scenario, rosenbrock.train, overwrite=True)

        scenario = Scenario(rosenbrock.configspace, n_trials=10)
        smac = facade(scenario, rosenbrock.train)
        smac.optimize()

        # Should not work: After optimization, we can not continue (yet)
        # However, we can load the results
        scenario = Scenario(rosenbrock.configspace, n_trials=10)
        smac = facade(scenario, rosenbrock.train, overwrite=True)
        smac.optimize()
        scenario = Scenario(rosenbrock.configspace, n_trials=10)
        smac2 = facade(scenario, rosenbrock.train)
        assert smac.incumbent == smac2.incumbent
        with pytest.raises(NotImplementedError, match="Unfortunately, previous runs can not be continued yet.*"):
            smac2.optimize()


def test_continue_different_scenario(rosenbrock, monkeypatch):
    for facade in [BlackBoxFacade, HyperparameterOptimizationFacade]:
        # Overwrite completely
        number_inputs = StringIO("1\n")
        monkeypatch.setattr("sys.stdin", number_inputs)
        scenario = Scenario(rosenbrock.configspace, name="blub1", n_trials=10)
        smac = facade(scenario, rosenbrock.train, overwrite=True)
        smac.optimize()
        scenario = Scenario(rosenbrock.configspace, name="blub1", n_trials=11)
        smac = facade(scenario, rosenbrock.train)

        # Keep old run
        try:
            shutil.rmtree("smac3_output/blub2")
            shutil.rmtree("smac3_output/blub2-old")
        except FileNotFoundError:
            pass

        number_inputs = StringIO("2\n")
        monkeypatch.setattr("sys.stdin", number_inputs)
        scenario = Scenario(rosenbrock.configspace, name="blub2", n_trials=10)
        smac = facade(scenario, rosenbrock.train, overwrite=True)
        smac.optimize()
        scenario = Scenario(rosenbrock.configspace, name="blub2", n_trials=11)
        smac = facade(scenario, rosenbrock.train)
        assert os.path.isdir("smac3_output/blub2-old")
