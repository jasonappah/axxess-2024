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
					<h3>{props.selectedPatient.id}</h3>
				</div>
			</div>
			<Table stickyHeader className="med-table">
				<colgroup>
					<col width="35%" />
					<col width="30%" />
					<col width="20%" />
					<col width="15%" />
				</colgroup>
				<TableHead>
					<TableRow>
						<TableCell>Medicine</TableCell>
						<TableCell>Administered On</TableCell>
                        <TableCell>Time</TableCell>
						<TableCell>Taken</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{medLogs.map((medLog, index) => (
						<TableRow key={index} className={medLog.taken ? "taken trow" : "missed trow"}>
							<TableCell>{medLog.name}</TableCell>
							<TableCell>{medLog.administered}</TableCell>
                            <TableCell>{medLog.time}</TableCell>
							<TableCell>{medLog.taken ? "Yes" : "No"}</TableCell>
						</TableRow>
					))}
				</TableBody>
			</Table>
		</div>
	);
}
