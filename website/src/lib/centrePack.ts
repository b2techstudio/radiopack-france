import { buildMetropolitanPack } from "./metropolitanPack";
import { validatePlacedChannels, type Channel, type PlacedChannel } from "./chirpPack";

export const centreV03Version = "v0.3";
export const centreV03MemoryCount = 51;
export const centreV03Filename = "radiopack-france-centre-val-de-loire-v0.3.csv";

const aviationChannels: Channel[] = [
  { name: "AIR-EMERG", frequency_mhz: 121.5, mode: "AM", step_khz: 8.33, comment: "Urgence aviation 121.500 MHz · RX seule" },
  { name: "TUF-TWR", frequency_mhz: 124.4, mode: "AM", step_khz: 8.33, comment: "Tours Val de Loire LFOT TWR/AFIS/A-A · SIA AIRAC 08/26 · RX seule" },
  { name: "CHR-TWR1", frequency_mhz: 125.88, mode: "AM", step_khz: 8.33, comment: "Chateauroux Deols LFLX TWR/AFIS/A-A · SIA courant 2026-08-20 · RX seule" },
  { name: "CHR-TWR2", frequency_mhz: 133.805, mode: "AM", step_khz: 8.33, comment: "Chateauroux Deols LFLX frequence auxiliaire · SIA AIRAC 08/26 · RX seule" },
  { name: "BOU-AFIS", frequency_mhz: 119.605, mode: "AM", step_khz: 8.33, comment: "Bourges LFLD AFIS/A-A · SIA AIRAC 08/26 · RX seule" },
  { name: "BLO-AFIS", frequency_mhz: 118.455, mode: "AM", step_khz: 8.33, comment: "Blois Le Breuil LFOQ AFIS/A-A · SIA AIRAC 08/26 · RX seule" },
  { name: "SDH-AFIS", frequency_mhz: 122.405, mode: "AM", step_khz: 8.33, comment: "Saint-Denis-de-l'Hotel LFOZ AFIS/A-A · SIA courant · RX seule" },
];

const newRadioChannels: Channel[] = [
  { name: "F5ZSQ-O", frequency_mhz: 430.275, mode: "FM", step_khz: 12.5, comment: "Bonneval F5ZSQ sortie RX · REF courant + seconde source · 2026-08-20" },
  { name: "F5ZSQ-I", frequency_mhz: 431.875, mode: "FM", step_khz: 12.5, comment: "Bonneval F5ZSQ entree RX · REF courant + seconde source · 2026-08-20" },
  { name: "F5ZXW-V", frequency_mhz: 145.2875, mode: "FM", step_khz: 12.5, comment: "Celon F5ZXW VHF crossband RX · REF + RepeaterBook · 2026-08-20" },
  { name: "F5ZXW-U", frequency_mhz: 431.0875, mode: "FM", step_khz: 12.5, comment: "Celon F5ZXW UHF crossband RX · REF + RepeaterBook · 2026-08-20" },
  { name: "F6ZAW-V", frequency_mhz: 145.575, mode: "FM", step_khz: 12.5, comment: "Vineuil F6ZAW VHF crossband RX · REF + RepeaterBook/AR ALEC · 2026-08-20" },
  { name: "F6ZAW-U", frequency_mhz: 433.5375, mode: "FM", step_khz: 12.5, comment: "Vineuil F6ZAW UHF crossband RX · REF + AR ALEC · 2026-08-20" },
  { name: "F5ZUZ-O", frequency_mhz: 430.3375, mode: "FM", step_khz: 12.5, comment: "Saint-Epain F5ZUZ sortie RX · REF + RepeaterBook/local · 2026-08-20" },
  { name: "F5ZUZ-I", frequency_mhz: 439.7375, mode: "FM", step_khz: 12.5, comment: "Saint-Epain F5ZUZ entree RX · REF + source locale · 2026-08-20" },
  { name: "F5ZAP-O", frequency_mhz: 430.375, mode: "FM", step_khz: 12.5, comment: "Egry F5ZAP sortie analogique RX · REF + F5KIA · 2026-08-20" },
  { name: "F5ZAP-I", frequency_mhz: 439.775, mode: "FM", step_khz: 12.5, comment: "Egry F5ZAP entree analogique RX · REF + F5KIA · 2026-08-20" },
  { name: "F1ZFY-O", frequency_mhz: 433.3, mode: "FM", step_khz: 12.5, comment: "Orleans F1ZFY sortie RX · REF courant · 2026-08-20" },
  { name: "F1ZFY-I", frequency_mhz: 434.9, mode: "FM", step_khz: 12.5, comment: "Orleans F1ZFY entree RX · REF courant · 2026-08-20" },
];

const keptV02Calls = new Set(["F5ZHF", "F5ZDE", "F5ZVB", "F5ZLP"]);

export const buildCentreV03Pack = (): PlacedChannel[] => {
  const base = buildMetropolitanPack("centre-val-de-loire", "v0.2");
  const national = base.filter(({ location }) => location < 40);
  const keptRepeaters = base.filter(({ channel }) => {
    const call = channel.name.split("-")[0];
    return keptV02Calls.has(call);
  });
  const aviation = aviationChannels.map((channel, index) => ({
    location: 40 + index,
    block: "AVIATION_V03",
    channel,
  }));
  const additions = newRadioChannels.map((channel, index) => ({
    location: 82 + index,
    block: "RADIOAMATEUR_V03",
    channel,
  }));
  const placed = [...national, ...aviation, ...keptRepeaters, ...additions].sort((a, b) => a.location - b.location);
  validatePlacedChannels(placed);
  if (placed.length !== centreV03MemoryCount) {
    throw new Error(`Centre-Val de Loire ${centreV03Version}: ${placed.length} memories, expected ${centreV03MemoryCount}`);
  }
  return placed;
};
