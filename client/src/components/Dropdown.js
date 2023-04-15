import { useState, useEffect } from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import FormHelperText from "@mui/material/FormHelperText";

function Dropdown({ onSelect }) {
  const [options, setOptions] = useState([]);
  const [selectedId, setSelectedId] = useState("");

  // FIXME should be configured, ideally solved with reverse proxy
  const backendURL = "http://localhost:80/api";

  useEffect(() => {
    fetch(`${backendURL}/org-ids`)
      .then((response) => response.json())
      .then((fetchedFeatures) => {
        // we assume that we are dealiing with numbers for org-ids here. Checking to be on the safe side
        const numbersOnly = fetchedFeatures.filter(
          (val) => typeof val === "number"
        );
        if (numbersOnly.length < fetchedFeatures.length) {
          console.warn("Warning: fetchedFeatures contains non-number values.");
        }
        if (numbersOnly.length > 1) {
          numbersOnly.sort((a, b) => a - b);
          setOptions(numbersOnly.concat(["Select All"]));
        } else {
          setOptions(numbersOnly);
        }
      });
  }, []);

  const handleIdChange = (event) => {
    setSelectedId(event.target.value);
    onSelect(event.target.value);
  };

  return (
    <FormControl sx={{ m: 1, minWidth: 140 }}>
      <InputLabel id="id-label">Organisation</InputLabel>
      <Select
        labelId="Organisation"
        value={selectedId}
        onChange={handleIdChange}
      >
        {options.map((option) => (
          <MenuItem key={option} value={option}>
            {option}
          </MenuItem>
        ))}
      </Select>
      <FormHelperText>Please select an orgainzation ID</FormHelperText>
    </FormControl>
  );
}

export default Dropdown;
