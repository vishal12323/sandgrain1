# Track 1 — Lido × Aave Monitoring Layer

## Objective
Build a public, real-time monitoring layer that shows how Lido staking assets (stETH / wstETH) are distributed across Aave markets.

This is the first Sandgrain deliverable.

## Current State

### Infrastructure
- Python environment working
- Web3 connection via Alchemy working
- Ethereum mainnet access confirmed
- Contract reads functioning correctly

### Data Pipeline
- stETH total supply retrieved
- wstETH total supply retrieved
- Aave V2 aSTETH total supply retrieved
- Aave V3 aEthwstETH total supply retrieved
- Token metadata verified
- Snapshot exported to JSON

## Current Metrics
- stETH total supply: 9,216,702.09
- wstETH total supply: 3,397,769.82
- Aave V2 stETH exposure: 3,954.92
- Aave V2 share of total stETH: 0.0429%
- Aave V3 wstETH exposure: 1,346,110.36
- Aave V3 share of total wstETH: 39.6175%

## Interpretation
The original Aave V2 stETH metric is technically correct but not the main signal.

The dominant Track 1 metric is:
- Aave V3 wstETH exposure
- with Aave V2 stETH as secondary context

## Track 1 v1 Display Plan
The first public page displays:
- stETH total supply
- wstETH total supply
- Aave V2 stETH exposure
- Aave V2 % of stETH supply
- Aave V3 wstETH exposure
- Aave V3 % of wstETH supply
- last updated timestamp

## Strategic Positioning
Project name:
Sandgrain — Lido Exposure Monitor (Track 1)

Value:
- shows real-time concentration of Lido assets in Aave
- improves visibility into staking-asset usage in DeFi
- supports governance, risk awareness, and ecosystem transparency

## Immediate Next Milestone
- deploy the static dashboard
- publish the repo
- add historical snapshots next