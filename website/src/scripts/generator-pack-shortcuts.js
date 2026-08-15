const generatorForm = document.querySelector("#radiopack-generator");
const packSelect = document.querySelector("#pack-select");
const shortcuts = document.querySelectorAll("[data-pack-shortcut]");

const selectPack = (packId) => {
  if (!(packSelect instanceof HTMLSelectElement)) return;

  const optionExists = Array.from(packSelect.options).some((option) => option.value === packId);
  if (!optionExists) return;

  packSelect.value = packId;
  packSelect.dispatchEvent(new Event("change", { bubbles: true }));
  generatorForm?.scrollIntoView({ behavior: "smooth", block: "start" });
  packSelect.focus({ preventScroll: true });
};

shortcuts.forEach((shortcut) => {
  if (!(shortcut instanceof HTMLElement)) return;

  const packId = shortcut.dataset.packShortcut;
  if (!packId) return;

  shortcut.tabIndex = 0;
  shortcut.setAttribute("role", "button");
  shortcut.setAttribute("aria-label", `Sélectionner le pack ${shortcut.dataset.packLabel ?? packId}`);

  shortcut.addEventListener("click", () => selectPack(packId));
  shortcut.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    selectPack(packId);
  });
});
