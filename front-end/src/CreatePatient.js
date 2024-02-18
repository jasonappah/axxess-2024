import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleMinus, faCirclePlus } from "@fortawesome/free-solid-svg-icons";
import Button from "@mui/material/Button";
import { uniqueId } from "react-bootstrap-typeahead/types/utils";
import { Label } from "@mui/icons-material";
import { InputLabel, MenuItem, Select } from "@mui/material";
import { Row } from "react-bootstrap";

import "./createPatient.css";
import { post } from "./Misc";

export default function CreatePatient() {
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

	function addPatientInfo(e) {
		console.log("Adding patient info");

        const prescript = numMedicine.map((medicine, index) => {
            return {
                "frequency_number": numFrequency[index],
                "frequency_unit": numUnits[index],
                "frequency_unit_number": 1,
                "medication_name": medicine + " " + numDosage[index],
            }
        })

        const data = {
            "name": name,
            "prescriptions": prescript,
            "role": "PATIENT",
        }

        post("user/" + id, data).then((response) => {
            if (response.status === 200) {
                console.log("Patient added");
            } else {
                console.log("Patient not added");
            }
        });
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
					<h1 align="center">Create Patient</h1>
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
									<MenuItem value={0}>Hours</MenuItem>
									<MenuItem value={1}>Days</MenuItem>
									<MenuItem value={2}>Weeks</MenuItem>
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
                                <MenuItem value={"MONTH"}>Months</MenuItem>
                                <MenuItem value={"YEAR"}>Years</MenuItem>
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
								}}
							/>
						</div>
					</div>
				</Row>

				<Button variant="contained" color="success" onClick={addPatientInfo}>
					Add Patient Info
				</Button>
			</div>
		</Box>
	);
}
