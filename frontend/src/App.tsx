import {
  Box,
  CssBaseline,
  ThemeProvider,
  Typography,
  createTheme,
} from "@mui/material";
import ourChatsJson from "./darkneonshadows.json";
import ChatComponent from "./ChatMessage";

export default function App() {
  const ourConversation: SnapchatChatConversation = ourChatsJson;

  enum ChatType {
    MEDIA,
    CHAT,
  }

  /**
   * The MUI theme for this web app.
   */
  const theme = createTheme({
    palette: {
      primary: {
        main: "#5EBBF9",
      },
      background: {
        default: "#EFEFEF",
      },
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          "*": {
            boxSizing: "border-box",
            padding: 0,
            margin: 0,
            scrollBehavior: "smooth",
          },
          a: {
            color: "inherit",
            textDecoration: "none",
          },
        },
      },
    },
  });

  interface SnapchatChat {
    sender: string;
    receiver: string;
    type: string;
    text: string;
    timestamp: string;
  }

  interface SnapchatChatConversation {
    users: String[];
    chats: SnapchatChat[];
  }

  function generateMessagesBox() {
    return (
      <ThemeProvider theme={theme}>
        <Box
          className="custom-scrollbar"
          sx={{
            background: "#EFEFEF",
            scroll: "none",
            overflow: "hidden",
          }}
        >
          <CssBaseline />
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
            }}
          >
            <ChatComponent chats={ourConversation.chats} sendingUser="nathanvcheshire" />;
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  return generateMessagesBox();
}
