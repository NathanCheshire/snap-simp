import {
  Box,
  CssBaseline,
  ThemeProvider,
  Typography,
  createTheme,
} from "@mui/material";
import SnapchatChatConversation from "./SnapchatChatConversation";
import ChatComponent from "./ChatComponent";

export default function App() {
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
          sx={{
            scroll: "none",
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: "100vw",
            height: "100vh",
            background: "#252525",
          }}
        >
          <CssBaseline />
          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              height: "80px",
              width: "100%",
              alignItems: "center",
              justifyContent: "space-between",
              scrollBehavior: "auto",
              overflowY: "scroll",
              "&::-webkit-scrollbar": {
                color: "#f0f0f0",
                width: "8px",
              },
              "&::-webkit-scrollbar-thumb": {
                backgroundColor: "#f0f0f0",
                borderRadius: "4px",
              },
              "&::-webkit-scrollbar-track": {
                backgroundColor: "transparent",
              },
              background: "#353535",
            }}
          >
            <Box paddingLeft='10px'>
              <Typography
                sx={{
                  color: "#f0f0f0",
                  fontWeight: "bold",
                  fontFamily: "Oswald",
                  fontSize: "32px",
                }}
              >
                SnapSimp - a Snapchat data analytics tool 
              </Typography>
            </Box>
          </Box>
          {/* <ChatComponent
            chats={ourConversation.chats}
            sendingUser="nathanvcheshire"
          /> */}
        </Box>
      </ThemeProvider>
    );
  }

  return generateMessagesBox();
}
