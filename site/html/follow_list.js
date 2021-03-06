function getJSON(url, callback) {
var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.responseType = 'text';
xhr.onload = function() {
    var status = xhr.status;
    if (status == 200) {
        callback(null, xhr.response);
    } else {
        callback(status);
    }
};
xhr.send();
}

window.onload = function name(){}

getJSON('/hackathon2020/site/scripts/all_users.py',  function(err, ppl) {
	ppl = JSON.parse(ppl)
	for (const key in ppl) {
		data = ppl[key];
		var un = data.username;
		var el = document.getElementById('generic_friend').cloneNode(true);
		el.getElementsByClassName('name')[0].innerHTML = un;
		b = el.getElementsByClassName('input_box')[0];
		b.value = un;
		b.checked = true;
		if (data.is_friend == '1') {
			b.setAttribute('checked',true);
		} else {
			b.checked = false;
		}
		document.getElementById('friend_list').innerHTML += el.innerHTML;
	}	
	});

