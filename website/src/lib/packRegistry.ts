export type PublicPackVariant = {
  id: string;
  label: string;
  memoryCount: number;
  filename: string;
  downloadUrl: string;
  aviationIncluded?: boolean;
};

export type PublicPack = {
  id: string;
  regionSlug: string;
  name: string;
  version: string;
  status: string;
  description: string;
  defaultVariant: string;
  aviationToggle?: {
    includedVariant: string;
    excludedVariant: string;
    memoryCount: number;
  };
  notamCheck: boolean;
  variants: PublicPackVariant[];
};

const legacyPublicPacks: PublicPack[] = [
  {
    id: "annecy-alpes-leman",
    regionSlug: "annecy-haute-savoie",
    name: "Annecy–Alpes–Léman",
    version: "v0.4",
    status: "Disponible",
    description: "Pack Alpes du Nord / bassin lémanique v0.4 avec 77 mémoires RX, dont F1ZTH 50 MHz, et variante sans aviation.",
    defaultVariant: "full",
    aviationToggle: {
      includedVariant: "full",
      excludedVariant: "no-aviation",
      memoryCount: 17,
    },
    notamCheck: true,
    variants: [
      {
        id: "full",
        label: "Version complète",
        memoryCount: 77,
        filename: "radiopack-france-annecy-alpes-leman-v0.4.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv",
        aviationIncluded: true,
      },
      {
        id: "no-aviation",
        label: "Sans aviation",
        memoryCount: 60,
        filename: "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv",
        aviationIncluded: false,
      },
    ],
  },
  {
    id: "bretagne",
    regionSlug: "bretagne",
    name: "Bretagne",
    version: "v0.2",
    status: "Disponible",
    description: "Pack régional Bretagne v0.2 de 151 mémoires RX, dont 16 mémoires aviation AIRAC 08/26.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 151,
        filename: "radiopack-france-bretagne-v0.2.csv",
        downloadUrl: "/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
        aviationIncluded: true,
      },
    ],
  },
  {
    id: "normandie",
    regionSlug: "normandie",
    name: "Normandie",
    version: "v0.4",
    status: "Disponible",
    description: "Pack régional Normandie v0.4 de 142 mémoires RX, publié en réception seule.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 142,
        filename: "radiopack-france-normandie-v0.4.csv",
        downloadUrl: "/downloads/normandie/radiopack-france-normandie-v0.4.csv",
      },
    ],
  },
];

const metropolitanMetadata = [
  { id: "hauts-de-france", name: "Hauts-de-France", memoryCount: 36 },
  { id: "ile-de-france", name: "Île-de-France", memoryCount: 34 },
  { id: "grand-est", name: "Grand Est", memoryCount: 36 },
  { id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 32 },
  { id: "pays-de-la-loire", name: "Pays de la Loire", memoryCount: 30 },
  { id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 30 },
  { id: "nouvelle-aquitaine", name: "Nouvelle-Aquitaine", memoryCount: 42 },
  { id: "auvergne-rhone-alpes", name: "Auvergne-Rhône-Alpes", memoryCount: 38 },
  { id: "occitanie", name: "Occitanie", memoryCount: 44 },
  { id: "provence-alpes-cote-d-azur", name: "Provence-Alpes-Côte d’Azur", memoryCount: 42 },
  { id: "corse", name: "Corse", memoryCount: 28 },
] as const;

const metropolitanPublicPacks: PublicPack[] = metropolitanMetadata.map((item) => {
  const filename = `radiopack-france-${item.id}-v0.1.csv`;
  return {
    id: item.id,
    regionSlug: item.id,
    name: item.name,
    version: "v0.1",
    status: "Disponible",
    description: `Socle régional v0.1 de ${item.memoryCount} mémoires RX : PMR446, appels, APRS/ISS et sélection FM 2 m paired RX. Périmètre volontairement non exhaustif, sans aviation.`,
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack v0.1",
        memoryCount: item.memoryCount,
        filename,
        downloadUrl: `/downloads/${item.id}/${filename}`,
        aviationIncluded: false,
      },
    ],
  };
});

export const publicPacks: PublicPack[] = [
  legacyPublicPacks[0],
  legacyPublicPacks[2],
  legacyPublicPacks[1],
  ...metropolitanPublicPacks,
];

export const defaultPublicPackId = "annecy-alpes-leman";

export const getPublicPack = (packId: string) =>
  publicPacks.find((pack) => pack.id === packId);

export const getPublicVariant = (pack: PublicPack, variantId: string) =>
  pack.variants.find((variant) => variant.id === variantId);
