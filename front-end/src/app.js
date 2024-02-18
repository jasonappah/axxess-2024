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
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faNotesMedical } from "@fortawesome/free-solid-svg-icons";

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
				setContent(
					<Patients setPage={setPage} setSelectedPatient={setSelectedPatient} />
				);
				break;
			case 1:
				setContent(
					<CreatePatient
						setPage={setPage}
						setSelectedPatient={setSelectedPatient}
					/>
				);
				break;
			case 2:
				setContent(
					<ViewPatient
						selectedPatient={selectedPatient}
						setPage={setPage}
						setSelectedPatient={setSelectedPatient}
					/>
				);
				break;
			default:
				setContent(
					<Patients setPage={setPage} setSelectedPatient={setSelectedPatient} />
				);
				break;
		}
	}, [page]);

	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<div className="page">
				<div className="menu">
					<FontAwesomeIcon icon={faNotesMedical} size="2x" className="logo" />
					<Button
						fullWidth
						sx={{ padding: 2, borderRadius: "0 !important"}}
						variant="outlined"
						color="primary"
						onClick={(e) => {
							setPage(0);
						}}
					>
						Patients
					</Button>
					<Button
						sx={{ padding: 2 }}
						fullWidth
						variant="outlined"
						color="primary"
						onClick={(e) => {
							setPage(1);
						}}
					>
						Create Patient
					</Button>
				</div>
				<div className="content">{content}</div>
			</div>
		</ThemeProvider>
	);
}

render(<App />, document.getElementById("root"));
