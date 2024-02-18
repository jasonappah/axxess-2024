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
					defaultValue="Hello World"
					variant="filled"
				/>
				<TextField
					disabled
					id="filled-disabled"
					label="ID"
					defaultValue="Hello World"
					variant="filled"
				/>
				<TextField
					id="filled-password-input"
					label="Medicine"
					type="password"
					autoComplete="current-password"
					variant="filled"
				/>

				<TextField id="filled-basic" label="Filled" variant="filled" />
			</div>
		</Box>
	);
}
