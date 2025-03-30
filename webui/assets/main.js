document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("timeline");
  console.log("✅ main.js betöltve");

  fetch("tasks.json")
    .then((res) => res.json())
    .then((data) => {
      console.log("📦 Betöltött taskok:", data);

      const items = data.map((task, index) => {
        const start = new Date(task.start);
        let end = new Date(task.end);

        // Ha ugyanaz, vagy túl rövid az időtartam, adjunk hozzá
        if (end.getTime() - start.getTime() < 5000) {
          end = new Date(start.getTime() + 60 * 1000); // +1 perc
        }

        return {
          id: index + 1,
          content: task.name || "Névtelen",
          start,
          end,
        };
      });

      console.log("🧱 Items:", items);

      const options = {
        stack: false,
        orientation: "top",
        margin: { item: 10, axis: 5 },
        zoomMin: 1000, // minimum 1 másodperces skála
        zoomMax: 1000 * 60 * 60, // max 1 óra
      };

      const timeline = new vis.Timeline(container, items, options);
      console.log("✅ Timeline létrehozva.");
    })
    .catch((err) => {
      console.error("❌ Nem sikerült betölteni a tasks.json-t:", err);
      container.innerHTML =
        "<p style='color:red;'>Nem sikerült betölteni az adatokat.</p>";
    });
});
