let previousInput = '';
let counter = 0;

function spellBadTimeCheck(event) {
    counter += 1;
    const callNum = counter;
    setTimeout(function () {
        if (previousInput !== input.value && callNum === counter) {
            counter = 0;
            previousInput = input.value;
            spellBad();
        }
    }, 500)
}

function spellBad() {
    let output = document.getElementById("output")
    let raw_input = input.value;

    if (raw_input.length === 0) {
        return setOutputPlaceholder(output)
    }

    let placeholderSpan = document.querySelector('[data-tooltip="Hover over a word to see where the spelling comes from"]');
    if (placeholderSpan) {
        placeholderSpan.style.opacity = 0;
        placeholderSpan.style.marginTop = 0;
        output.innerHTML = '';
    }

    let request = new XMLHttpRequest();
    request.open("POST", '/spellbad');
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = (e) => {
        if (request.readyState === 4 && request.status === 200) {
            let res = JSON.parse(request.responseText);
            let tooltips = [];
            output.innerHTML = '';
            for (let i = 0; i < res.words.length; i++) {
                output.innerHTML += res.words[i].badlySpelled.join('§');
                if (res.words[i].badlySpelled.join('') === res.words[i].word) {
                    tooltips.push([res.words[i].word]);
                    continue;
                }
                if (res.words[i].syllableOrigins) {
                    let tooltip = [];
                    for (let j = 0; j < res.words[i].syllableOrigins.length; j++) {
                        let sourceWord = res.words[i].syllableOrigins[j].word.join('');
                        tooltip.push(sourceWord);
                    }
                    tooltips.push(tooltip);
                }
            }
            output.style.color = '#000';
            prepareHighlights(output, tooltips);
        }
    }
    request.send(JSON.stringify({'text': raw_input}));
}

function prepareHighlights(element, tooltips) {
    let newHtml = '';
    let words = element.innerHTML.split(' ');
    for (let i = 0; i < words.length; i++) {
        const word = words[i].split('§');
        if (word[0] === "") {
            continue;
        }
        for (let j = 0; j < word.length; j++) {
            newHtml += '<span class="word" data-tooltip="' + tooltips[i][j] + '">' + word[j] + '</span>';
        }
        newHtml += '<span> </span>';
    }
    element.innerHTML = newHtml;

    let x = document.getElementsByClassName("word");
    for (let i = 0; i < x.length; i++) {
        x[i].addEventListener('mouseover', function() {
            $(this).addClass('hlight');
        });

        x[i].addEventListener('mouseout', function() {
            $(this).removeClass('hlight');
        });
    }
}

function setOutputPlaceholder(div) {
    div.innerHTML = '<span class="placeholder" data-placeholder-tooltip="Hover over a word to see the spelling origins">...bad xpeling comes out hear</span>';
    div.style.color = '#777';
}

const button = document.getElementById("read-more-button")
const p = document.getElementById("read-more")
button.addEventListener('click', function() {
    const rowHeight = $('#explanation-content')[0].scrollHeight;
    $('#explanation').animate({
        'max-height': '100%',
        'height': rowHeight,
        'overflow': 'visible',
        }, 'slow'
    );
    $('#read-more').animate({ 'opacity': 0 }, 'slow');
    $(this).animate({ 'opacity': 0 }, 'slow');
    $('#read-more').remove();
    $(this).remove();
});

let input = document.getElementById("input")
input.addEventListener("input", spellBadTimeCheck)
setOutputPlaceholder(document.getElementById("output"))
