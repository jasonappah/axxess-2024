import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCirclePlus } from "@fortawesome/free-solid-svg-icons";
import { set } from "date-fns";


export default function CreatePatient() {

    const [numMedicine,setnumMedicine] = useState([""]) 

	return (
		<Box
			component="form"
			sx={{
				"& .MuiTextField-root": { m: 1, width: "25ch" },
			}}
			noValidate
			autoComplete="off"
		>
			<div>
                
            <header>
                <h1 align="center">Create Patient</h1>
            </header>

				<TextField
					required
					id="filled-required"
					label="Name"
					variant="filled"
				/>
				<TextField
					required
					id="filled-required"
					label="ID"
					variant="filled"
				/>
                {numMedicine.map((medicine,index) =>(
                    <TextField
                    required
					id="filled-required"
					label="Medicine"
					variant="filled"
				/>
                ))}
			
				<TextField
                required 
                id="filled-basic" 
                label="Dosage" 
                variant="filled" 
                />

                <FontAwesomeIcon icon = {faCirclePlus} className="icon" onClick={(e) => 
                {
                var temp = numMedicine
                temp.push ("")
                setnumMedicine (temp)

                 }} />


			</div>
		</Box>
	);
}
