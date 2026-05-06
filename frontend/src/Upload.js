import axios from "axios";

function Upload() {
  const upload = async (e) => {
    const form = new FormData();
    form.append("file", e.target.files[0]);

    await axios.post("http://127.0.0.1:8000/upload", form);
    alert("Uploaded!");
  };

  return (
    <div className="upload-card">
      <label className="upload-area">
        <input type="file" onChange={upload} hidden />
        <div>
          <p>📂 Upload File</p>
          <span>PDF, Audio, Video</span>
        </div>
      </label>
    </div>
  );
}

export default Upload;