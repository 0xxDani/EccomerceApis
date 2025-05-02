document.addEventListener('DOMContentLoaded', function () {
    var select = document.getElementById('indicativo');

    // Realiza una solicitud a la API de REST Countries
    fetch('https://restcountries.com/v2/all')
        .then(response => response.json())
        .then(data => {
            // Itera sobre los países y agrega opciones al select
            data.forEach(country => {
                if (country.callingCodes.length > 0) {
                    var option = document.createElement('option');
                    option.value = '+' + country.callingCodes[0];
                    option.textContent = '+' + country.callingCodes[0] + ' - ' + country.name;
                    select.appendChild(option);
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});