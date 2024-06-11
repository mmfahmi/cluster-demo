function hideButton(){
    var loginButton =  document.getElementById("loginButton");
    if(loginButton){
        loginButton.style.display = "none";
    }
}

function simulateLogin(){
    setTimeout(function(){hideButton();},2000)
}
