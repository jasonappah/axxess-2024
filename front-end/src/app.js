import React from "react";
import { render } from "react-dom";

import { ThemeProvider, createTheme } from "@mui/material/styles";
import { green, purple } from "@mui/material/colors";

import CssBaseline from '@mui/material/CssBaseline';
import "./app.css"

const theme = createTheme({
	palette: {
		mode: "dark",
		primary: {
			main: purple[500],
		},
		secondary: {
			main: green[500],
		},
	},
});

function App() {
	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<div className="page">
			<h1>Hello!</h1>
			</div>
		</ThemeProvider>
	);
}

render(<App />, document.getElementById("root"));
