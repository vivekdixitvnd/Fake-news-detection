
async function checkNews() {
  const newsText = document.getElementById('newsInput').value;

  const res = await fetch('https://fake-news-detection-71hi.onrender.com/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: newsText })
  });

  const data = await res.json();
  document.getElementById('result').innerText =
    "Prediction: " + data.result + " (Confidence: " + data.confidence + "%)";
}
