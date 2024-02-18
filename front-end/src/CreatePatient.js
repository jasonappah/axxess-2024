import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCirclePlus } from "@fortawesome/free-solid-svg-icons";
import Button from '@mui/material/Button';



export default function CreatePatient() {

    const [numMedicine,setnumMedicine] = useState([""]) 
    const [numDosage,setnumDosage] = useState([""]) 

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

            <Box sx={{display:'flex'}}>
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

                <Box sx={{display:'flex',flexDirection:'column'}}>
                {numMedicine.map((medicine,index) =>(
                    <Box sx={{display:'flex',flexDirection:'row'}}>
                    <TextField
                    required
                    key={index}
					id="filled-required"
					label="Medicine"
					variant="filled"
				/>
                    <TextField
                    required 
                    id="filled-basic" 
                    label="Dosage" 
                 variant="filled" 
                />
                </Box>
                
                ))}</Box>
			
            </Box>

                <FontAwesomeIcon icon = {faCirclePlus} className="icon" onClick={(e) => 
                {
                var temp = [...numMedicine]
                temp.push ("")
                setnumMedicine (temp)

                var temp = [...numDosage]
                temp.push ("")
                setnumDosage (temp)


                 }} />

                <Button variant="contained" color="success"> 
                Add Patient Info
                </Button>


			</div>
		</Box>
	);
}
