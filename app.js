const url = "http://127.0.0.1:9090/";
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
      if (data.status === 201) {
        const audio = document.getElementById("audio");
        // document.getElementById("play-pdf").removeAttribute("hidden");
        document.getElementById("upload").setAttribute("aria-busy", "false");
        audio.setAttribute('src', data.audio )
        audio.load();
        audio.play();
      }
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

document.body.onload = () => {
  const data = getData();

  let audioItems = document.getElementsByClassName("recent-items");
};

async function getData() {
  try {
    const recent = document.getElementById("recent");
    const response = await fetch(url);
    const result = await response.json().then((data) => {
      for (let item in data.audios) {
        const div = document.createElement("div");
        const h6 = document.createElement("h6");
        const audioPlayer = document.createElement("audio");
        audioPlayer.setAttribute('controls', '')
        audioPlayer.setAttribute("src", data.audios[item]);
        h6.innerText = item;
        h6.classList.add("recent-items");
        div.appendChild(h6);
        div.appendChild(audioPlayer)
        recent.appendChild(div);
      }
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

async function playAudio() {
  try {
    let items = document.getElementsByClassName("recent-items");
    if (items.length > 0) {
      for (let i = 0; i < items.length; i++) {
        console.log(items[i]);
      }
    } else {
      console.log("not elements found");
    }
  } catch (err) {
    console.log(err);
    playAudio();
  }
}
playAudio();
