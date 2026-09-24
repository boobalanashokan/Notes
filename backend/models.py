from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Topic(BaseModel):
    id: str
    name: str
    week: int
    type: str
    subtopics: List[str] = Field(default_factory=list)
    learning_outcome: str
    project_task: str
    depends_on: List[str] = Field(default_factory=list)
    done: bool = False


class Area(BaseModel):
    id: str
    name: str
    topics: List[Topic] = Field(default_factory=list)


class Track(BaseModel):
    id: str
    name: str
    areas: List[Area] = Field(default_factory=list)


class Roadmap(BaseModel):
    tracks: List[Track] = Field(default_factory=list)
