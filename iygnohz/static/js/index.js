$(document).ready(function() {
    var $message = "Hi, I'm Dai ZhongYi.".split('').reverse();
    var $timeout = 120;

    var outputSlowly = setInterval(function() {

        $('#forme').append($message.pop());

        if ($message.length === 0) {
            clearInterval(outputSlowly);
        }

    }, $timeout);
});
