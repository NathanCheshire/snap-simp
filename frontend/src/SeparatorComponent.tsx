import { Box, Typography } from "@mui/material";

export interface SeparatorComponentProps {
  text: string;
  widthPercentage: number;
  yPadding?: number;
}

export default function SeparatorComponent({
  text,
  widthPercentage,
  yPadding,
}: SeparatorComponentProps) {
  return (
    <Box
      sx={{
        width: `${widthPercentage}%`,
        alignItems: "center",
        justifyContent: "center",
        display: "flex",
        flexDirection: "column",
        paddingY: `${yPadding}px` ?? "auto",
      }}
    >
      <Typography
        sx={{
          color: "#f0f0f0",
          fontSize: "22px",
          fontWeight: "bold",
          fontFamily: "Oswald",
        }}
      >
        {text}
      </Typography>
      <Box
        sx={{
          width: `${widthPercentage}%`,
          height: "3px",
          borderRadius: "3px",
          backgroundColor: "#f0f0f0",
        }}
      />
    </Box>
  );
}
