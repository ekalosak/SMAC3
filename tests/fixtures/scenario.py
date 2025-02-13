from typing import Callable

import pytest
from ConfigSpace import ConfigurationSpace

from smac import Scenario


@pytest.fixture
def make_scenario() -> Callable:
    def _make(
        configspace: ConfigurationSpace,
        deterministic: bool = False,
        use_multi_objective: bool = False,
        use_instances: bool = False,
        n_instances: int = 3,
        n_instance_features: int = 3,
        min_budget: int = 2,
        max_budget: int = 5,
        n_workers: int = 1,
        n_trials: int = 100,
    ) -> Scenario:
        objectives = "cost"
        if use_multi_objective:
            objectives = ["cost1", "cost2"]

        instances = None
        instance_features = None
        if use_instances and n_instances > 0:
            instances = []
            instance_features = {}
            for i in range(n_instances):
                instance_name = f"i{i+1}"
                instances += [instance_name]
                instance_features[instance_name] = [j + i for j in range(n_instance_features)]

        return Scenario(
            configspace=configspace,
            name="test",
            output_directory="smac3_output_test",
            objectives=objectives,
            deterministic=deterministic,
            walltime_limit=30,
            n_trials=n_trials,
            n_workers=n_workers,
            instances=instances,
            instance_features=instance_features,
            min_budget=min_budget,
            max_budget=max_budget,
        )

    return _make
