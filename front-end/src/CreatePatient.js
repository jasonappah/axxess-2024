import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

export default function CreatePatient() {
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
				<TextField
                    required
					id="filled-required"
					label="Medicine"
					variant="filled"
				/>

				<TextField id="filled-basic" label="Filled" variant="filled" />
			</div>
		</Box>
	);
}
