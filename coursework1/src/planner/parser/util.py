def predicate_args(text: str) -> list[str]:
    # args = text.strip(" ()").split(" ?")
    # args[0] = args[0].removeprefix("not (")
    # return args
    return text.strip(" ()").split(" ?")


def is_negated(text: str) -> bool:
    return text.strip(" ()").startswith("not (")


def parameter_items(text: str) -> tuple[str, str]:
    return zip(
        ("name", "type_str"),
        text.strip().split(" - ")
    )
