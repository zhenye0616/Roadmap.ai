(() => {
    const API_BASE = 'http://localhost:8001';
  
    // Resume upload → /api/resume
    document.getElementById('resume-form').addEventListener('submit', async e => {
      e.preventDefault();
      const fileInput = document.getElementById('resume-file');
      if (!fileInput.files.length) return alert('Please select a file.');
  
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);
  
      try {
        const resp = await fetch(`${API_BASE}/api/resume`, {
          method: 'POST',
          body: formData
        });
        const data = await resp.json();
        document.getElementById('resume-result').textContent =
          JSON.stringify(data, null, 2);
      } catch (err) {
        document.getElementById('resume-result').textContent = 'Error: ' + err;
      }
    });
  
    // JD parsing → /api/jd (use FormData, not JSON)
    document.getElementById('jd-form').addEventListener('submit', async e => {
      e.preventDefault();
      const url = document.getElementById('jd-url').value.trim();
      if (!url) return alert('Please enter a URL.');
  
      const formData = new FormData();
      formData.append('url', url);
  
      try {
        const resp = await fetch(`${API_BASE}/api/jd`, {
          method: 'POST',
          body: formData
        });
        const data = await resp.json();
        document.getElementById('jd-result').textContent =
          JSON.stringify(data, null, 2);
      } catch (err) {
        document.getElementById('jd-result').textContent = 'Error: ' + err;
      }
    });
  })();
  