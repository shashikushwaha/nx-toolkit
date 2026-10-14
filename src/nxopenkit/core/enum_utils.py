
def get_enum_name(enum_cls, member) -> str:
    return next(
        (
            name
            for name, value in vars(enum_cls).items()
            if value == member
        ),
        str(member),
    )