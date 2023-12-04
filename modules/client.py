class Authorization:
    """
    Authorization
    """

    token: str = (
        "MTE2ODM1MTkzNzMzOTU5NjgzMQ.GB8nod.NLDmVnrqxzmDghEyyot47VW_y3FhF4fbx1msdM"
    )
    secret: str = "Client secret"
    prefix: str = "."
    url: str = "https://discord.gg/fastly"
    owner_ids: list = [
        1163131417417494638,
    ] # Owner IDS, LIST

    class channels:
        farm: int = 1163370501507403847

    class roles:
        """
        Server roles
        """

        client: int = 1163370501507403847
        premium: int = 1163366415273832518
        plat: int = 1163366124944105492
        gold: int = 1163366081977647124
        silver: int = 1163366082648748053
        bronze: int = 1163366073685528637
        member: int = 1163346512273735750

    class db:
        """
        Database information
        """

        host: str = ""
        user: str = ""
        port: int = 5432
        password: str = ""
        database: str = ""


class Color:
    """
    Color class for colors
    """

    normal: int = 0x090909
    red: int = 0xFF0000
    green: int = 0x00FF00
    blurple: int = 0x7200FF
