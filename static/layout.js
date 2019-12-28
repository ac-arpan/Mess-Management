//CUSTOM JAVASCRIPT
document.getElementById(document.title).innerHTML='<span style="color:rgba(245, 245, 245, 0.781);">'+document.title+'</span>'




//TYPE WRITING EFFECT
line = 0, total = 2;//CURRENT LINE AND TOTAL LINE
sentence = ["This Is A Sample text", "It is Working","Your Mess Your Site"]
function type_anim(txt){
    if(line===total){
        line=0;
    }
    else{
        line++;
    }
    var obj = document.querySelector('#text')
    obj.innerText = ""
    var i = 0;
    var speed = 50; /* The speed/duration of the effect in milliseconds */
    function typeWriter() {
        if (i < txt[line].length) {
            obj.innerHTML += txt[line].charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    typeWriter();
}
if(document.querySelector('#text')!=null){
    setInterval(type_anim,2000,sentence);
}
//write(0);