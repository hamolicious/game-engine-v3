from typing import cast

import pygame

from engine import internal_components

from .. import builtin_components
from ..ecs import ECSManager
from ..internal_components.display import Display
from ..system import system


@system
def brain(ecs: ECSManager) -> None:
    # How do I find the entities?
    big_brein = ecs.find_any_variation_on_entity(builtin_components.BaseBrain)

    for entity_id in big_brein:
        brain = ecs.fetch_single_component_from_entity(big_brein)
