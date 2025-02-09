import axios from 'axios';

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
export function Push(input) {

  const requestData = { lat: input[0], long: input[1] };

  console.log('Sending request:', {
    method: 'POST',
    url: 'https://get-route-863661396582.europe-north1.run.app/get-route',
    data: requestData
  });
  axios({
    method: 'POST',
    url: 'https://get-route-863661396582.europe-north1.run.app/get-route',
    data: requestData,
    
    
  })
  .then((response) => {
    console.log(response.data);
    
  })
  .catch((error) => {
    console.log(error);
  });
}