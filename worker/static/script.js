const editButton = document.querySelectorAll(".editBtn");
const deleteButton = document.querySelectorAll(".deleteBtn");
const checkButton = document.querySelectorAll(".checkBtn");
const toast = document.getElementById('liveToast');
const myModal = document.getElementById('myModal');
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
const modal = new bootstrap.Modal(myModal);


postServer = async (btn, event, payload = {}) => {
  const id = btn.getAttribute("data-id");
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const response = await fetch(`/${event}/${id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(payload),
  });
  if (response.ok) {
    location.reload();
  } else {
    const toastBody = document.getElementsByClassName('toast-body');
    const data = await response.json();
    toastBody[0].textContent = data.msg;
    toastBootstrap.show();
  }
};

deleteButton.forEach((btn) => {
  btn.addEventListener("click", () => {
    postServer(btn, "delete");
  });
});

checkButton.forEach((btn) => {
  btn.addEventListener("click", () => {
    postServer(btn, "complete");
  });
});

editButton.forEach((btn) => {
  btn.addEventListener("click", () => {
    const taskBtn = document.getElementById('updatedTask');
    const dateBtn = document.getElementById('updatedDate');
    taskBtn.value = btn.closest('.list-group-item').textContent.trim();
    dateBtn.value = btn.getAttribute("data-date");
    modal.show();
    document.getElementById("saveEdit").addEventListener("click", () => {
      postServer(btn, "update", { updatedTask: taskBtn.value, updatedDate: dateBtn.value });
    });
  });
}
);