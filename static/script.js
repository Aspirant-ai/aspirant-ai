async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function generateQuestions() {
    const topic = document.getElementById('topic').value;
    const output = document.getElementById('questions-output');
    output.innerHTML = '<div class="loading">Generating questions...</div>';

    try {
        const response = await postData('/generate_questions', { topic });
        output.innerHTML = '<ol>' + 
            response.questions.map(q => `<li>${q}</li>`).join('') + 
            '</ol>';
    } catch (error) {
        output.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function askDoubt() {
    const question = document.getElementById('doubt').value;
    const output = document.getElementById('explanation-output');
    output.innerHTML = '<div class="loading">Analyzing your doubt...</div>';

    try {
        const response = await postData('/ask_doubt', { question });
        output.innerHTML = `<div class="explanation">${response.explanation}</div>`;
    } catch (error) {
        output.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}
