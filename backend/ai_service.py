import json
import os
from typing import Any
from urllib import error, request

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def _normalize_json_text(raw_text: str) -> str:
    cleaned = (raw_text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
        cleaned = cleaned.strip()
    return cleaned


def _gemini_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def _build_prompt(track: Any, stats: dict[str, Any]) -> str:
    upcoming_topics: list[str] = []
    for area in getattr(track, "areas", []) or []:
        for topic in getattr(area, "topics", []) or []:
            if not getattr(topic, "done", False):
                upcoming_topics.append(f"- {topic.name} ({area.name}, Week {topic.week})")

    next_topics = "\n".join(upcoming_topics[:6]) if upcoming_topics else "- No pending topics remain."

    area_rows = stats.get("areas") or []
    area_snapshot = []
    for area in area_rows:
        if isinstance(area, dict):
            area_name = area.get("area_name") or "Unknown area"
            completed = area.get("completed_topics")
            total = area.get("total_topics")
            percent_complete = area.get("percent_complete", 0)
        else:
            area_name = getattr(area, "area_name", getattr(area, "name", "Unknown area"))
            completed = getattr(area, "completed_topics", None)
            total = getattr(area, "total_topics", None)
            percent_complete = getattr(area, "percent_complete", 0)

        area_snapshot.append(
            {
                "area": area_name,
                "completed": completed,
                "total": total,
                "percent_complete": percent_complete,
            }
        )

    areas_snapshot = json.dumps(area_snapshot, ensure_ascii=False, indent=2)

    return f"""
You are an encouraging study coach. Analyze the learner's progress and return valid JSON only.

Track name: {track.name}
Progress: {stats.get('percent_complete', 0)}%
Completed topics: {stats.get('completed_topics', 0)}
Remaining topics: {stats.get('remaining_topics', 0)}

Focus areas:
{areas_snapshot}

Upcoming topics:
{next_topics}

Return JSON with exactly these keys:
{{
  "summary": "2-3 sentence coaching summary",
  "focus_areas": ["short actionable area 1", "short actionable area 2", "short actionable area 3"],
  "next_actions": ["actionable next step 1", "actionable next step 2", "actionable next step 3"]
}}
"""


def _call_gemini(prompt: str) -> dict[str, Any]:
    api_key = _gemini_api_key()
    if not api_key:
        raise RuntimeError("Gemini API is not configured. Add GEMINI_API_KEY or GOOGLE_API_KEY in your environment/secret store.")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.45,
            "topP": 0.9,
            "topK": 32,
            "responseMimeType": "application/json",
        },
    }
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        payload_error = exc.read().decode("utf-8", "replace")
        try:
            parsed_error = json.loads(payload_error)
            message = parsed_error.get("error", {}).get("message", payload_error)
        except json.JSONDecodeError:
            message = payload_error
        raise RuntimeError(message) from exc

    candidates = body.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no response for the study coach prompt.")

    parts = candidates[0].get("content", {}).get("parts") or []
    raw_text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
    if not raw_text:
        raise RuntimeError("Gemini returned an empty response for the study coach prompt.")

    cleaned = _normalize_json_text(raw_text)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned a non-JSON response for the study coach prompt.") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError("Gemini returned an unexpected payload format for the study coach prompt.")

    return parsed


def _fallback_guidance(track: Any, stats: dict[str, Any]) -> dict[str, Any]:
    completed = stats.get("completed_topics", 0)
    remaining = stats.get("remaining_topics", 0)
    progress = stats.get("percent_complete", 0)
    track_name = getattr(track, "name", "your track")

    summary = (
        f"You are {progress}% through {track_name}. "
        f"Keep the momentum going with a short, focused study block."
    )
    focus_areas = [
        "Review the most recent completed topic before moving on.",
        "Complete the next unfinished topic in your current queue.",
        "Keep daily progress consistent, even for a short study session.",
    ]
    next_actions = [
        f"Finish the next {remaining or 'remaining'} topic in {track_name}.",
        "Revisit yesterday's notes and summarize the key takeaway.",
        f"Aim for one focused session to move from {completed} completed topics to a stronger finish.",
    ]
    return {
        "summary": summary,
        "focus_areas": focus_areas,
        "next_actions": next_actions,
    }


def generate_track_guidance(track: Any, stats: dict[str, Any]) -> dict[str, Any]:
    try:
        prompt = _build_prompt(track, stats)
        result = _call_gemini(prompt)
    except Exception:
        return _fallback_guidance(track, stats)

    summary = str(result.get("summary") or "You are on the right track. Keep building momentum with the next topic in your queue.")
    focus_areas = result.get("focus_areas") or []
    next_actions = result.get("next_actions") or []

    if not isinstance(focus_areas, list):
        focus_areas = []
    if not isinstance(next_actions, list):
        next_actions = []

    return {
        "summary": summary,
        "focus_areas": [str(item) for item in focus_areas[:3]],
        "next_actions": [str(item) for item in next_actions[:3]],
    }
