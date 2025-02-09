import React, { useState } from "react";

const DistanceSlider = ({ min = 0, max = 100, step = 1, onChange }) => {
  const [value, setValue] = useState((min + max) / 2);

  const handleChange = (event) => {
    const newValue = Number(event.target.value);
    setValue(newValue);
    if (onChange) {
      onChange(newValue); // Send the value to parent component if needed
    }
  };

  return (
    <div className="slider-container">
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        className="slider"
      />
      <p>{value} Kilometers</p>
    </div>
  );
};

export default DistanceSlider;  // ✅ Corrected export