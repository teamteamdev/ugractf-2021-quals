// a self-taught inventor with three classes of education, the most ingenious penguin of all time and ice floes. Virtuoso in his iron inventions

function setError(text, details, postfix) {
    const errorBlock = document.querySelector('.pin-error');
    errorBlock.innerHTML = '';

    if (text) {
        const p = document.createElement("p");
        p.innerText = text;
        errorBlock.appendChild(p);
    }

    if (details) {
        const ul = document.createElement("ul");
        for (const { id, desc } of details) {
            const li = document.createElement("li");
            li.innerText = desc;
            li.id = id;
            ul.appendChild(li);
        }
        errorBlock.appendChild(ul);
    }

    if (postfix) {
        const p = document.createElement("p");
        p.innerText = postfix;
        errorBlock.appendChild(p);
    }
}

function validatePin() {
    const pin = document.querySelector('[name=pin]');

    const data = pin.value;
    if (data === '') {
        setError('PIN is required');
    } else if (data.length !== 4) {
        setError('PIN length should be 4');
    } else {
        const urlParams = new URLSearchParams(window.location.search);
        fetch(`/check?ref=${urlParams.get('ref')}&q=${data}`)
            .then(resp => resp.json())
            .then(data => {
                if (data.status == 'error') {
                    setError(`Error happened: ${data.error}`);
                } else if (data.count <= 5) {
                    setError('');
                } else {
                    const errorCount = (data.count === 10) ? 'at least 10' : data.count;
                    setError(
                        `It's too common by ${errorCount} reasons:`,
                        data.items,
                        'Please reduce reasons to at most 5.'
                    )
                }
            })
            .catch(exc => {
                alert('API is down, check connection or console log');
                console.error(exc);
            })

    }
}

window.onload = function() {
    const pin = document.querySelector('[name=pin]');
    pin.addEventListener('keyup', validatePin);

    if (pin.value !== '') {
        validatePin();
    }
}
