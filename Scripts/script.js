function authorizer(){
    if (sessionStorage.auth != 1){
      window.location.href = "http://" + IP + ":1880/Lineas_verdes/templates/login.html";
    }
  }
auth = sessionStorage.auth

// setInterval(() => {
//     authorizer()
// }, 1000);

// window.onload = authorizer();