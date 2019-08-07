#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `real_robots` package."""

import pytest

from click.testing import CliRunner

import real_robots  # noqa
from real_robots import cli
import gym
import numpy as np


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.demo)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.demo, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_goals():
    env = gym.make('REALRobot-v0')
    obs = env.reset()

    # Environment starts without goals
    # @TODO Check if we want to provide a goal file and load it immediately
    assert(env.goals is None)
    # goal_idx == -1 also means we are in the intrinsic phase
    assert(env.goal_idx == -1)
    # An all-zeroes matrix is displayed a goal (no goal)
    assert(obs['goal'].min() == 0 and obs['goal'].max() == 0)

    # Setting the goal path should not trigger the extrinsic phase - (Issue 12)
    env.set_goals_dataset_path('test_goals.npy.npz')
    assert(env.goal_idx == -1)

    # This should trigger the first goal
    env.set_goal()
    obs, _, _, _ = env.step(np.zeros(9))
    assert(not(obs['goal'].min() == 0 and obs['goal'].max() == 0))
    # We check one of the pixels to ensure this is the first goal
    assert(obs['goal'][126, 90, 2] == 102)
    assert(env.goal_idx == 0)

    # This should trigger the first goal
    env.set_goal()
    obs, _, _, _ = env.step(np.zeros(9))
    assert(not(obs['goal'].min() == 0 and obs['goal'].max() == 0))
    # We check one of the pixels to ensure this is the second goal
    assert(obs['goal'][126, 90, 2] == 142)
    assert(env.goal_idx == 1)
