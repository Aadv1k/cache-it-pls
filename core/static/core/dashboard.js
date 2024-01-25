const createJobBtn = document.getElementById("createJobBtn");
const editModal = document.getElementById("editModal");
const editModalForm = document.getElementById("editModalForm");
const doneBtn = document.getElementById("doneBtn");
const cancelBtn = document.getElementById("cancelBtn");
const deleteModal = document.getElementById("deleteModal");
const deleteDoneBtn = document.getElementById("deleteDoneBtn");
const deleteCancelBtn = document.getElementById("deleteCancelBtn");
const csrfToken = getCSRFToken();

document.querySelectorAll("#copyBtn").forEach(elem => {
    elem.addEventListener("click", async (event) => {
        const origin = (new URL(document.URL)).origin
        const url = `${origin}${event.target.dataset.url}`
        await navigator.clipboard.writeText(url);
    })
})

createJobBtn.addEventListener("click", showEditModal);
cancelBtn.addEventListener("click", closeEditModal);
editModalForm.addEventListener("submit", handleEditModalFormSubmit);
doneBtn.addEventListener("click", () => document.getElementById("editModalFormSubmitButton").click());

function handleEditModalFormSubmit(event) {
    event.preventDefault();
    const elem = event.target;
    const [timeNumeral, timeFrame] = Array.from(elem.querySelectorAll("select")).map(e => e.value);
    const rawURL = elem.querySelector("input[type='text']").value;

    try {
        const parsedURL = new URL(rawURL);
        fetch("/api/job/", {
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify({
                "time_int": timeNumeral,
                "time_frame": timeFrame,
                "url": parsedURL.href
            })
        }).then(async response => {
            const data = await response.json();
            if (!response.ok) {
                showErrorNotification(`Error: ${data.error}`);
                closeEditModal();
            } else {
                window.location.replace('/dashboard');
            }
        });
    } catch (err) {
        showErrorNotification("Invalid URL, You need to enter a valid one");
    }
}

function handleDeleteModal(event) {
    showDeleteModal();
    const id = event.target.dataset.id;
    deleteDoneBtn.addEventListener("click", async () => {
        const toDelete = event.target.dataset.id;
        const res = await fetch(`/api/job/${id}`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken,
            },
        });
        if (!res.ok) {
            showErrorNotification(`Was unable to delete job, due to code ${res.status}`);
        } else {
            window.location.replace('/dashboard');
        }
        closeDeleteModal();
    });
    deleteCancelBtn.addEventListener("click", closeDeleteModal);
}

function closeEditModal() {
    editModalForm.reset();
    editModal.classList.remove("is-active");
}

function showEditModal() {
    editModal.classList.add("is-active");
}

function showDeleteModal(event) {
    deleteModal.classList.add("is-active");
}

function closeDeleteModal(event) {
    deleteModal.classList.remove("is-active");
}

function showErrorNotification(message) {
    const errorNotification = document.getElementById("errorNotification");
    errorNotification.getElementsByTagName("p")[0].innerHTML = message;
    errorNotification.style = "display: block; z-index: 9999; width: fit-content; position: fixed; top: 1em; right: 1em";
    setTimeout(closeErrorNotification, 2500);
}

function closeErrorNotification() {
    document.getElementById("errorNotification").style.display = "none";
}

function getCSRFToken() {
    const csrfCookie = document.cookie.match(/csrftoken=([^ ;]*)/);
    return csrfCookie ? csrfCookie[1] : null;
}

function copy() {
    console.log(event)
}
