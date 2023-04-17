const url = "http://127.0.0.1:5000/";

document.getElementById("form").addEventListener("submit", function (e) {
  e.preventDefault();
  const file = document.getElementById("uploadFile").files[0];
  const filename = document.getElementById("fileName").value;
  document.getElementById("audio-header").innerText = filename;
  const formData = new FormData();
  formData.append("pdf_file", file);
  document.getElementById("upload").setAttribute("aria-busy", "true");
  upload(formData);
});

async function upload(formData) {
  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });
    setTimeout(() => {
      console.log("waiting...");
    }, 1000);
    const result = await response.json().then((data) => {
      if (data.isSuccess === true) {
        const audio = document.getElementById("audio");
        const audioSrc = document.getElementById("audio-src");
        audio.removeAttribute("hidden");
        document.getElementById("upload").setAttribute("aria-busy", "false");
        audio.load();
        audio.play();
      }
    });
  } catch (error) {
    console.error("Error:", error);
  }
}
