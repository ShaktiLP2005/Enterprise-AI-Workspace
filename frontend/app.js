const API_BASE_URL = "http://localhost:8000";


// --------------------------------------------------
// Document selection
// --------------------------------------------------

const fileInput = document.getElementById("fileInput");
const selectedFiles = document.getElementById("selectedFiles");

fileInput.addEventListener("change", () => {

    selectedFiles.innerHTML = "";

    const files = Array.from(fileInput.files);

    files.forEach(file => {

        const fileElement = document.createElement("div");

        fileElement.className = "file-item";
        fileElement.textContent = file.name;

        selectedFiles.appendChild(fileElement);
    });
});


// --------------------------------------------------
// Upload documents
// --------------------------------------------------

const uploadButton = document.getElementById("uploadButton");
const uploadStatus = document.getElementById("uploadStatus");

uploadButton.addEventListener("click", async () => {

    const files = Array.from(fileInput.files);

    if (files.length === 0) {
        uploadStatus.textContent = "Please select at least one document.";
        return;
    }

    const formData = new FormData();

    files.forEach(file => {
        formData.append("files", file);
    });

    uploadButton.disabled = true;
    uploadStatus.textContent = "Uploading and ingesting documents...";

    try {

        const response = await fetch(
            `${API_BASE_URL}/upload/`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Document upload failed."
            );
        }

        uploadStatus.textContent =
            `${data.documents.length} document(s) uploaded and ingested successfully.`;

    } catch (error) {

        uploadStatus.textContent =
            `Error: ${error.message}`;

    } finally {

        uploadButton.disabled = false;
    }
});


// --------------------------------------------------
// Query documents
// --------------------------------------------------

const queryInput = document.getElementById("queryInput");
const queryButton = document.getElementById("queryButton");

const queryStatus = document.getElementById("queryStatus");

const answerSection = document.getElementById("answerSection");
const answerElement = document.getElementById("answer");

const sourcesSection = document.getElementById("sourcesSection");
const sourcesElement = document.getElementById("sources");


queryButton.addEventListener("click", async () => {

    const query = queryInput.value.trim();

    if (!query) {
        queryStatus.textContent = "Please enter a question.";
        return;
    }

    queryButton.disabled = true;
    queryStatus.textContent = "Searching documents...";

    answerSection.style.display = "none";
    sourcesSection.style.display = "none";

    try {

        const response = await fetch(
            `${API_BASE_URL}/query/?query=${encodeURIComponent(query)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Query failed."
            );
        }

        // Display answer

        answerElement.textContent = data.answer;

        answerSection.style.display = "block";


        // Display sources

        sourcesElement.innerHTML = "";

        data.sources.forEach(source => {

            const sourceElement = document.createElement("div");

            sourceElement.className = "source";

            sourceElement.innerHTML = `
                <strong>${source.filename}</strong>
                <span>
                    Distance: ${source.distance.toFixed(4)}
                </span>
            `;

            sourcesElement.appendChild(sourceElement);
        });

        sourcesSection.style.display = "block";

        queryStatus.textContent = "";

    } catch (error) {

        queryStatus.textContent =
            `Error: ${error.message}`;

    } finally {

        queryButton.disabled = false;
    }
});