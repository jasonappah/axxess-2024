import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableRow,
} from "@mui/material";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStethoscope } from "@fortawesome/free-solid-svg-icons";

import "./patients.css";

export default function Patients(props) {
	const [patients, setPatients] = useState({
		123456: {
			id: "123456",
			name: "Bryant",
			medicines: ["med1", "med2"],
			age: 20,
		},
		456789: {
			id: "456789",
			name: "BK",
			medicines: ["med3", "med4"],
			age: 60,
		},
        abcd: {
			id: "abcd",
			name: "Jason",
			medicines: ["med3", "med4"],
			age: 60,
		},
        efgh: {
			id: "efgh",
			name: "Dan",
			medicines: ["med3", "med4"],
			age: 60,
		},
	});

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
						<TableCell>Medicines</TableCell>
						<TableCell>Age</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{Object.keys(patients).map((id) => {
						return (
							<TableRow key={id} hover>
								<TableCell>
									<FontAwesomeIcon icon={faStethoscope} className="icon" onClick={(e) => {
                                        console.log("View patient: ", patients[id]);
                                        props.setSelectedPatient(patients[id]);
                                        props.setPage(2);
                                    }} />
								</TableCell>
								<TableCell>{patients[id].id}</TableCell>
								<TableCell>{patients[id].name}</TableCell>
								<TableCell>{patients[id].medicines.join(", ")}</TableCell>
								<TableCell>{patients[id].age}</TableCell>
							</TableRow>
						);
					})}
				</TableBody>
			</Table>
		</div>
	);
}
