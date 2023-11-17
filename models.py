from __future__ import annotations
from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel


class Author(BaseModel):
    login: str


class LabelNode(BaseModel):
    name: str
    color: str


class Labels(BaseModel):
    nodes: List[LabelNode]


class IssueNode(BaseModel):
    title: str
    author: Author
    url: str
    labels: Labels
    updatedAt: datetime


class Issues(BaseModel):
    nodes: List[IssueNode]


class RepositoryNode(BaseModel):
    name: str
    description: Optional[str]
    url: str
    updatedAt: datetime
    issues: Issues


class Repositories(BaseModel):
    nodes: List[RepositoryNode]


class OrganizationNode(BaseModel):
    avatarUrl: str
    name: str
    description: Optional[str]
    url: str
    repositories: Repositories


class Organizations(BaseModel):
    nodes: List[OrganizationNode]


class User(BaseModel):
    organizations: Organizations


class Data(BaseModel):
    user: User


class ResponseModel(BaseModel):
    data: Data
