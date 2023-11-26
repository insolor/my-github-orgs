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


# class IssueNode(BaseModel):
#     title: str
#     author: Author
#     url: str
#     labels: Labels
#     updatedAt: datetime


class Issues(BaseModel):
    # nodes: list[IssueNode]
    totalCount: int


class RepositoryNode(BaseModel):
    name: str
    nameWithOwner: str
    description: str | None
    url: str
    updatedAt: datetime | None = None
    pushedAt: datetime | None = None
    stargazerCount: int
    issues: Issues | None = None
    parent: RepositoryNode | None = None


class Repositories(BaseModel):
    nodes: list[RepositoryNode]


class OrganizationNode(BaseModel):
    avatarUrl: str
    login: str
    name: str
    description: str | None = None
    url: str
    repositories: Repositories

    def __str__(self):
        if self.login != self.name:
            return f"{self.login} ({self.name})"
        else:
            return self.login


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
    saml_failure: bool | None = None


class Location(BaseModel):
    line: int
    column: int


class Error(BaseModel):
    type: str | None = None
    path: list[int | str] | None = None
    extensions: Extensions
    locations: list[Location]
    message: str


class ResponseModel(BaseModel):
    data: Data | None = None
    errors: list[Error] | None = None
