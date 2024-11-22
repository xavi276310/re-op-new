from pydantic import BaseModel, Field
from typing import List, Optional

class SkillSuggestion(BaseModel):
    skill: str
    reason: str

class ContentRemoval(BaseModel):
    content: str
    reason: str

class ContentModification(BaseModel):
    original: str
    suggested: str
    reason: str

class ResumeAnalysis(BaseModel):
    skills_to_add: List[SkillSuggestion]
    content_to_remove: List[ContentRemoval]
    content_to_modify: List[ContentModification]

# 其他Pydantic模型... 