# Sprint 66 — Technical inventory boundaries

Date: **2026-08-11**  
Logical state: **0.21.55**

## Goal

Push the remaining source-only blockers toward named technical inventories without converting infrastructure, maintenance scope, association identity, historical architecture, or undated secondary schedules into publication evidence.

## Normandie v0.4

### F5ZHA Laval

- The current REF directory still shows F5ZHA active on the paired RX frequencies **145.4675 / 432.575 MHz**.
- The Radio-Club des Fourches / ARAM53 can be independently identified as an active association in 2026, but no current technical publication from that association was found that validates the repeater pair.
- The existence of the association is **not** frequency validation.
- The authoritative/local reconciliation gate and the Mortain field gate therefore remain closed.

### F6ZES Sourdeval

- The current REF entry still identifies F6ZES, F1SMB, locator `IN98MR93XV` and 230 m.
- Frequency, mode and operational state remain absent.
- No second current frequency/mode source was found.
- Candidate delta remains **0** and no frequency is guessed.

## CROSS Étel — Channel 64

A current DIRM NAMO recruitment notice (`2026-2341297`) confirms that the CROSS Étel technical service maintains **17 radio stations** along the coast from Penmarc'h to Biarritz and explicitly places MHF/VHF radiocommunication in the maintenance context.

This is useful current primary technical evidence, but it still gives **no station-name inventory and no channel mapping**. It therefore cannot identify a Morbihan Ch64 transmitter. The existing conflict remains: the Ministry regional statement retains Ch63/64 while current local operational material converges on Ch63.

## CROSS Corsen — Channel 79

- A current 2026 public-service job notice again confirms radio-communications equipment at the **Stiff / Ouessant**.
- The PLACE procurement `DGAMPA-SNC1-2025-03_STIFF`, with a January 2026 deadline, confirms the continuing current renovation project at the Stiff. It does not map Channel 79.
- A secondary undated VHF schedule exposes the complete familiar Ch79 chain **Cap Fréhel / Bodic / Batz / Stiff / Pointe du Raz**. This is a useful search target, not current primary validation.
- The local Erquy source continues to provide the stronger secondary clue for **Cap Fréhel / Bodic**.
- The historical Légifrance architecture remains historical only.

No current primary source exploited in this sprint maps Ch79 to one or more of those sites.

## Météo-France Guide Marine 2026

The official landing page remains dated 2026-08-05 and states that the Guide Marine contains radio frequencies and VHF schedules. The direct 2026 PDF was retried again and still returned a `cache miss`; no PDF content or screenshot became available, so it produces **zero inference**.

## Memory contract

Nothing changes in the paired-RX rule:

- R3 / F1ZBX: **145.075 + 145.675 MHz**, 2 RX memories if the field gate clears, independently of the 2 required sessions.
- Étel Ch64: **156.225 + 160.825 MHz**, 2 RX memories if publishable.
- Corsen Ch79: **156.975 + 161.575 MHz**, 2 RX memories if publishable.

## Result

- Normandie internal candidate: **142** memories.
- Known guarded ceiling: **147**.
- Review: **3/9**.
- Open blockers: **6**.
- Eligible additions: **0**.
- Public Normandie v0.3.1: **139**, unchanged.
- Public Annecy–Alpes–Léman v0.2: **65/48**, unchanged.
- Bretagne: research only.

## New guard

`tests/test_sprint66_technical_inventory_boundaries.py` prevents future code or documentation from treating:

- a maintenance scope as a named station/channel inventory;
- association existence as repeater-frequency validation;
- an undated secondary schedule as current primary validation;
- a current infrastructure/procurement confirmation as a channel assignment.
