# Copyright [2023] The Helx Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import gymnasium
import optax
from absl import app, flags, logging

import helx
from helx.networks import MLP

helx.flags.define_flags_from_hparams(helx.agents.SACHparams)
FLAGS = flags.FLAGS


def main(argv):
    del argv
    logging.info("Starting")

    # environment
    env = gymnasium.make("HalfCheetah-v4", max_episode_steps=100)
    env = helx.environment.to_helx(env)

    # optimiser
    optimiser = optax.adam(learning_rate=FLAGS.learning_rate)

    # agent
    hparams = helx.flags.hparams_from_flags(
        helx.agents.SACHparams,
        obs_space=env.observation_space(),
        action_space=env.action_space(),
        replay_start=10,
        batch_size=2,
    )
    agent = helx.agents.SAC(
        hparams=hparams,
        optimiser=optimiser,
        seed=0,
        actor_representation_net=MLP(features=[128, 128]),
        critic_representation_net=MLP(features=[128, 128]),
    )

    helx.experiment.run(agent, env, 2)


if __name__ == "__main__":
    app.run(main)