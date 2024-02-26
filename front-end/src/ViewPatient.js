import { useEffect, useState } from "react";

import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableRow,
} from "@mui/material";
import { Link, useLoaderData } from "react-router-dom";
import "./viewPatient.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil } from "@fortawesome/free-solid-svg-icons";

export default function ViewPatient() {
	const {patient} = useLoaderData();

	return (
		<div className="col">
			<div className="view-container">
				<div className="space-between">
					<h2>{patient.name}</h2>
					<Link to={`/app/patient/${patient.id}/edit`}>
						<FontAwesomeIcon icon={faPencil} className="icon"  />
					</Link>
				</div>
				<div>
					<h3>{"ID: " + patient.id}</h3>
				</div>
			</div>
			<Table stickyHeader className="med-table">
				<colgroup>
					<col width="50%" />
					<col width="25%" />
					<col width="25%" />
				</colgroup>
				<TableHead>
					<TableRow>
						<TableCell>Medicine</TableCell>
						<TableCell>Amount</TableCell>
                        <TableCell>Frequency</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{patient.prescriptions.map((prescription, index) => (
						<TableRow key={index} className={"trow"}>
							<TableCell>{prescription.medication_name.split(" ")[0]}</TableCell>
							<TableCell>{prescription.medication_name.split(" ")[1]}</TableCell>
                            <TableCell>{prescription.frequency_unit_number == 1 ? prescription.frequency_number + " every " + prescription.frequency_unit.toLowerCase() : prescription.frequency_number + " every " + prescription.frequency_unit_number + " " + prescription.frequency_unit.toLowerCase() + "s"}</TableCell>
						</TableRow>
					))}
				</TableBody>
			</Table>
		</div>
	);
}
