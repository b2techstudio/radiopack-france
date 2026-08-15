import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export type ChannelMemory = {
  location: number;
  name: string;
  frequency: string;
  mode: string;
  step: string;
  comment: string;
};

export type ChannelGroup = {
  id: string;
  label: string;
  description: string;
  memories: ChannelMemory[];
};

const parseCsvRow = (row: string): string[] => {
  const cells: string[] = [];
  let current = "";
  let quoted = false;

  for (let index = 0; index < row.length; index += 1) {
    const character = row[index];

    if (character === '"') {
      if (quoted && row[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (character === "," && !quoted) {
      cells.push(current);
      current = "";
    } else {
      current += character;
    }
  }

  cells.push(current);
  return cells;
};

export const loadPublicPackMemories = (relativePublicPath: string): ChannelMemory[] => {
  const csvPath = resolve(process.cwd(), "public", relativePublicPath);
  const csv = readFileSync(csvPath, "utf8").replace(/\r/g, "").trim();
  const [headerRow, ...rows] = csv.split("\n");
  const headers = parseCsvRow(headerRow);
  const indexOf = (name: string) => headers.indexOf(name);

  const locationIndex = indexOf("Location");
  const nameIndex = indexOf("Name");
  const frequencyIndex = indexOf("Frequency");
  const modeIndex = indexOf("Mode");
  const stepIndex = indexOf("TStep");
  const commentIndex = indexOf("Comment");

  if ([locationIndex, nameIndex, frequencyIndex, modeIndex, stepIndex, commentIndex].some((index) => index < 0)) {
    throw new Error(`CSV public incomplet: ${relativePublicPath}`);
  }

  return rows
    .filter(Boolean)
    .map((row) => parseCsvRow(row))
    .map((cells) => ({
      location: Number(cells[locationIndex]),
      name: cells[nameIndex],
      frequency: cells[frequencyIndex],
      mode: cells[modeIndex],
      step: cells[stepIndex],
      comment: cells[commentIndex],
    }));
};

const matchesSpaceOrCall = (memory: ChannelMemory) => /^(APRS|ISS|SAT|CALL)/.test(memory.name);
const matchesPmr = (memory: ChannelMemory) => /^PMR\d{2}$/.test(memory.name);
const matchesMarine = (memory: ChannelMemory) => memory.comment.toLowerCase().includes("vhf marine");
const matchesAviation = (memory: ChannelMemory) => memory.mode === "AM";

const takeGroup = (
  remaining: Set<ChannelMemory>,
  id: string,
  label: string,
  description: string,
  predicate: (memory: ChannelMemory) => boolean,
): ChannelGroup => {
  const memories = [...remaining].filter(predicate);
  memories.forEach((memory) => remaining.delete(memory));
  return { id, label, description, memories };
};

const withoutEmptyGroups = (groups: ChannelGroup[]) => groups.filter((group) => group.memories.length > 0);

export const buildStandardChannelGroups = (memories: ChannelMemory[]): ChannelGroup[] => {
  const remaining = new Set(memories);
  const groups = [
    takeGroup(remaining, "pmr446", "PMR446", "Les 16 canaux PMR446 présents dans le pack public.", matchesPmr),
    takeGroup(remaining, "marine", "VHF marine", "Canaux maritimes en réception seule, avec les côtés navire et côte lorsqu'ils sont distincts.", matchesMarine),
    takeGroup(remaining, "space", "APRS / espace / appels", "APRS, ISS, satellites FM et fréquences d'appel conservées dans le pack.", matchesSpaceOrCall),
    takeGroup(remaining, "aviation", "Aviation", "Mémoires aviation AM publiées dans le CSV régional courant.", matchesAviation),
  ];

  if (remaining.size > 0) {
    groups.push({
      id: "regional",
      label: "Radioamateur / régional",
      description: "Relais, transpondeurs et autres mémoires régionales publiques restantes.",
      memories: [...remaining],
    });
  }

  return withoutEmptyGroups(groups);
};

export const buildBretagneChannelGroups = (memories: ChannelMemory[]): ChannelGroup[] => {
  const remaining = new Set(memories);
  const groups = [
    takeGroup(remaining, "rennes", "Rennes", "Rennes information, approche, sol, tour et ATIS.", (memory) => memory.name.startsWith("RNS-")),
    takeGroup(remaining, "brest", "Brest", "Iroise information, approche, tour et ATIS pour Brest Bretagne.", (memory) => memory.name.startsWith("BES-")),
    takeGroup(remaining, "dinard", "Dinard", "Tour/A-A et ATIS de Dinard.", (memory) => memory.name.startsWith("DIN-")),
    takeGroup(remaining, "quimper", "Quimper", "Tour/A-A de Quimper.", (memory) => memory.name.startsWith("QUIM-")),
    takeGroup(remaining, "air-emerg", "Urgence aviation", "Fréquence internationale d'urgence aviation présente dans le pack.", (memory) => memory.name === "AIR-EMERG"),
    takeGroup(remaining, "pmr446", "PMR446", "Les 16 canaux PMR446 présents dans le pack public.", matchesPmr),
    takeGroup(remaining, "marine", "VHF marine", "Canaux maritimes en réception seule, avec les côtés navire et côte lorsqu'ils sont distincts.", matchesMarine),
    takeGroup(remaining, "space", "APRS / espace / appels", "APRS, ISS, satellites FM et fréquences d'appel conservées dans le pack.", matchesSpaceOrCall),
  ];

  if (remaining.size > 0) {
    groups.push({
      id: "regional",
      label: "Radioamateur / régional",
      description: "Relais, transpondeurs et autres mémoires régionales publiques restantes.",
      memories: [...remaining],
    });
  }

  return withoutEmptyGroups(groups);
};
