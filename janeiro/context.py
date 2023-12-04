from dataclasses import dataclass

_APP_CONTEXT: "_AppContext"


@dataclass
class _AppContext:
    app_name: str


def set_app_context(**app_context):
    global _APP_CONTEXT

    _APP_CONTEXT = _AppContext(**app_context)


def get_app_context() -> _AppContext:
    try:
        return _APP_CONTEXT
    except NameError:
        raise Exception("App context is not initialized!")
