import {
  Box,
  CssBaseline,
  ThemeProvider,
  Typography,
  createTheme,
  useMediaQuery,
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

  /**
   * Whether a larger font for the navbar left name component can be used.
   */
  const canShowLargeName = useMediaQuery("(min-width:850px)");

  /**
   * The navbar logo component.
   */
  const logo = (
    <Box
      sx={{
        maxWidth: canShowLargeName ? "80px" : "60px",
        maxHeight: canShowLargeName ? "80px" : "60px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#0f0f0f",
        padding: "10px",
        borderRadius: "12px",
        userSelect: "none",
        transform: "rotate(0deg)",
      }}
    >
      <img
        alt="Nathan"
        src={require("./Logo.png")}
        style={{
          width: "100%",
          height: "auto",
          display: "block",
          maxWidth: "100%",
          borderRadius: "20px",
          transform: "scaleX(-1)",
        }}
      />
    </Box>
  );

  // todo where to put this?
  const scrollAttributes = {
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
  };

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
            height: "90px",
            width: "100%",
            alignItems: "center",
            justifyContent: "space-between",
            background: "#353535",
          }}
        >
          <Box paddingLeft="10px" flex={1}>
            {logo}
          </Box>
          <Box
            paddingRight="10px"
            flex={1}
            display="flex"
            alignItems={"center"}
            justifyContent={"center"}
          >
            <Typography
              sx={{
                color: "#f0f0f0",
                fontWeight: "bold",
                fontFamily: "Oswald",
                fontSize: "44px",
                userSelect: "none",
              }}
            >
              SnapSimp
            </Typography>
          </Box>
          <Box flex={1} />
        </Box>
        {/* <ChatComponent
            chats={ourConversation.chats}
            sendingUser="nathanvcheshire"
          /> */}
      </Box>
    </ThemeProvider>
  );
}
