/* Function for generating the input field, upload button, and API interaction on the mapDatabase page */
class dataPrometheusAPI extends HTMLElement {
    /* Sets initial values of element variables */
    constructor() {
        super();
        this.data = [];
    }

    /* Creates HTML structure of element, assigns DOM elements to instance properties, and adds event listeners for relevant forms */
    connectedCallback() {
        this.innerHTML = `
            <form method="POST" enctype="multipart/form-data">
                <label for="fileInput" id="fileInputLabel">Choose File(s)</label>
                <input id="fileInput" type="file" multiple name="file">
                <label for="fileUpload">Upload File(s)</label>
                <input id="fileUpload" type="submit">
            </form>
            <br>
            <div id="returnedImage">
                <img id="resultImage" src="">
            </div>
            <div id="loading" style="display:none">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        this.formElement = this.querySelector('form');
        this.selectElement = this.querySelector('input');
        this.loadingContainer = this.querySelector('#loading');
        this.formElement.addEventListener('submit', this.handleFormSubmit);
        this.formElement.addEventListener('submit', this.removeImage.bind(this));
        this.selectElement.addEventListener('change', this.updateLabel.bind(this));
    }

    handleFormSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const currentURL = window.location.href;
        const endpoint = currentURL.replace(window.location.origin, '').split('.')[0];
        this.showLoading();

        fetch(`http://localhost:5000/dataPrometheusAPI/${endpoint}`, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const contentType = response.headers.get('Content-Type');
                if (contentType && contentType.startsWith('image')) {
                    return response.arrayBuffer();
                } else {
                    return response.text();
                }
            })
            .then(data => {
                if (typeof data === 'string') {
                    console.log(data);
                    this.updateLoadingError(data);
                } else if (data instanceof ArrayBuffer) {
                    const blob = new Blob([data], { type: 'image/png' });
                    const imageUrl = URL.createObjectURL(blob);
                    const resultImage = document.querySelector('#resultImage');
                    resultImage.src = imageUrl;
                    this.hideLoading();
                }
            })
            .catch(error => {
                console.error(error);
            });
    };

    removeImage() {
        const resultImage = this.querySelector('#resultImage');
        resultImage.src = "";
    }

    /* Handles the loading text */
    showLoading() {
        this.loadingContainer.textContent = "Loading...";
        this.loadingContainer.style.display = 'block';
    }
    hideLoading() {
        this.loadingContainer.style.display = 'none';
    }

    updateLoadingError(errorMessage) {
        this.loadingContainer.textContent = errorMessage;
    }

    /* Updates the input field updating to show the name of the selected file */
    updateLabel(event) {
        const fileInput = event.target;
        const fileInputLabel = document.getElementById("fileInputLabel");

        if (fileInput.files.length === 1) {
            fileInputLabel.innerText = fileInput.files[0].name;
        } else if (fileInput.files.length > 1) {
            let fileNames = '';
            for (let i = 0; i < fileInput.files.length; i++) {
                fileNames += fileInput.files[i].name;
                if (i !== fileInput.files.length - 1) {
                    fileNames += ', ';
                }
            }
            fileInputLabel.innerText = fileNames;
        } else {
            fileInputLabel.innerText = 'Upload File(s)';
        }
    }
}

customElements.define('data-prometheus', dataPrometheusAPI);



/* Creates a button that is used to return to the index page */
class returnToMenu extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.innerHTML = `
        <a href="./index.html" class="menuButton">
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-left">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
            </span>
        </a>
        `;
    }
}

customElements.define('main-menu', returnToMenu);



/* Used for the menu background panning effect */
const menu = document.getElementById("menu");
Array.from(document.getElementsByClassName("menuItem"))
    .forEach((item, index) => {
        item.onmouseover = () => {
            menu.style.setProperty("--active-index", index)
        }
    });