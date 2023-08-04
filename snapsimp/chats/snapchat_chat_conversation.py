from datetime import timedelta, datetime
import json
from statistics import mean
from typing import List, Set
from collections import Counter

from chats.chat import Chat
from common.descriptive_stats import DescriptiveStatsTimedelta
from chats.chat_type import ChatType
from chats.chat_helpers import json_chat_encoder
from common.json_constants import INDENT


class SnapchatChatConversation:
    """
    A snapchat chat conversation stores a list of chats between two users for a designated period of time.
    """

    def __init__(self, chats: List[Chat]):
        """
        Initializes a SnapchatChatConversation instance.

        :param chats: the list of Chat objects for this conversation.
        It is expected that this list contains chats between two and only two users
        """
        sending_users = {chat.sender for chat in chats}
        receiving_users = {chat.receiver for chat in chats}

        self.__check_initialization_constraints(sending_users, receiving_users)

        self.chats = sorted(chats, key=lambda chat: chat.timestamp)
        self.users = sending_users.union(receiving_users)

    def __check_initialization_constraints(
        self, sending_users: Set[str], receiving_users: Set[str]
    ) -> None:
        """
        Checks if the provided users are valid for the conversation. The conversation must be between two users.

        :param sending_users: the set of users who sent chats
        :param receiving_users: the set of users who received chats
        """
        if len(sending_users) > 2 or len(receiving_users) > 2:
            raise AssertionError(
                f"All sent and received chats must be from the same two users. sending={sending_users}, receiving={receiving_users}"
            )
        if len(sending_users.union(receiving_users)) > 2:
            raise AssertionError("Sending users and receiving users must be the same.")

    def get_earlist_chat_date(self) -> datetime:
        """
        Returns the earliest chat date of this conversation.

        :return: the earliest chat date of this conversation
        """
        return self.chats[0].timestamp

    def get_latest_chat_date(self) -> datetime:
        """
        Returns the lastest chat date of this conversation.

        :return: the latest chat date of this conversation
        """
        return self.chats[-1].timestamp

    def get_earliest_chat(self) -> Chat:
        """
        Returns the earliest chat of this conversation.

        :return: the earliest chat of this conversation
        """
        return self.chats[0]

    def get_latest_chat(self) -> Chat:
        """
        Returns the latest chat of this conversation.

        :return: the earliest chat of this conversation
        """
        return self.chats[-1]

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
        sender_counts = Counter([chat.sender for chat in self.chats])
        return sender_counts.most_common(1)[0][0]

    def get_dominant_receiver(self) -> str:
        """
        Returns the dominant receiver of this conversation.

        :return: the dominant receiver of this conversation
        """
        receiver_counts = Counter([chat.receiver for chat in self.chats])
        return receiver_counts.most_common(1)[0][0]

    def get_conversation_duration(self) -> timedelta:
        """
        Returns the duration of the conversation.

        :return: a timedelta object representing the duration of the conversation.
        """
        return self.get_latest_chat_date() - self.get_earlist_chat_date()

    def get_num_chats_sent_by_dominant_sender(self) -> int:
        """
        Returns the number of chats sent by the dominant sender within this conversation.

        :return: the number of chats sent by the dominant sender within this conversation
        """
        dominant_sender = self.get_dominant_sender()
        return len([chat for chat in self.chats if chat.sender == dominant_sender])

    def get_num_chats_sent_by_dominant_receiver(self) -> int:
        """
        Returns the number of chats sent by the dominant receiver within this conversation.

        :return: the number of chats sent by the dominant receiver within this conversation
        """
        dominant_receiver = self.get_dominant_receiver()
        return len([chat for chat in self.chats if chat.sender == dominant_receiver])

    def get_num_chats_received_by_dominant_sender(self) -> int:
        """
        Returns the number of chats received by the dominant sender within this conversation.

        :return: the number of chats received by the dominant sender within this conversation
        """
        dominant_sender = self.get_dominant_sender()
        return len([chat for chat in self.chats if chat.receiver == dominant_sender])

    def get_num_chats_received_by_dominant_receiver(self) -> int:
        """
        Returns the number of chats received by the dominant receiver within this conversation.

        :return: the number of chats received by the dominant receiver within this conversation
        """
        dominant_receiver = self.get_dominant_receiver()
        return len([chat for chat in self.chats if chat.receiver == dominant_receiver])

    def get_sent_chats_by_user(self, username: str) -> List[Chat]:
        """
        Returns the chats sent by the provided user within this conversation.

        :return: the chats sent by the provided user
        """
        if username not in self.users:
            raise AssertionError(f'"{username}" is not a part of this conversation.')

        return [chat for chat in self.chats if chat.sender == username]

    def get_received_chats_by_user(self, username: str) -> List[Chat]:
        """
        Returns the chats received by the provided user within this conversation.

        :return: the chats received by the provided user
        """
        if username not in self.users:
            raise AssertionError(f'"{username}" is not a part of this conversation.')

        return [chat for chat in self.chats if chat.receiver == username]

    def get_num_chats_received_by_user(self, username: str) -> int:
        """
        Returns the number of chats sent by the provided user within this conversation.

        :return: the number of chats sent by the provided user within this conversation
        """
        sent_chats_by_user = self.get_sent_chats_by_user(username)
        return len(sent_chats_by_user) if sent_chats_by_user else 0

    def get_num_chats_received_by_user(self, username: str) -> int:
        """
        Returns the number of chats received by the provided user within this conversation.

        :return: the number of chats received by the provided user within this conversation
        """
        received_chats_by_user = self.get_received_chats_by_user(username)
        return len(received_chats_by_user) if received_chats_by_user else 0

    def __get_switching_chats(self) -> List[Chat]:
        switching_chats = []

        for i in range(len(self.chats) - 1):
            current_chat = self.chats[i]
            next_chat = self.chats[i + 1]

            if current_chat.sender != next_chat.sender:
                switching_chats.append(current_chat)

        switching_chats.append(self.chats[-1])

        return switching_chats

    def calculate_descriptive_response_stats_of_receiver(
        self, receiver: str
    ) -> DescriptiveStatsTimedelta:
        """
        Computes and returns the descriptive stats for the provided receiver. Namely, the minimum, average, and maximum
        time taken before they respond to the other person's chats.

        :param receiver: the username of the receiver
        """

        if receiver not in self.users:
            raise AssertionError(f"{receiver} should be in list of users: {self.users}")

        latest_chats_before_sender_switch = self.__get_switching_chats()

        # Extract the timestamps of chats sent by the receiver
        receiver_chat_times = [
            chat.timestamp
            for chat in latest_chats_before_sender_switch
            if chat.sender == receiver
        ]
        # Pair each chat time with the next one (if it exists)
        paired_chat_times = list(zip(receiver_chat_times, receiver_chat_times[1:]))
        # Compute the time differences
        awaiting_response_times = [(t2 - t1) for t1, t2 in paired_chat_times]

        min_diff = min(awaiting_response_times)
        max_diff = max(awaiting_response_times)
        avg_diff = timedelta(
            seconds=mean([diff.total_seconds() for diff in awaiting_response_times])
        )

        return DescriptiveStatsTimedelta(min_diff, avg_diff, max_diff)

    def print_formatted_conversation(self):
        last_sender = None
        for chat in self.chats:
            if chat.type == ChatType.MEDIA:
                continue
            elif len(chat.text.strip()) == 0:
                continue

            if last_sender == chat.sender:
                print(chat.timestamp, ": ", chat.text)
            else:
                print(chat.sender)
                print(chat.timestamp, ': "', chat.text, '"')
            last_sender = chat.sender
            print()

    def to_json(self, file_path):
        """
        Saves the chat conversation to a JSON file.

        :param file_path: the path to the JSON file
        """

        chats_list = [
            {
                "sender": chat.sender,
                "receiver": chat.receiver,
                "type": chat.type,
                "text": chat.text,
                "timestamp": chat.timestamp,
            }
            for chat in self.chats
        ]

        conversation_dict = {
            "users": list(self.users),
            "chats": chats_list,
        }

        with open(file_path, "w") as f:
            json.dump(conversation_dict, f, default=json_chat_encoder, indent=INDENT)

    def __str__(self):
        return f"SnapchatChatConversation(users={self.users}, num_chats={len(self.chats)}, earliest_chat_date={self.get_earlist_chat_date()}, latest_chat_date={self.get_latest_chat_date()})"

    def __repr__(self):
        return self.__str__()
