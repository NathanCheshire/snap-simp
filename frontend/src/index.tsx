import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import WebFont from "webfontloader";

WebFont.load({
  google: {
    families: ["Manrope", "Oswald", "Roboto", "Teko", "Caveat"],
  },
});

const rootElement = document.getElementById("root")!;
const reactRoot = ReactDOM.createRoot(rootElement);

reactRoot.render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
