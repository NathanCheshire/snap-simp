from typing import List, Set
from collections import Counter

from snaps.snap import Snap

class SnapchatSnapConversation:
    def __init__(self, snaps: List[Snap]):
        sending_users = {snap.sender for snap in snaps}
        receiving_users = {snap.receiver for snap in snaps}

        self.check_initialization_constraints(sending_users, receiving_users)

        self.snaps = sorted(snaps, key=lambda snap: snap.timestamp)
        self.users = sending_users

    def check_initialization_constraints(self, sending_users: Set[str], receiving_users: Set[str]) -> None:
        if len(sending_users) != 2 or len(receiving_users) != 2:
            raise AssertionError("All sent and received snaps must be from the same two users.")
        if sending_users != receiving_users:
            raise AssertionError("Sending users and receiving users must be the same.")

    def __str__(self):
        return f"SnapchatSnapConversation(users={self.users}, num_snaps={len(self.snaps)}, earliest_snap_date={self.get_earlier_snap_date()}, latest_snap_date={self.get_latest_snap_date()})"

    def __repr__(self):
        return self.__str__()

    def get_earlier_snap_date(self):
        return self.snaps[0].timestamp

    def get_latest_snap_date(self):
        return self.snaps[-1].timestamp

    def get_earliest_snap(self):
        return self.snaps[0]

    def get_latest_snap(self):
        return self.snaps[-1]

    def get_users(self):
        return self.users

    def get_dominant_sender(self):
        sender_counts = Counter([snap.sender for snap in self.snaps])
        return sender_counts.most_common(1)[0][0]

    def get_dominant_receiver(self):
        receiver_counts = Counter([snap.receiver for snap in self.snaps])
        return receiver_counts.most_common(1)[0][0]
    
    def get_conversation_duration(self):
        return self.get_latest_snap_date() - self.get_earlier_snap_date()

