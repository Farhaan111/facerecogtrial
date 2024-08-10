document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('file');
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/recognize', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    document.getElementById('result').innerText = result.message;
});
