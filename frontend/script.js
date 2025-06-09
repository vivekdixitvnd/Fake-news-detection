async function checkNews() {
  const newsText = document.getElementById('newsInput').value;
  console.log('Input text:', newsText);

  try {
    console.log('Sending request to API...');
        const res = await fetch('https://fake-news-detection-71hi.onrender.com/predict', {

    // const res = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: newsText })
    });

    console.log('API Response received');
    const data = await res.json();
    
    // Enhanced console logging
    console.log('=== Detailed API Response ===');
    console.log('Full Response Object:', JSON.stringify(data, null, 2));
    console.log('Result:', data.result);
    console.log('Confidence Score:', data.confidence + '%');
    console.log('Timestamp:', new Date().toLocaleString());
    console.log('==========================');

    if (data.error) {
      console.error('API Error:', data.error);
      document.getElementById('result').innerText = "Error: " + data.error;
    } else {
      document.getElementById('result').innerText =
        "Prediction: " + data.result + " (Confidence: " + data.confidence + "%)";
    }
  } catch (error) {
    console.error('=== Error Details ===');
    console.error('Error Type:', error.name);
    console.error('Error Message:', error.message);
    console.error('Stack Trace:', error.stack);
    console.error('===================');
    document.getElementById('result').innerText = "Unexpected Error Occurred!";
  }
}
