//CUSTOM JAVASCRIPT
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
setInterval(type_anim, 2000,sentence)
//write(0);



















// // List of sentences
// var _CONTENT = [ 
// 	"Welcome to our Mess Management System", 
// 	"You can follow your monthly Mess-Bill", 
// 	"And you can see weekly Meal Chart", 
// 	"You can contact us for any information or suggestion :)"
// ];

// // Current sentence being processed
// var _PART = 0;

// // Character number of the current sentence being processed 
// var _PART_INDEX = 0;

// // Holds the handle returned from setInterval
// var _INTERVAL_VAL;

// // Element that holds the text
// var _ELEMENT = document.querySelector("#text");

// // Cursor element 
// var _CURSOR = document.querySelector("#cursor");

// // Implements typing effect
// function Type() { 
// 	// Get substring with 1 characater added
// 	var text =  _CONTENT[_PART].substring(0, _PART_INDEX + 1);
// 	_ELEMENT.innerHTML = text;
// 	_PART_INDEX++;

// 	// If full sentence has been displayed then start to delete the sentence after some time
// 	if(text === _CONTENT[_PART]) {
// 		// Hide the cursor
// 		_CURSOR.style.display = 'none';

// 		clearInterval(_INTERVAL_VAL);
// 		setTimeout(function() {
// 			_INTERVAL_VAL = setInterval(Delete, 40);
// 		}, 1000);
// 	}
// }

// // Implements deleting effect
// function Delete() {
// 	// Get substring with 1 characater deleted
// 	var text =  _CONTENT[_PART].substring(0, _PART_INDEX - 1);
// 	_ELEMENT.innerHTML = text;
// 	_PART_INDEX--;

// 	// If sentence has been deleted then start to display the next sentence
// 	if(text === '') {
// 		clearInterval(_INTERVAL_VAL);

// 		// If current sentence was last then display the first one, else move to the next
// 		if(_PART == (_CONTENT.length - 1))
// 			_PART = 0;
// 		else
// 			_PART++;

// 		_PART_INDEX = 0;

// 		// Start to display the next sentence after some time
// 		setTimeout(function() {
// 			_CURSOR.style.display = 'inline-block';
// 			_INTERVAL_VAL = setInterval(Type, 40);
// 		}, 200);
// 	}
// }

// // Start the typing effect on load
// _INTERVAL_VAL = setInterval(Type, 40);
