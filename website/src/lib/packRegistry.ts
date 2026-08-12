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

export const publicPacks: PublicPack[] = [
  {
    id: "annecy-alpes-leman",
    regionSlug: "annecy-haute-savoie",
    name: "Annecy–Alpes–Léman",
    version: "v0.2",
    status: "Disponible",
    description: "Pack Alpes du Nord / bassin lémanique avec variante optionnelle sans aviation.",
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
        memoryCount: 65,
        filename: "radiopack-france-annecy-alpes-leman-v0.2.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv",
        aviationIncluded: true,
      },
      {
        id: "no-aviation",
        label: "Sans aviation",
        memoryCount: 48,
        filename: "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv",
        aviationIncluded: false,
      },
    ],
  },
  {
    id: "bretagne",
    regionSlug: "bretagne",
    name: "Bretagne",
    version: "v0.1",
    status: "Disponible",
    description: "Pack régional Bretagne v0.1 de 135 mémoires RX, sans aviation dans ce périmètre initial.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 135,
        filename: "radiopack-france-bretagne-v0.1.csv",
        downloadUrl: "/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",
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

export const defaultPublicPackId = "annecy-alpes-leman";

export const getPublicPack = (packId: string) =>
  publicPacks.find((pack) => pack.id === packId);

export const getPublicVariant = (pack: PublicPack, variantId: string) =>
  pack.variants.find((variant) => variant.id === variantId);
