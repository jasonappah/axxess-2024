import React, { useEffect, useState } from "react";
import { render } from "react-dom";

import { ThemeProvider, createTheme } from "@mui/material/styles";
import { green, purple } from "@mui/material/colors";

import CssBaseline from "@mui/material/CssBaseline";
import "./app.css";
import { Button } from "@mui/material";
import Patients from "./Patients";
import CreatePatient from "./CreatePatient";
import ViewPatient from "./ViewPatient";

const theme = createTheme({
	palette: {
		mode: "light",
		primary: {
			main: purple[500],
		},
		secondary: {
			main: green[500],
		},
	},
});

function App() {
	const [page, setPage] = useState(0);
	const [content, setContent] = useState(<Patients />);
	const [selectedPatient, setSelectedPatient] = useState(<Patients />);

	useEffect(() => {
		switch (page) {
			case 0:
				setContent(<Patients />);
				break;
			case 1:
				setContent(<CreatePatient />);
				break;
			case 2:
				setContent(<ViewPatient />);
				break;
			default:
				setContent(<Patients />);
				break;
		}
	}, [page]);

	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<div className="page">
				<div className="menu"></div>
				<div className="content">{content}</div>
			</div>
		</ThemeProvider>
	);
}

render(<App />, document.getElementById("root"));
