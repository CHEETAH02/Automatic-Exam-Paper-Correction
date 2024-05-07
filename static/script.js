let counts = {
    MCQ: 0,
    FITB: 0,
    Equation: 0,
    Brief: 0
};

const toggleDiv = (type) => {
    const div = document.getElementById(`${type.toLowerCase()}_div`);
    const activateButton = document.getElementById(`${type.toLowerCase()}_toggle`);

    if (div.style.display === "none") {
        activateButton.innerText = `Disable ${type} Questions`;
        div.style.display = "inline";
    } else {
        activateButton.innerText = `Enable ${type} Questions`;
        div.style.display = "none";
    }
};

const addQuestion = (type) => {
    counts[type]++;
    let optionCount = 1;
    document.getElementById(`${type.toLowerCase()}_count`).value++;

    const newDiv = document.createElement('div');
    newDiv.setAttribute('id', `${type.toLowerCase()}div${counts[type]}`);

    newDiv.appendChild(createLabelElement(`${type} ${counts[type]}`, `${type.toLowerCase()}${counts[type]}`));
    newDiv.appendChild(createInputElement('text', `${type.toLowerCase()}${counts[type]}`, `${type.toLowerCase()}${counts[type]}`, 'text-black', '1000px'));

    newDiv.appendChild(document.createElement('br'));
    newDiv.appendChild(document.createElement('br'));

    if (type === "MCQ") {
        for (let option of ['a', 'b', 'c', 'd']) {
            newDiv.appendChild(createLabelElement(`${option}. `, `op${counts[type]}${optionCount}`));
            newDiv.appendChild(createInputElement('text', `op${counts[type]}${optionCount}`, `op${counts[type]}${optionCount}`, 'text-black', ''));
            optionCount++;
        }
    }

    newDiv.appendChild(createLabelElement('Answer. ', `q${counts[type]}ans${counts[type]}`));
    if (type == "MCQ") {
        const input = createInputElement('number', `q${counts[type]}ans${counts[type]}`, `${type.toLowerCase()}_ans${counts[type]}`, 'text-black', '');
        input.setAttribute('min', '1');
        input.setAttribute('max', '4');
        newDiv.appendChild(input);
    }
    else {
        newDiv.appendChild(createInputElement('text', `q${counts[type]}ans${counts[type]}`, `${type.toLowerCase()}_ans${counts[type]}`, 'text-black', ''));
    }

    newDiv.appendChild(document.createElement('br'));
    newDiv.appendChild(document.createElement('br'));

    const parentDiv = document.getElementById(`${type.toLowerCase()}_div`);
    parentDiv.insertBefore(newDiv, document.getElementById(`${type.toLowerCase()}_add`));
};

const removeQuestion = (type) => {
    if (counts[type] > 0) {
        document.getElementById(`${type.toLowerCase()}div${counts[type]--}`).remove();
        document.getElementById(`${type.toLowerCase()}_count`).value -= 1;
    }
};

const createInputElement = (type, id, name, className, style) => {
    const input = document.createElement('input');
    input.setAttribute('type', type);
    input.setAttribute('id', id);
    input.setAttribute('name', name);
    input.setAttribute('class', className);
    input.style.width = style;
    return input;
};

const createLabelElement = (text, forAttribute) => {
    const label = document.createElement('label');
    label.setAttribute('for', forAttribute);
    label.innerText = text;
    return label;
};

document.getElementById('mcq_toggle').addEventListener('click', () => toggleDiv('MCQ'));
document.getElementById('mcq_add').addEventListener('click', () => addQuestion('MCQ'));
document.getElementById('mcq_remove').addEventListener('click', () => removeQuestion('MCQ'));

document.getElementById('fitb_toggle').addEventListener('click', () => toggleDiv('FITB'));
document.getElementById('fitb_add').addEventListener('click', () => addQuestion('FITB'));
document.getElementById('fitb_remove').addEventListener('click', () => removeQuestion('FITB'));

document.getElementById('equation_toggle').addEventListener('click', () => toggleDiv('Equation'));
document.getElementById('equation_add').addEventListener('click', () => addQuestion('Equation'));
document.getElementById('equation_remove').addEventListener('click', () => removeQuestion('Equation'));

document.getElementById('brief_toggle').addEventListener('click', () => toggleDiv('Brief'));
document.getElementById('brief_add').addEventListener('click', () => addQuestion('Brief'));
document.getElementById('brief_remove').addEventListener('click', () => removeQuestion('Brief'));
