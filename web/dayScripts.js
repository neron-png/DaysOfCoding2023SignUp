let url = "http://localhost:5000"

async function uploadData(e){
    var form = document.getElementById('make_form');
    var formdata = new FormData(e.target);

	var modal = document.getElementById("myModal");

    var test_case = formdata.get('test_case')

    await fetch(url + "/problem_checking", {
        method: "GET",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"test_case": test_case})
    }).then(response => {
      if(response.status == 200){
        let data = response.json().then(data => {
            console.log(data)
        //     console.log(data);
        // document.getElementById('submit').setAttribute("disabled", "true");
        // document.getElementById('info').innerHTML = "Your request for finding a team has been successfully submitted. Thank you and good luck!";

        // // alert('You have successfully created and joined your team!\nCopy this code and share it with your teammates to have them join');
		//     modal.style.display = "block";
        });

      } else if ( response.status === 418 ){
       
        let data = response.json().then(data => {
          console.log(data);
          alert(data["error"]);
        });
        
        }
       else {
        alert("Κάτι πήγε στραβά!\nΠαρακαλούμε στείλτε μας μήνυμα στο discord της εκδήλωσης https://discord.com/invite/uzs9JHqFAP");
      }
  }).catch(error => {
    alert("Κάτι πήγε στραβά!\nΠαρακαλούμε στείλτε μας μήνυμα στο discord της εκδήλωσης https://discord.com/invite/uzs9JHqFAP \nΉ στα social @acmauth");
  });

}


document.getElementById('submit').addEventListener("submit", function(e) {
    e.preventDefault(); // before the code
    uploadData(e);
  })