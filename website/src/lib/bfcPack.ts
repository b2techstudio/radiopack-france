import { buildMetropolitanPack } from "./metropolitanPack";
import type { Channel, PlacedChannel } from "./chirpPack";

export const bfcV03Version = "v0.3";
export const bfcV03MemoryCount = 54;
export const bfcV03Filename = "radiopack-france-bourgogne-franche-comte-v0.3.csv";

export const bfcV03ExtraChannels: Channel[] = [
  {
    name: "F5ZIQ-V",
    frequency_mhz: 145.45,
    mode: "FM",
    step_khz: 12.5,
    comment: "Besancon F5ZIQ crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZIQ-U",
    frequency_mhz: 432.55,
    mode: "FM",
    step_khz: 12.5,
    comment: "Besancon F5ZIQ crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZVA-V",
    frequency_mhz: 145.25,
    mode: "FM",
    step_khz: 12.5,
    comment: "Chateau-Chinon F5ZVA crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZVA-U",
    frequency_mhz: 431.25,
    mode: "FM",
    step_khz: 12.5,
    comment: "Chateau-Chinon F5ZVA crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZFQ-V",
    frequency_mhz: 145.2625,
    mode: "FM",
    step_khz: 12.5,
    comment: "Ballon Alsace F5ZFQ crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZFQ-U",
    frequency_mhz: 430.125,
    mode: "FM",
    step_khz: 12.5,
    comment: "Ballon Alsace F5ZFQ crossband RX, validation 2026-08-19",
  },
  {
    name: "F1ZCA-A",
    frequency_mhz: 430.3,
    mode: "FM",
    step_khz: 12.5,
    comment: "Mont Poupet F1ZCA RU12 paired RX, validation 2026-08-19",
  },
  {
    name: "F1ZCA-B",
    frequency_mhz: 431.9,
    mode: "FM",
    step_khz: 12.5,
    comment: "Mont Poupet F1ZCA RU12 paired RX, validation 2026-08-19",
  },
  {
    name: "F5ZXZ-V",
    frequency_mhz: 145.2125,
    mode: "FM",
    step_khz: 12.5,
    comment: "Cosne-sur-Loire F5ZXZ crossband RX, validation 2026-08-19",
  },
  {
    name: "F5ZXZ-U",
    frequency_mhz: 431.1,
    mode: "FM",
    step_khz: 12.5,
    comment: "Cosne-sur-Loire F5ZXZ crossband RX, validation 2026-08-19",
  },
  {
    name: "VEZE-AFIS",
    frequency_mhz: 122.205,
    mode: "AM",
    step_khz: 8.33,
    comment: "Besancon La Veze LFQM AFIS/A-A RX, AIRAC 08/26 review",
  },
  {
    name: "SY-APP1",
    frequency_mhz: 119.505,
    mode: "AM",
    step_khz: 8.33,
    comment: "Saint-Yan LFLN APP auxiliary RX, SIA AIP review",
  },
  {
    name: "SY-APP2",
    frequency_mhz: 123.405,
    mode: "AM",
    step_khz: 8.33,
    comment: "Saint-Yan LFLN APP RX, SIA AIP review",
  },
  {
    name: "SY-GND",
    frequency_mhz: 121.805,
    mode: "AM",
    step_khz: 8.33,
    comment: "Saint-Yan LFLN Ground RX, SIA AIP review",
  },
  {
    name: "SY-TWR",
    frequency_mhz: 122.3,
    mode: "AM",
    step_khz: 8.33,
    comment: "Saint-Yan LFLN Tower RX, SIA AIP review",
  },
  {
    name: "SY-ATIS",
    frequency_mhz: 132.48,
    mode: "AM",
    step_khz: 8.33,
    comment: "Saint-Yan LFLN ATIS RX, SIA AIP review",
  },
  {
    name: "CHAL-INFO",
    frequency_mhz: 118.605,
    mode: "AM",
    step_khz: 8.33,
    comment: "Chalon Champforgeuil LFLH AFIS/A-A RX, SIA AIP review",
  },
];

export const buildBfcV03Pack = (): PlacedChannel[] => {
  const base = buildMetropolitanPack("bourgogne-franche-comte", "v0.2");
  const additions = bfcV03ExtraChannels.map((channel, index) => ({
    location: 80 + index,
    block: channel.mode === "AM" ? "AVIATION_V03" : "RADIOAMATEUR_V03",
    channel,
  }));
  const placed = [...base, ...additions].sort((a, b) => a.location - b.location);
  if (placed.length !== bfcV03MemoryCount) {
    throw new Error(`BFC ${bfcV03Version}: ${placed.length} memories, expected ${bfcV03MemoryCount}`);
  }
  return placed;
};
