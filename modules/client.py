class Authorization:
    """
    Authorization
    """

    token: str = (
        "MTE2ODM1MTkzNzMzOTU5NjgzMQ.GB8nod.NLDmVnrqxzmDghEyyot47VW_y3FhF4fbx1msdM"
    )
    secret: str = "M37HfDPVtAfcODU2SaCRwjI8c-MAm4X8"
    prefix: str = "!"
    url: str = "https://discord.gg/8T7S9GFpVN"
    owner_ids: list = [
        1181236538386948116,
    ] # Owner IDS, LIST

    class channels:
        farm: int = 1181237485007810630

    class roles:
        """
        Server roles
        """

        client: int = 1168351937339596831
        premium: int = 1181237902496256041
        plat: int = 1181238036315504660
        gold: int = 1181238145103175711
        silver: int = 1181238247247069254
        bronze: int = 1181238311201820704
        member: int = 1181238385789128755

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
