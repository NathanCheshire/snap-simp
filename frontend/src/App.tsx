import { Box, CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import SnapchatChatConversation from "./SnapchatChatConversation";
import ourChatsJson from "./darkneonshadows.json";
import ChatComponent from "./ChatComponent";

export default function App() {
  const ourConversation: SnapchatChatConversation = ourChatsJson;

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
            <ChatComponent
              chats={ourConversation.chats}
              sendingUser="nathanvcheshire"
            />
            ;
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  return generateMessagesBox();
}
