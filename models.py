from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Author(BaseModel):
    login: str


class LabelNode(BaseModel):
    name: str
    color: str


class Labels(BaseModel):
    nodes: list[LabelNode]


class IssueNode(BaseModel):
    title: str
    author: Author
    url: str
    labels: Labels
    updatedAt: datetime


class Issues(BaseModel):
    nodes: list[IssueNode]


class RepositoryNode(BaseModel):
    name: str
    description: str | None
    url: str
    updatedAt: datetime
    issues: Issues


class Repositories(BaseModel):
    nodes: list[RepositoryNode]


class OrganizationNode(BaseModel):
    avatarUrl: str
    name: str
    description: str | None
    url: str
    repositories: Repositories


class Organizations(BaseModel):
    nodes: list[OrganizationNode]


class User(BaseModel):
    organizations: Organizations


class Data(BaseModel):
    user: User


class ResponseModel(BaseModel):
    data: Data