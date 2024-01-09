#!/usr/bin/env python3

import os

BASENAME = os.path.basename(__file__)  # Prints the basename of the file where logpr is called.
VERSION_NUM = 2.0
LOGGING_HEADER = f"[{BASENAME} v{VERSION_NUM}]: "


def logpr(message):
    """
    Logging print.
    """

    # To be expanded.
    print(LOGGING_HEADER + str(message))
