//import axios from 'axios';

/**
 * Method used to pull data from the backend DB.
 * @param {*} address The address of the data to be pulled.
 *                    Check documentation for full list of addresses available.
 */
export function Pull(address) {
  return new Promise((resolve, reject) => {
    fetch("https://get-route-863661396582.europe-north1.run.app/get-route")
      .then(response => {
        if (!response.ok) {
          throw new Error('Error - Flask Unreachable');
        }
        return response.json();
      })
      .then(data => {
        resolve(data);
      })
      .catch(error => {
        console.error('Error - Data Unreachable: ', error);
        reject(error);
      });
  });
}

/**
 * Method to write data to the backend DB
 * @param {*} address Address data should be written to.
 * @param {*} input Data to be written to backend.
 */
import axios from 'axios';

export function Push(input) {
    const requestData = { 
      lat: input[1], 
      long: input[0], 
      maximise_rating: input[3], 
      walking: input[4], 
      range: input[2], 
      warrior_mode: input[5]
    };

    console.log('Sending request:', {
      method: 'post',
      url: 'http://localhost:5069/',
      data: requestData
    });

    // Return the axios promise to allow the caller to await it
    return axios({
      method: 'post',
      url: 'http://localhost:5069/',
      data: requestData
    });
}
