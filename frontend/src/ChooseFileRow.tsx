import { Box, Tooltip, Typography, IconButton, Button } from "@mui/material";
import { SetStateAction, Dispatch, useRef } from "react";
import DeleteIcon from "@mui/icons-material/Delete";

export interface ChooseFileRowProps {
  buttonName: string;
  buttonTooltip: string;
  noChosenFileLabel: string;
  chosenFile: File | null;
  setChosenFile: Dispatch<SetStateAction<File | null>>;
}

export default function ChooseFileRow({
  buttonName,
  buttonTooltip,
  noChosenFileLabel,
  chosenFile,
  setChosenFile,
}: ChooseFileRowProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const onAccountDataInputChanged = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files && event.target.files[0];
    setChosenFile(file);
  };

  const accountDataInput = (
    <input
      type="file"
      ref={inputRef}
      style={{ display: "none" }}
      accept=".html"
      onChange={onAccountDataInputChanged}
    />
  );

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: "10px",
      }}
    >
      <Tooltip title={buttonTooltip}>
        <Button
          onClick={() => {
            if (inputRef.current) {
              inputRef.current.click();
            }
          }}
          variant="contained"
          sx={{
            fontWeight: "bold",
            fontSize: "16px",
            textTransform: "none",
            color: "#0f0f0f",
          }}
        >
          {buttonName}
        </Button>
      </Tooltip>
      {accountDataInput}
      <Box width="10px" />
      <Typography
        sx={{
          fontFamily: "Oswald",
          fontSize: "18px",
          fontWeight: "bold",
          textAlign: "center",
          userSelect: "none",
          color: "#f0f0f0",
        }}
      >
        {chosenFile?.name ?? noChosenFileLabel}
      </Typography>
      {chosenFile?.name && (
        <IconButton
          onClick={() => {
            setChosenFile(null);
          }}
          sx={{
            color: "#f0f0f0",
            size: "md",
          }}
        >
          <DeleteIcon />
        </IconButton>
      )}
    </Box>
  );
}
