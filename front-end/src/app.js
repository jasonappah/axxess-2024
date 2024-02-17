import React from "react";
import { render } from "react-dom";

import { ThemeProvider, createTheme } from "@mui/material/styles";
import { green, purple } from "@mui/material/colors";

import CssBaseline from '@mui/material/CssBaseline';
import "./app.css"
import { Button } from "@mui/material";

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
			<Button variant="contained" color="primary">
				Hello World
			</Button>
			</div>
		</ThemeProvider>
	);
}

render(<App />, document.getElementById("root"));
