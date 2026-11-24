This is a pygame tower defense game I made
It of course requires pygame to be installed

<img width="1917" height="1080" alt="image" src="https://github.com/user-attachments/assets/5ae37e8e-560e-4e21-9147-13fe0b00eda1" />

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Pygame on GitHub Pages</title>
  <script src="https://jsdelivr.net"></script>
  <style>
    body { margin: 0; background: #111; display: flex; justify-content: center; align-items: center; height: 100vh; }
    canvas { border: 1px solid #444; }
  </style>
</head>
<body>
  <canvas id="canvas"></canvas>

  <script type="text/javascript">
    async function startPygame() {
      let pyodide = await loadPyodide();
      
      // 1. Load Pygame-CE (supports synchronous loops)
      await pyodide.loadPackage("pygame-ce");

      // 2. Bind the HTML canvas to SDL2
      const canvas = document.getElementById("canvas");
      pyodide.canvas.setCanvas2D(canvas);

      // 3. Fetch your untouched Python script and run it
      const response = await fetch("main.py");
      const code = await response.text();
      await pyodide.runPythonAsync(code);
    }
    startPygame();
  </script>
</body>
</html>
