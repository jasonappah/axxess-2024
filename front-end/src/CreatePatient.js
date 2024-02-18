import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleMinus, faCirclePlus } from "@fortawesome/free-solid-svg-icons";
import Button from "@mui/material/Button";

import "./createPatient.css";

export default function CreatePatient() {
	const [numMedicine, setnumMedicine] = useState([]);
	const [numDosage, setnumDosage] = useState([]);

	return (
		<Box
			component="form"
			sx={{
				"& .MuiTextField-root": { m: 1, width: "25ch" },
			}}
			noValidate
			autoComplete="off"
		>
			<div className="create-fields">
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
				<TextField required id="filled-required" label="ID" variant="filled" />
				{numMedicine.map((medicine, index) => (
					<div className="medicine">
						<TextField
							required
							key={index}
							value={medicine}
							id="filled-required"
							label="Medicine"
							variant="filled"
							disabled
						/>
						<TextField
							required
							value={numDosage[index]}
							id="filled-basic"
							label="Dosage"
							variant="filled"
							disabled
						/>
						<FontAwesomeIcon
							icon={
								index == numMedicine.length - 1 ? faCirclePlus : faCircleMinus
							}
							className="icon"
							size="2x"
							onClick={(e) => {
								if (index == numMedicine.length - 1) {
									var temp = [...numMedicine];
									temp.push("");
									setnumMedicine(temp);

									var temp = [...numDosage];
									temp.push("");
									setnumDosage(temp);
								} else {
									var temp = [...numMedicine];
									temp.splice(index, 1);
									setnumMedicine(temp);

									var temp = [...numDosage];
									temp.splice(index, 1);
									setnumDosage(temp);
								}
							}}
						/>
					</div>
				))}

				{/* <FontAwesomeIcon
					icon={faCirclePlus}
					className="icon"
					size="2x"
					onClick={(e) => {
						var temp = [...numMedicine];
						temp.push("");
						setnumMedicine(temp);

						var temp = [...numDosage];
						temp.push("");
						setnumDosage(temp);
					}}
				/> */}

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


				<Button variant="Add Patient Info">Contained</Button>
			</div>
		</Box>
	);
}
