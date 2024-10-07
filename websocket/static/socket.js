let s;
let bod;
let room;
let login = `
    <input id="name" onkeydown="
        if (event.key === 'Enter') {
            if (this.value !== '') {
                send(s, [this.value, color], 'name');
                document.querySelector('#fails').innerHTML = '';
                document.querySelector('#msgs').innerHTML = login;
            }
        }
    ">
    <button onclick="
        if (document.querySelector('#name').value !== '') {
            send(s, document.querySelector('#name').value, 'name');
            document.querySelector('#fails').innerHTML = '';
            document.querySelector('#msgs').innerHTML = login;
        }
    ">login</button>
`;
let sen = `
        <input id="send" onkeydown="
            if (event.key === 'Enter') {
                send(s, this.value);
                this.value = '';
                document.querySelector('#fails').innerHTML = '';
            }    
        ">
        <button onclick="
            send(s, document.querySelector('#send').value);
            document.querySelector('#send').value = '';
            document.querySelector('#fails').innerHTML = '';
        ">send</button> <button onclick="
            send(s, 'room', 'leave');
            document.querySelector('#game').style = '';
            document.querySelector('#game').innerHTML = '';
            document.querySelector('#msgs').innerHTML = cr;
            document.querySelector('#fails').innerHTML = '';
            rom = false;
        ">leave room</button>
        <div id="msges"></div>
        <br>
    `;
let cr = `<input id="cr" onkeydown="
            if (event.key === 'Enter') {
                if (this.value == '') {
                    send(s, null, 'create');
                }
                else {
                    send(s, this.value, 'create');
                }
                this.value = '';
            }    
        ">
        <button onclick="
            if (document.querySelector('#cr').value == '') {
                send(s, null, 'create');
            }
            else {
                send(s, document.querySelector('#cr').value, 'create');
            }
            document.querySelector('#cr').value = '';
        ">create</button><br>
    `;
let pos;
let color = [];
let xp = 0;
let rom;
color[0] = Math.floor(Math.random() * (255 - 0 + 1)) + 0
color[1] = Math.floor(Math.random() * (255 - 0 + 1)) + 0
color[2] = Math.floor(Math.random() * (255 - 0 + 1)) + 0

let connect = function(name) {
    const s = new WebSocket(`ws://${ip}:5001`);
    s.onopen = function() {
        if (name !== '') {
            send(s, [name, color], 'name');
        }
        else {
            document.querySelector('#fails').innerHTML = 'please write a name';
        }
    };
    s.onmessage = function(e) {
        let header = JSON.parse(e.data)[0];
        let msg = JSON.parse(e.data)[1];
        if (header === 'msg'){
            document.querySelector('#msges').innerHTML += `${msg}<br>`;
            let b = document.querySelector('#msges').innerHTML.split('<br>')
            if (b.length === 18) {
                b.shift();
                b = b.join('<br>');
                document.querySelector('#msges').innerHTML = b;
            }
        }
        else if (header === 'rooms') {
            let text = "";
            for (let i = 0; i < msg.length; i++) {
                text += msg[i] + ` <button onclick="
                    send(s, \`${msg[i]}\`, 'join')
                    document.querySelector('#msgs').innerHTML = sen;
                    document.querySelector('#rooms').innerHTML = '';
                    document.querySelector('#fails').innerHTML = '';
                ">join</button><br>`;
            }
            document.querySelector("#rooms").innerHTML = text;
        }
        else if (header === 'fail'){
            document.querySelector('#fails').innerHTML = msg;
        }
        else if (header === 'success') {
            if (msg === 'room') {
                rom = true;
                document.querySelector('#msgs').innerHTML = sen;
                document.querySelector('#rooms').innerHTML = '';
                document.querySelector('#fails').innerHTML = '';
                document.querySelector("#game").style.width = '500px';
                document.querySelector("#game").style.height = '500px';
                document.querySelector("#game").style.border = 'black';
                document.querySelector("#game").style.borderWidth = '1px';
                document.querySelector("#game").style.borderStyle = 'solid';
                pos = [0, 0];
                send(s, pos, 'move');
            }
        }
        else if (header === 'move') {
            document.querySelector("#game").innerHTML = msg
        }
        else if (header === 'rm_name') {
            if (msg === '') {
                document.querySelector("#name").innerHTML = msg;
            }
            else {
                document.querySelector("#name").innerHTML = `room: ${msg}`;
            }
            room = msg;
        }
        else if (header === 'rm_ppl') {
            if (msg === '') {
                document.querySelector("#ppl").innerHTML = '';
            }
            else {
                let txt = '';
            for (let i = 0; i < msg.length; i++) {
                if (i !== msg.length - 1) {
                    txt += msg[i] + ', ';
                }
                else {
                    txt += msg[i];
                }
            }
            document.querySelector("#ppl").innerHTML = `participants: ${txt.replace(document.querySelector("#usrname").innerHTML, "you")}`;
            }
        }
        else if (header === 'name') {
            document.querySelector('#username').innerHTML = `username:`;
            document.querySelector('#usrname').innerHTML = `${msg}`;
        }
        else if (header === 'xp') {
            xp = msg
            console.log(xp)
        }
        else if (header === 'ate') {
            pos = [0, 0];
        }
    }
    return s
}


