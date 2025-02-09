import React, { useState } from 'react';

function PubInputPage() {
  // State variables for each slider
  const [hoursAtPub, setHoursAtPub] = useState(1);           // 1 to 12 (half-hour increments)
  const [timeAtEachPub, setTimeAtEachPub] = useState(15);       // 15 to 180 minutes (15-min increments)
  const [walkingEnjoyment, setWalkingEnjoyment] = useState(1);  // 1 to 5

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h2>User Inputs</h2>

      {/* Hours at the Pub */}
      <div style={{ marginBottom: '1.5rem' }}>
        <label htmlFor="hoursAtPub" style={{ display: 'block', marginBottom: '.5rem' }}>
          Hours at the Pub: <strong>{hoursAtPub} hrs</strong>
        </label>
        <input
          id="hoursAtPub"
          type="range"
          min="1"
          max="12"
          step="0.5"
          value={hoursAtPub}
          onChange={(e) => setHoursAtPub(parseFloat(e.target.value))}
          style={{ width: '100%' }}
        />
      </div>

      {/* Time at each Pub */}
      <div style={{ marginBottom: '1.5rem' }}>
        <label htmlFor="timeAtEachPub" style={{ display: 'block', marginBottom: '.5rem' }}>
          Time at Each Pub: <strong>{timeAtEachPub} mins</strong>
        </label>
        <input
          id="timeAtEachPub"
          type="range"
          min="15"
          max="180"
          step="15"
          value={timeAtEachPub}
          onChange={(e) => setTimeAtEachPub(parseInt(e.target.value, 10))}
          style={{ width: '100%' }}
        />
      </div>

      {/* Enjoyment of Walking */}
      <div style={{ marginBottom: '1.5rem' }}>
        <label htmlFor="walkingEnjoyment" style={{ display: 'block', marginBottom: '.5rem' }}>
          Enjoyment of Walking: <strong>{walkingEnjoyment}</strong>
        </label>
        <input
          id="walkingEnjoyment"
          type="range"
          min="1"
          max="5"
          step="1"
          value={walkingEnjoyment}
          onChange={(e) => setWalkingEnjoyment(parseInt(e.target.value, 10))}
          style={{ width: '100%' }}
        />
      </div>
    </div>
  );
}

export default PubInputPage;
