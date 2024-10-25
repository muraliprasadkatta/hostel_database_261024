// for state and pincode input field
const availableDist = {
    'Andhra Pradesh': ['Easte godavari','West godavari','Krishna'],
    'Telangana': ['Rnaga dist']
};

let availableKeywords = [];

// Populate availableKeywords from all states
for (const pinCodes of Object.values(availableDist)) {
    availableKeywords = availableKeywords.concat(pinCodes);
}

const resultBoxState = document.querySelector(".result-box-state");
const inputBoxState = document.getElementById("input-search-box-state");

const resultBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-search-box");

inputBoxState.addEventListener("input", function () {
    let result_n = [];
    let input_n = inputBoxState.value;

    if (input_n.length) {
        result_n = Object.keys(availableDist).filter((state) => {
            return state.toLowerCase().includes(input_n.toLowerCase());
        });
        console.log(result_n);
    }
    displayState(result_n, resultBoxState);

    if (!result_n.length) {
        resultBoxState.innerHTML = '';
    }
});

function displayState(result_n, resultBoxState) {
    const content = result_n.map((list) => {
        return "<li onclick=selectInputState(this)>" + list + "</li>";
    });
    resultBoxState.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInputState(list) {
    const selectedState = list.innerText;
    inputBoxState.value = selectedState;

    // Filter pin codes based on the selected state
    const selectedPinCodes = availableDist[selectedState] || [];
    display(selectedPinCodes, resultBox);

    // Clear the state suggestions
    resultBoxState.innerHTML = '';
}

inputBox.onkeyup = function () {
    let result = [];
    let input = inputBox.value;

    if (input.length) {
        result = availableKeywords.filter((pincode) => {
            return pincode.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);
    }
    display(result, resultBox);

    if (!result.length) {
        resultBox.innerHTML = '';
    }
};

function display(result, resultBox) {
    const content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });
    resultBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
}
