class semanticMap extends HTMLElement {
    constructor() {
      super();
  
      // Create a shadow DOM
      this.attachShadow({ mode: "open" });
  
      // Create a button element
      const button = document.createElement("button");
  
      // Set the text content of the button
      button.textContent = "Call Flask API";
  
      // Add a click event listener to the button
      button.addEventListener("click", async () => {
        // Make a fetch request to your Flask API endpoint
        const response = await fetch("http://localhost:5000/trainMapper", {
          method: "POST", // or "GET"
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}), // replace with your request data
        });
  
        // Get the response data as JSON
        const data = await response.json();
  
        // Log the response data to the console
        console.log(data);
      });
  
      // Append the button to the shadow DOM
      this.shadowRoot.appendChild(button);
    }
  }
  
  // Define the custom element
  customElements.define("semantic-mapper", semanticMap);