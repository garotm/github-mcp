from enum import Enum


class IssueState(str, Enum):
    open = "open"
    closed = "closed"
    all = "all"


class PullRequestState(str, Enum):
    open = "open"
    closed = "closed"
    all = "all"
