/**
 * Method used to pull data from the backend DB.
 * @param {*} address The address of the data to be pulled.
 *                    Check documentation for full list of addresses available.
 */
export function Pull() {
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
  return new Promise((resolve, reject) => {
    console.log(JSON.stringify(input))
      fetch("https://get-route-863661396582.europe-north1.run.app/get-route", {
        method: "POST",
        headers: {
          "content-Type" : "application/json"
        },
        body :JSON.stringify(input),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error - Flask Unreachable');
          }
          return response.json();
        })
        .then(input => {
          
          resolve(input)
        })
        .catch(error => {
          console.error('Error - Data Unreachable: ', error);
          reject(error)
        });
    });
}