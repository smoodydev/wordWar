// Base Variables

let num_letters = 5;
let num_attempts = 5;
let attempt = 0;
let letter_index = 0;

// Base functions for both Keybinds and Fake Keyboard

function enter_letter(letter) {
    if (letter_index < num_letters) {
        $(`#li${attempt}${letter_index}`).text(letter);
        letter_index++;
    }
    console.log(letter_index, num_letters, attempt)
}

function clear_line(line = attempt) {
    $(`#word_input-${line} .letter_input`).text("");
    letter_index = 0;
}

function last_letter() {
    if (letter_index > 0) {
        letter_index--;
        $(`#li${attempt}${letter_index}`).text("");
    }

}


// retrieves word for sending
function get_word() {
    let word_attempt = "";
    for (let i = 0; i < num_letters; i++) {
        word_attempt += ($(`#li${attempt}${i}`).text());
    }
    return word_attempt;
}

// Paints returned cell based on validity

function paintCells(result, word_attempt) {
    console.log(attempt)
    for (let i = 0; i < result.length; i++) {
        $(`#li${attempt}${i}`).addClass(result[i]);
        console.log(word_attempt);
        console.log(`#li${attempt}${i}`);
        $(`.keyboard_key[value='${word_attempt[i]}']`).addClass("used")
    }
}


function try_word() {
    let word_attempt = get_word().toLocaleLowerCase();
    if (word_attempt.length == num_letters) {
        $.post($SCRIPT_ROOT + '/try_word', {
            word: word_attempt
        }, function (data) {
            if (data.validated) {
                wordsent = "";
                paintCells(data.result, word_attempt);
                $("#result").text("Result for " + word_attempt);
                attempt++;
                letter_index = 0;
            }
            else {
                $("#result").text(word_attempt + " is not a valid word");
            }
        });
    }

}

$('#new_word').bind('click', function () {
    $.post($SCRIPT_ROOT + '/new_word', {
        function(data) {
            $("#result").text("You received a new word!");
            attempt = 0;
            letter_index = 0;
            generate_board();
            generate_keyboard();

        }
    });

    return false;
});





let generate_board = () => {
    $("#game_board").empty();
    for (let i = 0; i <= num_attempts; i++) {
        $("#game_board").append(`<div id="word_input-${i}" class="word_input" name="${i}"></div>`);
        for (let j = 0; j < num_letters; j++) {
            $(`#word_input-${i}`).append(`<div id="li${i}${j}" class="letter_input" name="${j}"></div>`);
        }
    }


};


let keyboard_keys = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

let generate_keyboard = () => {
    $("#keyboard").empty();

    for (let i = 0; i < keyboard_keys.length; i++) {
        $("#keyboard").append(`<div id="keyboard_row-${i}" class="keyboard_row"></div>`);
        for (let j = 0; j < keyboard_keys[i].length; j++) {
            $(`#keyboard_row-${i}`).append(`<button class="keyboard_key" value="${keyboard_keys[i][j]}">${keyboard_keys[i][j].toUpperCase()}</button>`);

        }
    }

    $("#keyboard").append(`
        <div class="keyboard_row">
            <button id="clear" class="keyboard_action">Clear</button>
            <button id="back" class="keyboard_action">Back</button>
            <button id="enter" class="keyboard_action">Enter</button>
        </div>`);

    $(".keyboard_key").click(function () {
        enter_letter($(this).val().toLocaleUpperCase())
    });

    $('#enter').bind('click', function () {
        try_word();
        return false;
    });

    $('#back').bind('click', function () {

        last_letter();
        return false;
    });

    $('#clear').bind('click', function () {

        clear_line();
        return false;
    });


}

generate_board();
generate_keyboard();

$("body").keydown(function (event) {
    let keydown = event.which;
    if (keydown >= 65 && keydown <= 90) {
        let letter_in = String.fromCharCode(keydown)
        enter_letter(letter_in.toLocaleUpperCase())
    }
    else if (keydown == 13) {
        event.preventDefault();
        $('#enter').focus();
        try_word();

    } else if (keydown == 46) {
        clear_line();

    }
    else if (keydown == 8) {
        last_letter();

    }

});
