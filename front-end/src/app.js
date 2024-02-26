import React from "react";
import { render } from "react-dom";
import {
	createBrowserRouter,
	Link,
	Outlet,
	RouterProvider,
  } from "react-router-dom";
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
import { get } from "./Misc";
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

const router = createBrowserRouter([
  {
    path: "/",
    element: <div>TODO: Login page</div>,
  },
  {
	path: '/app',
	element: <App />,
	children: [
	  {
		path: '/app/',
		element: <Patients />,
		loader: async () => {
			const res = await get("users/patients")
			if (res.status === 200) {
				const json = await res.json()
				return {patients: json}
			}
			throw res
		}
	  },
	  {
		path: '/app/patient/:patientId',
		loader: async ({params}) => {
			const res = await get(`users/${params.patientId}/`)
			if (res.status === 200) {
				const json = await res.json()
				return {patient: json}
			}
			throw res
		},
		element: <ViewPatient />,
	  },
	  {
		path: '/app/patient/:patientId/edit',
		element: <CreatePatient />,
		loader: async ({params}) => {
			const res = await get(`users/${params.patientId}/`)
			if (res.status === 200) {
				const json = await res.json()
				return {selectedPatient: json}
			}
			throw res
		}
	  },
	  {
		path: '/app/create-patient',
		element: <CreatePatient />,
		loader: async () => {
			return {selectedPatient: null}
		}
	  },
	]
  }
]);

function App() {
	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<div className="page">
				<div className="menu">
					<Link to="/app">
						<FontAwesomeIcon icon={faNotesMedical} size="2x" className="logo" />
					</Link>
					<Link to="/app">
						<Button
							fullWidth
							sx={{ padding: 2, borderRadius: "0 !important"}}
							variant="outlined"
							color="primary"
						>
							Patients
						</Button>
					</Link>
					<Link to="/app/create-patient">
						<Button
							sx={{ padding: 2 }}
							fullWidth
							variant="outlined"
							color="primary"
							onClick={(e) => {
								console.log("Create patient");
							}}
						>
							Create Patient
						</Button>
					</Link>
				</div>
				<div className="content"><Outlet/></div>
			</div>
		</ThemeProvider>
	);
}

render( <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>, document.getElementById("root"));
