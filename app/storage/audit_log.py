import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from app.config import get_settings


def _get_audit_path() -> Path:
    settings = get_settings()
    path = Path(settings.audit_log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_audit_log() -> List[Dict[str, Any]]:
    path = _get_audit_path()

    if not path.exists():
        return []

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def write_audit_event(event: Dict[str, Any]) -> Dict[str, Any]:
    events = read_audit_log()

    event_with_timestamp = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }

    events.append(event_with_timestamp)

    path = _get_audit_path()
    path.write_text(json.dumps(events, indent=2), encoding="utf-8")

    return event_with_timestamp


def get_workflow_events(workflow_id: str) -> List[Dict[str, Any]]:
    return [
        event
        for event in read_audit_log()
        if event.get("workflow_id") == workflow_id
    ]