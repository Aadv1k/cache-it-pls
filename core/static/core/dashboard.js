const createJobBtn = document.getElementById("createJobBtn")

const editModal = document.getElementById("editModal");
const editModalForm = document.getElementById("editModalForm");
const doneBtn = document.getElementById("doneBtn");

createJobBtn.addEventListener("click", showEditModal)

editModalForm.addEventListener("submit", handleEditModalFormSubmit)

doneBtn.addEventListener("click", () => {
    document.getElementById("editModalFormSubmitButton").click()
})


function handleEditModalFormSubmit(event) {
    event.preventDefault();
    const elem = event.target;

    const [timeNumeral, timeFrame] = Array.from(elem.querySelectorAll("select")).map(e => e.value);
    const rawURL = elem.querySelector("input[type='text']").value;
    const csrfToken = elem.querySelector("input[type='hidden']").value;

    let parsedURL;

    try {
        parsedURL = new URL(rawURL);
    } catch (err) {
        showErrorNotification("Invalid URL, You need to enter a valid one");
        return;
    }


    console.log(rawURL, timeFrame, timeNumeral, csrfToken)

    fetch("/api/job", {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
            "time_int": timeNumeral,
            "time_frame": timeFrame,
            "url": parsedURL.href
        })})
        .then(response => {
        if (!response.ok) {
            showErrorNotification("Something went wrong when trying to fetch a response");
        } 

        // TEMP: closeEditModal();
        editModalForm.reset()
    });
}


function closeEditModal() {
    editModal.classList.remove("is-active");
}

function showEditModal() {
    editModal.classList.add("is-active");
}

function showDeleteModal() {
    alert("TBD");
}

function showErrorNotification(message) {
    const errorNotification = document.getElementById("errorNotification");

    errorNotification.innerText = message

    errorNotification.style.display = "block";
    errorNotification.style.zIndex = "9999";
    errorNotification.style.width = "fit-content"
    errorNotification.style.position = "fixed"
    errorNotification.style.top = "1em"
    errorNotification.style.right = "1em"

    setTimeout(closeErrorNotification, 1500)
}

function closeErrorNotification() {
    const errorNotification = document.getElementById("errorNotification");
    errorNotification.style.display = "none";
}
