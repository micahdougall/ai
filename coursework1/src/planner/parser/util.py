import re


def predicate_args(text: str) -> list[str]:
    """Splits a string of predicate arguments"""
    return text.strip(" ()").split(" ?")


def split_string(lines: str) -> list[str]:
    """Splits lines of arguments"""
    return lines.strip().split("\n")


def split_negated(text: str) -> list[str]:
    """Splits a string of parameter arguments"""
    regx_split = re.compile(r" (?!\()")
    return regx_split.split(text.strip(" ()"))
