import {
  Box,
  Button,
  CssBaseline,
  IconButton,
  ThemeProvider,
  Tooltip,
  Typography,
  createTheme,
  useMediaQuery,
} from "@mui/material";
import { SetStateAction, useEffect, useRef, useState } from "react";
import SeparatorComponent from "./SeparatorComponent";
import ChooseFileRow from "./ChooseFileRow";

export default function App() {
  useEffect(() => {
    document.title = "SnapSimp";
  }, []);

  /**
   * The MUI theme for this web app.
   */
  const theme = createTheme({
    palette: {
      primary: {
        main: "#33a9dc",
      },
      secondary: {
        main: "#66bee5",
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
        src={require("./assets/Logo.png")}
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

  const [accountDataChosenFile, setAccountDataChosenFile] =
    useState<File | null>(null);

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
          background: "#151515",
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
            background: "#202020",
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
                fontFamily: "Teko",
                fontSize: "58px",
                userSelect: "none",
              }}
            >
              SnapSimp
            </Typography>
          </Box>
          <Box flex={1} />
        </Box>
        <SeparatorComponent
          text="Location Visualizer"
          widthPercentage={90}
          yPadding={20}
        />
        <SeparatorComponent
          text="JSON Export Tools"
          widthPercentage={90}
          yPadding={20}
        />
        <Box
          sx={{
            padding: "20px",
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "center",
            gap: "20px",
          }}
        >
          <Tooltip title="Export your snap_history.html data to JSON">
            <Button
              variant="contained"
              sx={{
                fontWeight: "bold",
                fontSize: "16px",
                textTransform: "none",
                color: "#0f0f0f",
              }}
            >
              Snap History
            </Button>
          </Tooltip>
          <Tooltip title="Export your chat_history.html data to JSON">
            <Button
              variant="contained"
              sx={{
                fontWeight: "bold",
                fontSize: "16px",
                textTransform: "none",
                color: "#0f0f0f",
              }}
            >
              Chat History
            </Button>
          </Tooltip>
        </Box>
        <ChooseFileRow
          buttonName={"Account Data"}
          buttonTooltip={"Export your account.html data to JSON"}
          noChosenFileLabel={"No account.html file chosen"}
          chosenFile={accountDataChosenFile}
          setChosenFile={setAccountDataChosenFile}
        />
        {/* <ChatComponent
            chats={ourConversation.chats}
            sendingUser="nathanvcheshire"
          /> */}
      </Box>
    </ThemeProvider>
  );
}
