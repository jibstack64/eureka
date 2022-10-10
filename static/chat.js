
const interval = setInterval(function() {
    refresh()
  }, 5000);

refresh = () => {
    const req = new XMLHttpRequest()
    req.open("GET", "/chat/messages?count=500") // "slow" but oh well
    req.send()
    req.onload = () => {
        var response = JSON.parse(req.response)
        if (req.status > 205) {
            alert(req.status)
        }
        var elem = document.getElementById("chatbox")
        elem.innerHTML = ""
        if (response == undefined) {
            return alert("Error refreshing messages.")
        }
        for (var i = 0; i < response.length; i++) {
            console.log(response[i] + elem.innerHTML)
            elem.innerHTML += `<li>${response[i]}</li>`
        }
    }
}

send_message = () => {
    var inp = document.getElementById("usermsg").value
    const req = new XMLHttpRequest()
    req.open("POST", "/chat/messages")
    req.send(JSON.stringify({"content": inp}))
    req.onload = () => {
        if (req.status > 205) {
            return alert("Error sending message.") // return (user not gonna need refresh)
        }
    }
    refresh()
}
