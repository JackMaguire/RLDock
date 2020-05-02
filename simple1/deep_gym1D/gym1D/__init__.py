import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Gym1D-v0',
    entry_point='gym1D.envs:Gym1DEnv',
    max_episode_steps=200,
)
