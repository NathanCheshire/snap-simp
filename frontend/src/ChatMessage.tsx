import { Box, Typography } from "@mui/material";
import { formatDistanceToNow } from "date-fns";
import SnapchatChat from "./SnapchatChat";

export interface ChatMessageProps {
  message: SnapchatChat;
  sendingUser: string;
}

export function ChatMessage ({ message, sendingUser }: ChatMessageProps)  {
  const isSendingUser = message.sender === sendingUser;

  return (
    <Box
      display="flex"
      paddingY="2px"
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
