let url = "http://localhost:5000"

async function uploadData(e){
    var form = document.getElementById('make_form');
    var formdata = new FormData(e.target);

	var modal = document.getElementById("myModal");

    var username = formdata.get('discord');

    console.log(username);

    await fetch(url + "/createTeam", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"discord_username": username})
    }).then(response => {
      if(response.status == 200){
        let data = response.json().then(data => {
            console.log(data);
        document.getElementById('submit').setAttribute("disabled", "true");
        document.getElementById('title').innerHTML = data["code"];
        document.getElementById('info').innerHTML = "Joined successfully. Good Luck!";

        // alert('You have successfully created and joined your team!\nCopy this code and share it with your teammates to have them join');
		modal.style.display = "block";
        });

      } else{
          alert("Κάτι πήγε στραβά!\nΠαρακαλούμε στείλτε μας μήνυμα στο discord της εκδήλωσης https://discord.com/invite/uzs9JHqFAP");
      }
  }).catch(error => {
    alert("Κάτι πήγε στραβά!\nΠαρακαλούμε στείλτε μας μήνυμα στο discord της εκδήλωσης https://discord.com/invite/uzs9JHqFAP\nΉ στα social @acmauth");
  });

}


document.getElementById('make_form').addEventListener("submit", function(e) {
    e.preventDefault(); // before the code
    uploadData(e);
  })