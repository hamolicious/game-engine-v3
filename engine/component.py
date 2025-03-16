from __future__ import annotations


class Component: ...


class ComponentTemplate(Component):
    @classmethod
    def all_variations(cls) -> tuple[type[ComponentTemplate], ...]:
        return tuple(cls.__subclasses__())
