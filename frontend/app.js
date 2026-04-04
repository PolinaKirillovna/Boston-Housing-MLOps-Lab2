const formGrid = document.getElementById("form-grid");
const predictionForm = document.getElementById("prediction-form");
const predictionValue = document.getElementById("prediction-value");
const requestStatus = document.getElementById("request-status");
const fillDemoBtn = document.getElementById("fill-demo-btn");

let featureMetadata = [];

async function fetchJson(url, options = {}) {
    const response = await fetch(url, options);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`${response.status} ${response.statusText}: ${errorText}`);
    }
    return response.json();
}

function createField(feature) {
    const wrapper = document.createElement("div");
    wrapper.className = "field-card";

    const label = document.createElement("label");
    label.setAttribute("for", feature.name);
    label.textContent = feature.label;

    const meta = document.createElement("div");
    meta.className = "field-meta";
    meta.textContent = feature.description;

    let input;
    if (feature.name === "chas") {
        input = document.createElement("select");

        const optionNo = document.createElement("option");
        optionNo.value = "0";
        optionNo.textContent = "0 — No";

        const optionYes = document.createElement("option");
        optionYes.value = "1";
        optionYes.textContent = "1 — Yes";

        input.appendChild(optionNo);
        input.appendChild(optionYes);
    } else {
        input = document.createElement("input");
        input.type = "number";
        input.step = feature.type === "int" ? "1" : "any";
        input.placeholder = String(feature.placeholder);
    }

    input.id = feature.name;
    input.name = feature.name;
    input.required = true;
    input.dataset.valueType = feature.type;
    input.dataset.placeholderValue = String(feature.placeholder);

    wrapper.appendChild(label);
    wrapper.appendChild(meta);
    wrapper.appendChild(input);

    return wrapper;
}

function formatPrice(value) {
    return `$${value.toFixed(2)}k`;
}

function buildForm(features) {
    formGrid.innerHTML = "";
    features.forEach((feature) => {
        formGrid.appendChild(createField(feature));
    });
}

function fillDemoValues() {
    featureMetadata.forEach((feature) => {
        const element = document.getElementById(feature.name);
        if (element) {
            element.value = feature.placeholder;
        }
    });
}

function collectPayload() {
    const payload = {};

    featureMetadata.forEach((feature) => {
        const element = document.getElementById(feature.name);
        const rawValue = element.value.trim();

        if (rawValue === "") {
            throw new Error(`Field "${feature.label}" is required.`);
        }

        payload[feature.name] =
            feature.type === "int" ? parseInt(rawValue, 10) : parseFloat(rawValue);
    });

    return payload;
}

function renderPrediction(value) {
    predictionValue.textContent = formatPrice(value);
}

async function loadMetadata() {
    const metadataResponse = await fetchJson("/feature-metadata");
    featureMetadata = metadataResponse.features;
    buildForm(featureMetadata);
}

predictionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    requestStatus.textContent = "Sending request...";

    try {
        const payload = collectPayload();
        const response = await fetchJson("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        renderPrediction(response.predicted_medv);
        requestStatus.textContent = "Prediction completed successfully.";
    } catch (error) {
        requestStatus.textContent = `Error: ${error.message}`;
    }
});

fillDemoBtn.addEventListener("click", () => {
    fillDemoValues();
});

async function init() {
    try {
        await loadMetadata();
        fillDemoValues();
        requestStatus.textContent = "Frontend is connected to the API.";
    } catch (error) {
        requestStatus.textContent = `Initialization error: ${error.message}`;
    }
}

init();
