import {
  Box,
  Tooltip,
  Typography,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { SetStateAction, Dispatch, useRef, useState } from "react";
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
  const [removeConfirmationModalOpen, setRemoveConfirmationModalOpen] =
    useState<boolean>(false);

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
        padding: "10px",
      }}
    >
      <Dialog
        open={removeConfirmationModalOpen}
        onClose={() => {
          setRemoveConfirmationModalOpen(false);
        }}
      >
        <DialogTitle>Remove File Confirmation</DialogTitle>
        <DialogContent>
          Are you sure you want to remove this file? This action cannot be
          undone.
        </DialogContent>
        <DialogActions>
          <Button
            sx={{
              fontWeight: "bold",
              textTransform: "none",
            }}
            variant="contained"
            onClick={() => {
              setRemoveConfirmationModalOpen(false);
            }}
          >
            Keep
          </Button>
          <Button
            sx={{
              fontWeight: "bold",
              textTransform: "none",
            }}
            color="error"
            variant="contained"
            onClick={() => {
              setRemoveConfirmationModalOpen(false);
              setChosenFile(null);
            }}
          >
            Remove
          </Button>
        </DialogActions>
      </Dialog>
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
            setRemoveConfirmationModalOpen(true);
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
