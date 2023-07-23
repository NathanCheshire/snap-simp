from datetime import timedelta
import datetime
from typing import List, Optional, Set
from collections import Counter

from snaps.snap import Snap

class SnapchatSnapConversation:
    """
    A snapchat snap conversation stores a list of snaps between two users for a designated period of time.
    """

    def __init__(self, snaps: List[Snap]):
        """
        Initialize a SnapchatSnapConversation instance.
        
        :param snaps: the list of Snap objects for this conversation
        It is expected that this list contains snaps between two and only two users
        """
        sending_users = {snap.sender for snap in snaps}
        receiving_users = {snap.receiver for snap in snaps}

        self.check_initialization_constraints(sending_users, receiving_users)

        self.snaps = sorted(snaps, key=lambda snap: snap.timestamp)
        self.users = sending_users

    def check_initialization_constraints(self, sending_users: Set[str], receiving_users: Set[str]) -> None:
        """
        Checks if the provided users are valid for the conversation. The conversation must be between two users.
        
        :param sending_users: the set of users who sent snaps
        :param receiving_users: the set of users who received snaps
        """
        if len(sending_users) != 2 or len(receiving_users) != 2:
            raise AssertionError("All sent and received snaps must be from the same two users.")
        if sending_users != receiving_users:
            raise AssertionError("Sending users and receiving users must be the same.")

    def get_earlist_snap_date(self) -> datetime:
        """
        Returns the earliest snap date of this conversation.

        :return: the earliest snap date of this conversation
        """
        return self.snaps[0].timestamp

    def get_latest_snap_date(self) -> datetime:
        """
        Returns the lastest snap date of this conversation.

        :return: the latest snap date of this conversation
        """
        return self.snaps[-1].timestamp

    def get_earliest_snap(self) -> Snap:
        """
        Returns the earliest snap of this conversation.

        :return: the earliest snap of this conversation
        """
        return self.snaps[0]

    def get_latest_snap(self) -> Snap:
        """
        Returns the latest snap of this conversation.

        :return: the earliest snap of this conversation
        """
        return self.snaps[-1]

    def get_users(self) -> List[str]:
        """
        Returns the list of the users this conversation belongs to.

        :return: a list of the users this conversation belongs to
        """
        return list(self.users)

    def get_dominant_sender(self) -> str:
        """
        Returns the dominant sender of this conversation.

        :return: the dominant sender of this conversation
        """
        sender_counts = Counter([snap.sender for snap in self.snaps])
        return sender_counts.most_common(1)[0][0]

    def get_dominant_receiver(self) -> str:
        """
        Returns the dominant receiver of this conversation.

        :return: the dominant receiver of this conversation
        """
        receiver_counts = Counter([snap.receiver for snap in self.snaps])
        return receiver_counts.most_common(1)[0][0]
    
    def get_conversation_duration(self) -> timedelta:
        """
        Returns the duration of the conversation.

        :return: a timedelta object representing the duration of the conversation.
        """
        return self.get_latest_snap_date() - self.get_earlier_snap_date()

    def get_num_snaps_sent_by_dominant_sender(self) -> int:
        """
        Returns the number of snaps sent by the dominant sender within this conversation.

        :return: the number of snaps sent by the dominant sender within this conversation
        """
        dominant_sender = self.get_dominant_sender()
        return len([snap for snap in self.snaps if snap.sender == dominant_sender])

    def get_num_snaps_sent_by_dominant_receiver(self) -> int:
        """
        Returns the number of snaps sent by the dominant receiver within this conversation.

        :return: the number of snaps sent by the dominant receiver within this conversation
        """
        dominant_receiver = self.get_dominant_receiver()
        return len([snap for snap in self.snaps if snap.sender == dominant_receiver])

    def get_num_snaps_received_by_dominant_sender(self) -> int:
        """
        Returns the number of snaps received by the dominant sender within this conversation.

        :return: the number of snaps received by the dominant sender within this conversation
        """
        dominant_sender = self.get_dominant_sender()
        return len([snap for snap in self.snaps if snap.receiver == dominant_sender])

    def get_num_snaps_received_by_dominant_receiver(self) -> int:
        """
        Returns the number of snaps received by the dominant receiver within this conversation.

        :return: the number of snaps received by the dominant receiver within this conversation
        """
        dominant_receiver = self.get_dominant_receiver()
        return len([snap for snap in self.snaps if snap.receiver == dominant_receiver])

    def get_sent_snaps_by_user(self, username: str) -> List[Snap]:
        """
        Returns the snaps sent by the provided user within this conversation.

        :return: the snaps sent by the provided user
        """
        if username not in self.users:
            raise AssertionError(f"\"{username}\" is not a part of this conversation.")

        return [snap for snap in self.snaps if snap.sender == username]
    
    def get_received_snaps_by_user(self, username: str) -> List[Snap]:
        """
        Returns the snaps received by the provided user within this conversation.

        :return: the snaps received by the provided user
        """
        if username not in self.users:
            raise AssertionError(f"\"{username}\" is not a part of this conversation.")

        return [snap for snap in self.snaps if snap.receiver == username]

    def get_num_snaps_sent_by_user(self, username: str) -> int:
        """
        Returns the number of snaps sent by the provided user within this conversation.

        :return: the number of snaps sent by the provided user within this conversation
        """
        sent_snaps_by_user = self.get_sent_snaps_by_user(username)
        return len(sent_snaps_by_user) if sent_snaps_by_user else 0
    
    def get_num_snaps_sent_by_user(self, username: str) -> int:
        """
        Returns the number of snaps received by the provided user within this conversation.

        :return: the number of snaps received by the provided user within this conversation
        """
        received_snaps_by_user = self.get_received_snaps_by_user(username)
        return len(received_snaps_by_user) if received_snaps_by_user else 0
    
    def __str__(self):
        return f"SnapchatSnapConversation(users={self.users}, num_snaps={len(self.snaps)}, earliest_snap_date={self.get_earlier_snap_date()}, latest_snap_date={self.get_latest_snap_date()})"

    def __repr__(self):
        return self.__str__()