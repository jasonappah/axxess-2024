import { Table } from "@mui/material";
import { useEffect } from "react";

import "./viewPatient.css";

export default function ViewPatient(props) {
    
    useEffect(() => {
        if (props.selectedPatient === undefined) {
            props.setPage(0);
        }
    }, [props.selectedPatient]);
    
    return (
        <div className="view-container">
            <div>
                <h1>{props.selectedPatient.name}</h1>
            </div>
            <div>
                <h2>{props.selectedPatient.id}</h2>
            </div>
            <Table>

            </Table>
        </div>
    );
}