import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableRow,
} from "@mui/material";
import { useState } from "react";

import "./patients.css";

export default function Patients() {
	const [patients, setPatients] = useState({
		id: {
			id: "123456",
			name: "name",
			medicines: ["med1", "med2"],
			age: 20,
		},
	});

	return (
		<div className="patients-table">
			<Table>
				<TableHead>
					<TableRow>
						<TableCell>ID</TableCell>
						<TableCell>Name</TableCell>
						<TableCell>Medicines</TableCell>
						<TableCell>Age</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{Object.keys(patients).map((id) => {
						return (
							<TableRow>
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
