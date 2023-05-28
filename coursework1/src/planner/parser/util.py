def predicate_args(text: str) -> list[str]:
    return text.strip(" ()").split(" ?")


def split_string(lines: str) -> list[str]:
    return lines.strip().split("\n")


# def is_negated(text: str) -> bool:
#     return text.strip(" ()").startswith("not (")
#
#
# def parameter_items(text: str) -> tuple[str, str]:
#     return zip(
#         ("name", "type_str"),
#         text.strip().split(" - ")
#     )
