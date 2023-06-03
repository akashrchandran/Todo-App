const editButton = document.getElementById('edit');
const deleteButton = document.getElementById('delete');

deleteButton.addEventListener('click', async () => {
    const id = deleteButton.getAttribute('data-id');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch(`/delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ id: id }),
    })
    const data = await response.json();
    if (data.status === 200) {
        location.reload();
    }
});