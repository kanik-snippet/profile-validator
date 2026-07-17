from dataclasses import dataclass, field


@dataclass
class ApplicationState:
    """Global application state."""

    initialized: bool = False
    is_running: bool = False
    shutdown_requested: bool = False

    active_jobs: int = 0
    active_profiles: int = 0
    queue_size: int = 0

    running_job_id: str | None = None

    statistics: dict = field(default_factory=dict)


application_state = ApplicationState()