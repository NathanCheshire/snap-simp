import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import { formatDistanceToNow } from "date-fns";

interface ChatMessageProps {
  message: {
    sender: string;
    receiver: string;
    type: string;
    text: string;
    timestamp: string;
  };
  sendingUser: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, sendingUser }) => {
  const isSendingUser = message.sender === sendingUser;

  return (
    <Box
      display="flex"
      paddingY='2px'
      justifyContent={isSendingUser ? "flex-end" : "flex-start"}
    >
      <Box
        sx={{
          padding: "10px",
          borderRadius: "14px",
          maxWidth: "75%",
          backgroundColor: isSendingUser ? "#0A74DA" : "#2C2C2E",
          color: isSendingUser ? "white" : "white",
        }}
      >
       
        {message.type === "MEDIA" ? (
          <Typography variant="body1">[Media]</Typography>
        ) : (
          <Typography variant="body1">{message.text}</Typography>
        )}
        <Typography
          variant="caption"
          style={{ display: "block", marginTop: "5px" }}
        >
          {formatDistanceToNow(new Date(message.timestamp))} ago
        </Typography>
      </Box>
    </Box>
  );
};

interface ChatComponentProps {
  chats: Array<{
    sender: string;
    receiver: string;
    type: string;
    text: string;
    timestamp: string;
  }>;
  sendingUser: string;
}

const ChatComponent: React.FC<ChatComponentProps> = ({
  chats,
  sendingUser,
}) => {
  return (
    <Box
      style={{
        backgroundColor: "#1C1C1E",
        padding: "10px",
        minHeight: "100vh",
      }}
    >
      {chats.map((chat, index) => (
        <ChatMessage key={index} message={chat} sendingUser={sendingUser} />
      ))}
    </Box>
  );
};

export default ChatComponent;
