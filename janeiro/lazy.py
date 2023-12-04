import importlib
from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class LazyImportTarget(Generic[T]):
    module_path: str = None
    module_target: List[str] = field(default_factory=list)

    def do_import(self) -> T:
        value = importlib.import_module(self.module_path)
        for target in self.module_target:
            if target.endswith("()"):
                is_callable = True
                target = target[:-2]
            else:
                is_callable = False

            value = getattr(value, target)
            if is_callable:
                value = value()

        return value

    @staticmethod
    def from_ref(ref: str):
        target = LazyImportTarget()

        if ":" in ref:
            target.module_path, module_ref = ref.split(":")
        else:
            target.module_path = ref
            module_ref = None

        if module_ref:
            target.module_target = module_ref.split(".")

        return target
