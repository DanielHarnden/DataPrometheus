/* Function for generating the input field, upload button, and API interaction on the mapDatabase page */
class mapDatabase extends HTMLElement {
    /* Sets initial values of element variables */
    constructor() {
        super();
        this.data = [];
    }

    /* Creates HTML structure of element, assigns DOM elements to instance properties, and adds event listeners for relevant forms */
    connectedCallback() {
        this.innerHTML = `
            <form method="POST" enctype="multipart/form-data">
                <label for="fileInput" id="fileInputLabel">Choose File to Upload</label>
                <input id="fileInput" type="file" name="file" onchange="updateLabel">
                <label for="allowReversing">Allow Reverse Database Mapping (may result in worse output in less complicated databases)</label>
                <input id="allowReversing" type="checkbox">
                <label for="fileUpload">Map Database</label>
                <input id="fileUpload" type="submit">
            </form>
            <br><br><br>
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
        /* TODO: Solve caught ReferenceError: updateLabel is not defined error. It doesn't break anything though, just clogs the console*/
        this.selectElement.addEventListener('change', this.updateLabel.bind(this));
    }

    handleFormSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const db = formData.get('file');
        const allowReversing = event.target.allowReversing.checked;
        this.showLoading();

        fetch(`http://localhost:5000/mapDatabase/${db}/${allowReversing}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(imageBlob => {
            const imageUrl = URL.createObjectURL(imageBlob);
            const resultImage = this.querySelector('#resultImage');
            resultImage.src = imageUrl;
            this.hideLoading();
        })
        .catch(error => {
            console.error('Error when handling the image:', error);
            this.hideLoading();
        });
    };

    removeImage() {
        const resultImage = this.querySelector('#resultImage');
        resultImage.src = "";
    }

    /* Handles the loading text */
    showLoading() {
        this.loadingContainer.style.display = 'block';
    }
    hideLoading() {
        this.loadingContainer.style.display = 'none';
    }
  
    /* Updates the input field updating to show the name of the selected file */
    updateLabel(event) {
        const fileInput = event.target;
        const fileInputLabel = document.getElementById("fileInputLabel");
        fileInputLabel.innerText = fileInput.files[0].name;
    }
}

customElements.define('map-database', mapDatabase);