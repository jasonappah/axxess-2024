import { useEffect, useState } from "react";

import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableRow,
} from "@mui/material";

import "./viewPatient.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil } from "@fortawesome/free-solid-svg-icons";

export default function ViewPatient(props) {
	const [medLogs, setMedLogs] = useState([
		{
			name: "Tylenol",
			administered: "2021-10-01",
            time: "12:00 PM",
			taken: true,
		},
		{
			name: "Advil",
			administered: "2021-10-01",
            time: "12:00 PM",
			taken: true,
		},
        {
            name: "Tylenol",
            administered: "2021-10-01",
            time: "12:00 PM",
            taken: false,
        },
        {
            name: "Advil",
            administered: "2021-10-01",
            time: "12:00 PM",
            taken: true,
        },

	]);

	useEffect(() => {
		if (props.selectedPatient === undefined) {
			props.setPage(0);
		}
	}, [props.selectedPatient]);

	return (
		<div className="col">
			<div className="view-container">
				<div className="space-between">
					<h2>{props.selectedPatient.name}</h2>
					<FontAwesomeIcon icon={faPencil} className="icon" />
				</div>
				<div>
					<h3>{"ID: " + props.selectedPatient.id}</h3>
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
					{props.selectedPatient.prescriptions.map((prescription, index) => (
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
