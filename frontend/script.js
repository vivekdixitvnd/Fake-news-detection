async function checkNews() {
  const newsText = document.getElementById('newsInput').value;

  try {
    const res = await fetch('https://fake-news-detection-71hi.onrender.com/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: newsText })
    });

    const data = await res.json();

    if (data.error) {
      document.getElementById('result').innerText = "Error: " + data.error;
    } else {
      document.getElementById('result').innerText =
        "Prediction: " + data.result + " (Confidence: " + data.confidence + "%)";
    }
  } catch (error) {
    document.getElementById('result').innerText = "Unexpected Error Occurred!";
    console.error(error);
  }
}
