let url = "http://127.0.0.1:5000"

// Code

fetch(url + "/activeDays")
  .then(response => response.json())
  .then(data => {
    let activeDays = data.activeDays;
    activeDays.forEach(day => {
      document.getElementById(`day_${day}`).classList.remove("disabled");
      document.getElementById(`day_${day}`).classList.remove("text-secondary");
      document.getElementById(`day_${day}`).classList.add("text-light");
    });
  });