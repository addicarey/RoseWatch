/* calculator AC */
/* Defines an async function that takes in 3 parameters AC */
async function convertCurrency(amount, fromCurrency, toCurrency) {
/* Constructs a URL to fetch the current price data from the Coingecko API AC */
        const url = `https://api.coingecko.com/api/v3/simple/price?ids=oasis-network&vs_currencies=${fromCurrency}`;
/* Makes an HTTP request to the API and awaits the response AC */
        const response = await fetch(url);
/* Extracts the JSON data from the response and assigns it to the data variable AC */
        const data = await response.json();
/* Retrieves the exchange rate AC */
        const rate = data["oasis-network"][fromCurrency];
/* Calculates the converted amount by dividing amount by the exchange rate AC */
        const result = amount / rate;
/* Returns a string representing the converted amount with two decimal places AC */
        return `${result.toFixed(2)} ${toCurrency.toUpperCase()}`;
      }
/* Selects the first <form> element in the document AC */
      const form = document.querySelector("form");
/* Adds a submit event listener to the form with an async callback function AC*/
      form.addEventListener("submit", async (event) => {
/* Prevents the default form submission behavior AC */
        event.preventDefault();
/* Retrieves the value of the amount input field using its ID AC */
        const amount = document.querySelector("#amount").value;
/* Sets fromCurrency to "eur" and toCurrency to "rose" AC */
        const fromCurrency = "eur";
        const toCurrency = "rose";
/* Calls the convertCurrency function with the provided parameters and awaits the result AC */
        const result = await convertCurrency(amount, fromCurrency, toCurrency);
/* Updates the text content of the HTML elements with the converted result and the original amount AC */
        document.querySelector("#result").textContent = result;
        document.querySelector("#amount2").textContent = amount;
      });

           

