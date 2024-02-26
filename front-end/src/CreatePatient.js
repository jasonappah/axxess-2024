import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleMinus, faCirclePlus } from "@fortawesome/free-solid-svg-icons";
import Button from "@mui/material/Button";
import { MenuItem, Select } from "@mui/material";
import { Row } from "react-bootstrap";
import { useLoaderData, useNavigate } from "react-router-dom";

import "./createPatient.css";
import { post } from "./Misc";

export default function CreatePatient() {
	const {selectedPatient} = useLoaderData();
	const navigate = useNavigate();
	const [numMedicine, setnumMedicine] = useState([]);
	const [numDosage, setnumDosage] = useState([]);
	const [numFrequency, setnumFrequency] = useState([]);
	const [numUnits, setnumUnits] = useState([]);

	const [id, setId] = useState("patient" + Math.floor(Math.random() * 1000));

	const [tempMedicine, setTempMedicine] = useState("");
	const [tempDosage, setTempDosage] = useState("");
	const [tempFrequency, setTempFrequency] = useState("");
	const [tempUnits, setTempUnits] = useState("HOUR");

	const [name, setName] = useState("");

	useEffect(() => {
		if (selectedPatient) {
			// fill with selected patient info if selectedPatient
			console.log("Editing patient");
			console.log(selectedPatient);
			setName(selectedPatient.name);
			setId(selectedPatient.id);
			setnumMedicine(
				selectedPatient.prescriptions.map(
					(prescription) => prescription.medication_name.split(" ")[0]
				)
			);
			setnumDosage(
				selectedPatient.prescriptions.map(
					(prescription) => prescription.medication_name.split(" ")[1]
				)
			);
			setnumFrequency(
				selectedPatient.prescriptions.map(
					(prescription) => prescription.frequency_number
				)
			);
			setnumUnits(
				selectedPatient.prescriptions.map(
					(prescription) => prescription.frequency_unit
				)
			);
		} else {
			setnumMedicine([]);
			setnumDosage([]);
			setnumFrequency([]);
			setnumUnits([]);
			setId("patient" + Math.floor(Math.random() * 1000));
			setTempMedicine("");
			setTempDosage("");
			setTempFrequency("");
			setTempUnits("HOUR");
			setName("");
		}
	}, [selectedPatient]);

	function addPatientInfo(e) {
		console.log("Adding patient info");

		const prescript = numMedicine.map((medicine, index) => {
			return {
				frequency_number: numFrequency[index],
				frequency_unit: numUnits[index],
				frequency_unit_number: 1,
				medication_name: medicine + " " + numDosage[index],
			};
		});

		console.log(prescript);

		const data = {
			name: name,
			prescriptions: prescript,
			id: id,
			role: "PATIENT",
		};

		var url = selectedPatient ? "users/update/" : "users/";
		console.log(url);

		// if (selectedPatient) {
		// 	setnumMedicine([]);
		// 	setnumDosage([]);
		// 	setnumFrequency([]);
		// 	setnumUnits([]);
		// 	setId("patient" + Math.floor(Math.random() * 1000));
		// 	setTempMedicine("");
		// 	setTempDosage("");
		// 	setTempFrequency("");
		// 	setTempUnits("HOUR");
		// 	setName("");
		// 	navigate('/app')
		// 	return;
		// }

		post(url + id, data).then((response) => {
			if (response.status === 200) {
				console.log("Patient added");
				setnumMedicine([]);
				setnumDosage([]);
				setnumFrequency([]);
				setnumUnits([]);
				setId("patient" + Math.floor(Math.random() * 1000));
				setTempMedicine("");
				setTempDosage("");
				setTempFrequency("");
				setTempUnits("HOUR");
				setName("");
				navigate('/app')
			} else {
				console.log("Patient not added");
			}
		});
	}

	function deletePatient(e) {
		console.log("Deleting patient");

		var url = "users/delete/" + id;
		console.log(url);

		post(url, {}).then((response) => {
			if (response.status === 200) {
				console.log("Patient deleted");
				setnumMedicine([]);
				setnumDosage([]);
				setnumFrequency([]);
				setnumUnits([]);
				setId("patient" + Math.floor(Math.random() * 1000));
				setTempMedicine("");
				setTempDosage("");
				setTempFrequency("");
				setTempUnits("HOUR");
				setName("");
				navigate('/app')
			} else {
				console.log("Patient not deleted");
			}
		});
		// console.log("Patient deleted");
		// setnumMedicine([]);
		// setnumDosage([]);
		// setnumFrequency([]);
		// setnumUnits([]);
		// setId("patient" + Math.floor(Math.random() * 1000));
		// setTempMedicine("");
		// setTempDosage("");
		// setTempFrequency("");
		// setTempUnits("HOUR");
		// setName("");
		// navigate('/app')
	}

	return (
		<Box
			component="form"
			sx={{
				// "& .MuiTextField-root": { m: 1, width: "25ch" },
				width: "100%",
			}}
			noValidate
			autoComplete="off"
		>
			<div className="temp">
				<header>
					<h1 align="center">{selectedPatient ? "Edit " : "Create "}Patient</h1>
				</header>

				<Row className="cp-row">
					<div
						className="cp-div"
						style={{
							display: "flex",
							flexDirection: "column",
							justifyContent: "center",
							alignItems: "center",
						}}
					>
						<h3>Info</h3>
						<TextField
							id="filled-required"
							label="Name"
							variant="filled"
							value={name}
							onChange={(e) => setName(e.target.value)}
						/>
						<TextField
							id="filled-required"
							label="ID"
							disabled
							variant="filled"
							value={id}
						/>
					</div>

					<div
						className="cp-div"
						style={{ display: "flex", flexDirection: "column" }}
					>
						<h3>Prescriptions</h3>
						{numMedicine.map((medicine, index) => (
							<div
								className="med-div"
								style={{
									display: "flex",
									flexDirection: "row",
									justifyContent: "center",
									alignItems: "center",
								}}
							>
								<TextField
									key={index}
									value={numMedicine[index]}
									id="filled-required"
									label="Medicine"
									variant="filled"
									disabled={true}
								/>
								<TextField
									value={numDosage[index]}
									id="filled-basic"
									label="Dosage"
									variant="filled"
									disabled={true}
								/>
								<TextField
									id="filled-basic"
									label="Frequency"
									variant="filled"
									placeholder="2"
									value={numFrequency[index]}
									disabled
								/>
								<Select
									labelId="demo-simple-select-label"
									id="demo-simple-select"
									value={numUnits[index]}
									label="Units"
									variant="filled"
									disabled
								>
									<MenuItem value={"HOUR"}>Hours</MenuItem>
									<MenuItem value={"DAY"}>Days</MenuItem>
									<MenuItem value={"WEEK"}>Weeks</MenuItem>
								</Select>
								<FontAwesomeIcon
									icon={faCircleMinus}
									className="icon"
									size="2x"
									onClick={(e) => {
										var temp = [...numMedicine];
										temp.splice(index, 1);
										setnumMedicine(temp);

										var temp = [...numDosage];
										temp.splice(index, 1);
										setnumDosage(temp);
									}}
								/>
							</div>
						))}

						<div
							className="med-div"
							style={{
								display: "flex",
								flexDirection: "row",
								justifyContent: "center",
								alignItems: "center",
							}}
						>
							<TextField
								id="filled-required"
								label="Medicine"
								variant="filled"
								placeholder="Tylenol, Advil, etc."
								value={tempMedicine}
								onChange={(e) => setTempMedicine(e.target.value)}
							/>
							<TextField
								id="filled-basic"
								label="Dosage"
								variant="filled"
								placeholder="500g"
								value={tempDosage}
								onChange={(e) => setTempDosage(e.target.value)}
							/>
							<TextField
								id="filled-basic"
								label="Frequency"
								variant="filled"
								placeholder="2"
								value={tempFrequency}
								onChange={(e) => setTempFrequency(e.target.value)}
							/>
							<Select
								labelId="demo-simple-select-label"
								id="demo-simple-select"
								value={tempUnits}
								label="Units"
								variant="filled"
								onChange={(e) => setTempUnits(e.target.value)}
							>
								<MenuItem value={"HOUR"}>Hours</MenuItem>
								<MenuItem value={"DAY"}>Days</MenuItem>
								<MenuItem value={"WEEK"}>Weeks</MenuItem>
							</Select>
							<FontAwesomeIcon
								icon={faCirclePlus}
								className="icon"
								size="2x"
								onClick={(e) => {
									var temp = [...numMedicine];
									temp.push(tempMedicine);
									setnumMedicine(temp);

									var temp = [...numDosage];
									temp.push(tempDosage);
									setnumDosage(temp);

									var temp = [...numFrequency];
									temp.push(tempFrequency);
									setnumFrequency(temp);

									var temp = [...numUnits];
									temp.push(tempUnits);
									setnumUnits(temp);

									setTempMedicine("");
									setTempDosage("");
									setTempFrequency("");
									setTempUnits("HOUR");
								}}
							/>
						</div>
					</div>
				</Row>

				<div className="row">
					<Button
						variant="contained"
						color={selectedPatient ? "warning" : "primary"}
						onClick={addPatientInfo}
					>
						{selectedPatient ? "Edit Patient" : "Add Patient"}
					</Button>
					{selectedPatient ? (
						<Button variant="contained" color={"error"} onClick={deletePatient}>
							Delete Patient
						</Button>
					) : null}
				</div>
			</div>
		</Box>
	);
}
