document.addEventListener("DOMContentLoaded", function () {
    const root = document.getElementById("root");
  
    fetch("tasks.json")
      .then((res) => res.json())
      .then((tasks) => {
        const container = document.createElement("div");
        container.id = "gantt-target";
        root.appendChild(container);
  
        new Gantt(container, tasks, {
          view_mode: "Hour",
          on_click: (task) => {
            if (confirm(`Új részfeladatot szeretnél létrehozni ebből?\\n\\n${task.name}`)) {
              if (window.pywebview && window.pywebview.api && window.pywebview.api.create_subtask) {
                window.pywebview.api.create_subtask(task);
              } else {
                console.warn("Python API nem elérhető.");
              }
            }
          },
          custom_popup_html: task => {
            return `<div class="popup">
              <h4>${task.name}</h4>
              <p>${task.start} – ${task.end}</p>
            </div>`;
          }
        });
      })
      .catch((err) => {
        root.innerHTML = "<p style='color:red;'>Nem sikerült betölteni a task adatokat.</p>";
        console.error(err);
      });
  });