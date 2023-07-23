from datetime import timedelta
import datetime
from typing import List, Set
from collections import Counter

from snaps.snap import Snap
from common.descriptive_stats import DescriptiveStatsTimedelta

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

        self.__check_initialization_constraints(sending_users, receiving_users)

        self.snaps = sorted(snaps, key=lambda snap: snap.timestamp)
        self.users = sending_users

    def __check_initialization_constraints(self, sending_users: Set[str], receiving_users: Set[str]) -> None:
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
    
    def calculate_descriptive_response_stats_of_dominant_receiver(self) -> DescriptiveStatsTimedelta:
        pass



    
    #     """
#     Computes and returns the descriptive stats between the top person you send and receive snaps to/from.
#     The provided lists are expected to have the same top user from them meaning you send the most
#     snaps to the person who sends you the most. The descriptive stats include a minimum, average, and maximum amount of time
#     between you sending a snap or series of snaps and the receipient replying AND the receipient sending you a snap or
#     series of snaps and you replying.

#     :param sent_snaps: the snaps you have sent
#     :param received_snaps: the snaps you have received
#     """

#     top_to_user = filtering.get_top_username(sent_snaps, SnapDirection.RECEIVED)
#     top_from_user = filtering.get_top_username(received_snaps, SnapDirection.SENT)

#     if top_to_user != top_from_user:
#         raise AssertionError(f"Top from snapper must be equal to top to snapper, from sent and received snaps found that top sender was {top_from_user} while top receiver was {top_to_user}")

#     top_sent_to_snaps = filtering.get_snaps_by_user(sent_snaps, top_to_user, SnapDirection.RECEIVED)
#     top_received_from_snaps = filtering.get_snaps_by_user(received_snaps, top_from_user, SnapDirection.SENT)

#     all_top_snaps = top_sent_to_snaps + top_received_from_snaps
#     time_ordered = order_by_time_in_ascending_order(all_top_snaps)

#     current_sender = time_ordered[0].sender
#     current_time = time_ordered[0].timestamp
#     awaiting_response_periods: List[DateRange] = []

#     for snap in time_ordered:
#         if current_sender == snap.sender:
#             current_time = snap.timestamp
#             continue
#         else:
#             current_sender = snap.sender
#             new_time = snap.timestamp
#             awaiting_response_periods.append(DateRange(current_time, new_time))
#             current_time = new_time


#     awaiting_response_times = [p2.start_date - p1.end_date for p1, p2 in zip(awaiting_response_periods, awaiting_response_periods[1:])]

#     min_diff = min(awaiting_response_times)
#     max_diff = max(awaiting_response_times)
#     avg_diff = timedelta(seconds=mean([diff.total_seconds() for diff in awaiting_response_times]))

#     return DescriptiveStatsTimedelta(min_diff, avg_diff, max_diff)

    def calculate_descriptive_response_stats_of_dominant_sender(self) -> DescriptiveStatsTimedelta:
        pass
    
    def __str__(self):
        return f"SnapchatSnapConversation(users={self.users}, num_snaps={len(self.snaps)}, earliest_snap_date={self.get_earlier_snap_date()}, latest_snap_date={self.get_latest_snap_date()})"

    def __repr__(self):
        return self.__str__()