import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableRow,
} from "@mui/material";
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStethoscope } from "@fortawesome/free-solid-svg-icons";

import "./patients.css";
import { get } from "./Misc";

export default function Patients(props) {
	const [patients, setPatients] = useState({});

	useEffect(() => {
		get("users/patients").then((response) => {
			console.log("Getting patients");
			console.log(response);
			if (response.status === 200) {
				response.json().then((data) => {
					console.log(data);
					setPatients(data);
				});
			}
		});
	}, []);

	return (
		<div className="patients-table">
			<Table stickyHeader>
				<colgroup>
					<col width="5%" />
					<col width="10%" />
					<col width="30%" />
					<col width="45%" />
					<col width="10%" />
				</colgroup>
				<TableHead>
					<TableRow>
						<TableCell></TableCell>
						<TableCell>ID</TableCell>
						<TableCell>Name</TableCell>
						<TableCell>Prescriptions</TableCell>
						<TableCell>Age</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{Object.keys(patients).map((id) => {
						return (
							<TableRow key={id} hover className="trow">
								<TableCell>
									<FontAwesomeIcon
										icon={faStethoscope}
										className="icon"
										onClick={(e) => {
											console.log("View patient: ", patients[id]);
											props.setSelectedPatient(patients[id]);
											props.setPage(2);
										}}
									/>
								</TableCell>
								<TableCell>
									<p className="patient-id">{patients[id].id}</p>
								</TableCell>
								<TableCell>{patients[id].name}</TableCell>
								<TableCell>
									{patients[id].prescriptions
										.map((p) => p.medication_name + ", ")
										.join(" ").slice(0, -2)}
								</TableCell>
								<TableCell>{patients[id].age}</TableCell>
							</TableRow>
						);
					})}
				</TableBody>
			</Table>
		</div>
	);
}
