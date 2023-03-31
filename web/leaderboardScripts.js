let url = "http://127.0.0.1:5000"

// Code

//Get the array
let table = document.getElementById("table-body");
let updated_spot = document.getElementById("updated");

//Get the data
fetch(url + "/leaderboard")
  .then(response => response.json())
  .then(data => {
    console.log(data);
    leaderboard = data["leaderboard"];
    updated = data["updated"];

    updated_spot.innerHTML = updated;
    
    let i = 0;
    leaderboard.forEach(row => {
        i++;
        let tablerow = table.insertRow();
        tablerow.insertCell().innerHTML = i;
        tablerow.insertCell(1).innerHTML = row["team"];
        tablerow.insertCell(2).innerHTML = row["score"];
    });

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