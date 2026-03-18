# Sandgrain — Lido Exposure Monitor (Track 1)

## Overview

Sandgrain is a real-time monitoring layer that tracks how Lido staking assets are distributed across DeFi venues.

Track 1 focuses on Aave exposure.

## Current Scope

This version shows:

- stETH total supply
- wstETH total supply
- Aave V2 stETH exposure
- Aave V2 share of total stETH
- Aave V3 wstETH exposure
- Aave V3 share of total wstETH

## Core Insight

Aave V3 wstETH is the dominant Lido-on-Aave exposure metric, while Aave V2 stETH is comparatively minimal.

## Why This Matters

Lido is a major part of Ethereum’s staking infrastructure. As staking assets become embedded across DeFi, concentration inside specific lending markets can become a systemic risk factor.

This project is a first monitoring layer for that concentration.

## Architecture

- Python + web3.py for on-chain reads
- Alchemy for Ethereum mainnet RPC
- JSON snapshot export
- Static dashboard using HTML, CSS, and JavaScript

## Files

- `track1_aave_monitor.py` — pulls live on-chain data and exports snapshot JSON
- `track1_snapshot.json` — latest exported metric snapshot
- `dashboard/index.html` — dashboard UI
- `research_notes.md` — working notes and framing

## Next Steps

- add time-series history
- add charting
- add other venues such as Maker and Curve
- expand into a broader Lido concentration monitor