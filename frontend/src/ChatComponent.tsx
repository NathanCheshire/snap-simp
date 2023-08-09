import { Box, Typography } from "@mui/material";
import { ChatMessage } from "./ChatMessage";
import SnapchatChat from "./SnapchatChat";

export interface ChatComponentProps {
  chats: SnapchatChat[];
  sendingUser: string;
}

export default function ChatComponent({
  chats,
  sendingUser,
}: ChatComponentProps) {
  return (
    <Box
      style={{
        backgroundColor: "#1C1C1E",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          height: "80px",
          backgroundColor: "#303030",
          paddingBottom: "10px",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography
          sx={{
            color: "#f0f0f0",
            fontFamily: "Oswald",
            fontSize: "36px",
          }}
        >
          {chats[0].receiver === sendingUser
            ? chats[0].sender
            : chats[0].receiver}
        </Typography>
      </Box>
      <Box
        sx={{
          height: "calc(100vh - 80px)",
        }}
      >
        {chats.map((chat, index) => (
          <ChatMessage key={index} message={chat} sendingUser={sendingUser} />
        ))}
        ß
      </Box>
    </Box>
  );
}
