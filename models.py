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
    stargazerCount: int
    isFork: bool
    issues: Issues


class Repositories(BaseModel):
    nodes: list[RepositoryNode]


class OrganizationNode(BaseModel):
    avatarUrl: str
    name: str
    description: str | None = None
    url: str
    repositories: Repositories

    def __str__(self):
        return self.name


class Organizations(BaseModel):
    nodes: list[OrganizationNode]


class User(BaseModel):
    avatarUrl: str
    login: str
    name: str
    url: str
    repositories: Repositories
    organizations: Organizations

    def __str__(self):
        if self.login != self.name:
            return f"{self.login} ({self.name})"
        else:
            return self.login


class Data(BaseModel):
    user: User


class Extensions(BaseModel):
    saml_failure: bool


class Location(BaseModel):
    line: int
    column: int


class Error(BaseModel):
    type: str
    path: list[int | str]
    extensions: Extensions
    locations: list[Location]
    message: str


class ResponseModel(BaseModel):
    data: Data
    errors: list[Error] | None = None
