import os

BASENAME = os.path.basename(__file__)
VERSION_NUM = 2.0
LOGGING_HEADER = f"[{BASENAME} v{VERSION_NUM}]: "


def logpr(message):
    """
    Logging print.
    """

    # To be expanded.
    print(LOGGING_HEADER + str(message))
