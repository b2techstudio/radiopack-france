const generatorForm = document.querySelector("#radiopack-generator");
const packSelect = document.querySelector("#pack-select");

if (generatorForm && packSelect instanceof HTMLSelectElement) {
  const shortcutDefinitions = [
    { match: "Annecy", packId: "annecy-alpes-leman", label: "Annecy–Alpes–Léman" },
    { match: "Normandie", packId: "normandie", label: "Normandie" },
    { match: "Bretagne", packId: "bretagne", label: "Bretagne" },
  ];

  const selectPack = (packId) => {
    const optionExists = Array.from(packSelect.options).some((option) => option.value === packId);
    if (!optionExists) return;

    packSelect.value = packId;
    packSelect.dispatchEvent(new Event("change", { bubbles: true }));
    generatorForm.scrollIntoView({ behavior: "smooth", block: "start" });
    packSelect.focus({ preventScroll: true });
  };

  document.querySelectorAll(".info-grid .info-card").forEach((shortcut) => {
    if (!(shortcut instanceof HTMLElement)) return;

    const definition = shortcutDefinitions.find(({ match }) => shortcut.textContent?.includes(match));
    if (!definition) return;

    shortcut.dataset.packShortcut = definition.packId;
    shortcut.tabIndex = 0;
    shortcut.setAttribute("role", "button");
    shortcut.setAttribute("aria-label", `Sélectionner le pack ${definition.label}`);

    if (!shortcut.querySelector(".shortcut-action")) {
      const action = document.createElement("span");
      action.className = "shortcut-action";
      action.textContent = "Sélectionner ce pack ↑";
      shortcut.append(action);
    }

    shortcut.addEventListener("click", () => selectPack(definition.packId));
    shortcut.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      selectPack(definition.packId);
    });
  });
}
