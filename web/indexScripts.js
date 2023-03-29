let url = "http://127.0.0.1:5000"

// Code

fetch(url + "/activeDay")
  .then(response => response.json())
  .then(data => {
    let activeDay = data["activeDay"];
    console.log(activeDay)

    let dayTab = document.getElementById(`day_link`);
    if (activeDay >= 1){
      dayTab.classList.remove('disabled')
      dayTab.classList.remove('secondary')
      dayTab.classList.add('text-light')
      dayTab.innerHTML = "Day " + activeDay
    }

  });