from ..builtin_components import Detection, Transform2D
from ..ecs import ECSManager
from ..system import system


@system(
    reads=(Transform2D,),
    writes=(Detection,),
)
def detection(ecs: ECSManager) -> None:
    detections = ecs.find_entities_with_all_components(Detection)

    for entity_id in detections:
        detect = ecs.fetch_single_component_from_entity(entity_id, Detection)
        detect.in_range = []
        t1 = ecs.fetch_single_component_from_entity(entity_id, Transform2D)

        for other in ecs.find_entities_with_all_components(Transform2D):
            if detect.detect_only is not None:
                ec = ecs.fetch_components_from_entity(other, *detect.detect_only)

                if not set(detect.detect_only).issubset(set(ec.keys())):
                    continue

            t2 = ecs.fetch_single_component_from_entity(other, Transform2D)
            dist = t2.world_position.distance_squared_to(t1.world_position)

            if dist <= detect.range**2:
                detect.in_range.append(other)