let move = function(e) {
    let focus = document.activeElement;
    if (e.key === 'Enter') {
            if (focus !== document.querySelector('input')) {
                document.querySelector('input').focus()
                focus = document.activeElement;
            }
            else {
                document.body.focus();
                document.activeElement.blur();
            }
    }
    if (focus === document.body) {
        if (e.key === 'ArrowUp') {
            if (pos[0] !== 0) {
                pos[0] -= 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowDown') {
            if (pos[0] + 30 !== 492) {
                pos[0] += 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowRight') {
            if (pos[1] + 30 !== 492) {
                pos[1] += 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowLeft') {
            if (pos[1] !== 0) {
                pos[1] -= 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === ' ') {
            send(s, pos, 'eat');
        }
    }
}


document.addEventListener('keydown', move)


let send = function(s, msg, header = 'msg') {
    if (msg !== '') {
        if (header === 'msg') {
            s.send(JSON.stringify([header, msg]))
            document.querySelector('#msges').innerHTML += `<span style="color:rgb(${color[0]},${color[1]},${color[2]});">you</span>: ${msg}<br>`;
            let b = document.querySelector('#msges').innerHTML.split('<br>')
            if (b.length === 18) {
                b.shift();
                b = b.join('<br>');
                document.querySelector('#msges').innerHTML = b;
            }
        }
        else {
            s.send(JSON.stringify([header, msg]))
        }
    }
}

let show_profile = function() {
    nam = document.querySelector('#usrname').innerText
    bod = document.body.innerHTML;
    document.body.innerHTML = `
        <h1>${nam}</h1>
        xp: ${xp}
        <br>
        <button onclick="
            document.body.innerHTML = bod;
            if (rom === true) {
                send(s, pos, 'move');
            }
        ">back</button>
    `;
}

let send_http_req = function(obj = {}, method = "POST", to = `http://${ip}:5000/server`, result_trgt = "body", func = (r) => {document.querySelector(`${result_trgt}`).innerHTML = `${r}`;}) {
    if (typeof obj == "object") {
        httpreq = new XMLHttpRequest();
        httpreq.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(this.responseText !== ""){
                    if(this.responseText == true){
                        document.querySelector(`${result_trgt}`).innerHTML = ``;
                        return this.responseText;
                    }
                    else{
                        func(this.responseText);
                        return this.responseText;
                    }
                }
            }
            else if (this.status !== 200 && this.status !== "" && this.status !== 0) {
                console.log(this.status);
                return this.statusText;
            }
        };
        arr = [];
        Object.keys(obj).forEach((v) => {
            arr.push(`${v}=${obj[`${v}`]}`);
        });
        txt = encodeURI(arr.join("&"));
        if (method.toUpperCase() === "GET"){
            httpreq.open(`${method.toUpperCase()}`, `${to}?${txt}`, true);
            httpreq.setRequestHeader('Access-Control-Allow-Origin', "true");
            httpreq.send();
        }
        else if(method.toUpperCase() === "POST"){
            httpreq.open(`${method.toUpperCase()}`, `${to}`, true);
            httpreq.setRequestHeader('Access-Control-Allow-Origin', "true");
            httpreq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            httpreq.send(`${txt}`);
        }
    }
}

let askname = function(name) {
    if (name !== '') {
        send_http_req({name: name}, undefined, undefined, undefined, (r) => {
            r = JSON.parse(r)
            if (r === true) {
                s = connect(name);
                document.querySelector('#fails').innerHTML = '';
                document.querySelector('#msgs').innerHTML = login;
                if (focus !== document.body) {
                    document.body.focus();
                    document.activeElement.blur();
                }
                document.querySelector('#msgs').innerHTML = cr;
                document.querySelector('#logout').innerHTML = `
                    <button onclick="show_profile();">profile</button>
                    <button onclick="location.reload();">sign out</button>
                `;
            }
            else {
                document.querySelector('#fails').innerHTML = 'user already exist'
            }
        })
    }
    else {
        document.querySelector('#fails').innerHTML = 'please write a name';
    }
}
