from common.snap_simp_enum import SnapSimpEnum


class ChatHistoryTableColumnIndicie(SnapSimpEnum):
    """
    Indicies for extracting information from a particular chat history table row containing multiple cells.
    """

    SENDER = 0
    TYPE = 1
    TIME_STAMP = 2
