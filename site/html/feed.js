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

getJSON('/hackathon2020/site/scripts/sortPosts.py',  function(err, posts) {
	posts = JSON.parse(posts)
	for (const key in posts) {
		data = posts[key];
		var un = data.username;
		var con = data.content;
		var ip = data.interestPercent;
		var post = document.getElementById('generic_post').cloneNode(true);
		post.getElementsByClassName('username')[0].innerHTML = un;
		post.getElementsByClassName('content')[0].innerHTML = con;
		post.getElementsByClassName('interestPercent')[0].innerHTML= ip;
		post.getElementsByClassName('form_interestPercent')[0].setAttribute("value", ip);
		post.getElementsByClassName('repayLength')[0].setAttribute("value", '5');
		post.getElementsByClassName('form_to')[0].setAttribute("value", un);
		post.getElementsByClassName('postID')[0].setAttribute("value",data.postID);
		document.getElementById('feed').innerHTML += post.innerHTML;
	}	
	});

getJSON('/hackathon2020/site/scripts/getMoney.py',  function(err, val) {
	// amt money, owed/mont, total owed

	var amt = val.split('\n')[1];
	var monthly = val.split('\n')[2];
	var total = val.split('\n')[3];
	document.getElementById('moneyamt').innerHTML = '$' + Math.round(amt);
	//document.getElementById('moneyamt').innerHTML = '$' + monthly;
	document.getElementById('owedamt').innerHTML = '$' + Math.round(total);
});

