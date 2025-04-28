// Here, get all the buttons that were selected 
const selectedSurgeries = document.querySelectorAll('#surgery-options .btn-check')
const submitButton = document.getElementById('submit-btn')
const disableButton = document.getElementById('reset-btn')
const currImage = document.getElementById('image');

submitButton.addEventListener('click', function(event){
    event.preventDefault(); 
  
    // Clear previous images 
    currImage.innerHTML = ''; 
    
    // Disable submit button immediately
    submitButton.disabled = true;
  
    const selected = [];
  
    // Look for all surgeries that were selected
    selectedSurgeries.forEach(surgery => {
        if (surgery.checked) {
            selected.push(surgery.value);
        }
    });
  
    // If no selection then alert 
    if (selected.length === 0) {
        alert('No surgery selected. Please select at least one');
        submitButton.disabled = false; 
        return;
    }
    // Show loading as the image loads
    currImage.classList.add('image-loading');
    currImage.innerHTML = '<p style="text-align:center; font-size:1.2em;">Loading...</p>';

    const surgeryChoices = new FormData();
    surgeryChoices.append('surgeries', selected.join(', '));
  
    fetch('/response', {
        method: 'POST',
        body: surgeryChoices
    })
    .then(response => response.json())
    .then(data => {
        // Actually load the new image
        const imageData = data.image_bytes;
        displayImage(`data:image/png;base64,${imageData}`);
  
        selectedSurgeries.forEach(button => {
        button.checked = false;
      });

      // Enable for reset 
      disableButton.disabled = false; 
    })
    // Catch anything here 
    .catch(error => {
        console.error('Error:', error);

        // Reset the loading screen to normal 
        currImage.classList.remove('image-loaded', 'image-loading');
    
        submitButton.disabled = false;
        alert('Failed to generate image. Please try again.');
    });
});
  
// Reset everything if not already 
disableButton.addEventListener('click', function(event){
    // Clear any photos 
    currImage.innerHTML = ''; 
    // Replace with "Awaiting image..."
    currImage.classList.remove('image-loaded', 'image-loading');
    disableButton.disabled = true;
    submitButton.disabled = false;
});

// Helper function to display the image generated from ChatGPT
function displayImage(src) {
    const container = document.getElementById('image');
    document.getElementById('image').classList.add('image-loaded');
    container.innerHTML = `<img src="${src}" alt="Generated result" style="max-width:100%; max-height:100%;" />`;
}
