# Chapter 4: Sovereign LLM Gateway (`v1.10.0`) & 3D FCC Campfire Mesh

* **Canonical Workspace Sources:**
  - [Dandelion Hobo Network - Sovereign LLM Gateway Architecture v1.10.0](https://docs.google.com/document/d/1nBIWX8WMK8cFa9Zv6BzmuZAvYiZSzvms1ymZE9KvU4E/edit?usp=drivesdk&ouid=108041868247398199219)
  - [The Dandelion Network - Happy Hobo Field Manual & Mesh Telemetry v1.9.0](https://docs.google.com/document/d/1_ty7_tshobNCOxzoNjoItRadh6n_-D2ud0_DSduZZTM/edit?usp=drivesdk&ouid=108041868247398199219)

---

## Gateway Topology

```text
[ Hobo Mesh Nodes / ESP32-C5 + iCE40UP5K ESP-SDR ]
        |  (Bluetooth LE / 32-Byte DND3 Frame / Zero-Hardware Radio)
        v
[ Dandelion OS Gateway (Flight Deck v4.1.1) ]
  |-- Cost & Token Optimization Router (40-Trit Fowler Seed vs FP16)
  |-- Data Sovereignty & PII Stripper at Edge
  +-- Dynamic Multi-Provider Failover
        |-- Local Sovereign Foundry (profplum:30000 / Ollama / BitNet)
        +-- Frontier Cloud Endpoints (Fallback)
```

* **3D FCC Campfire Mesh Percolation:** In a 3D Face-Centered Cubic (`z = 12`) neighborhood topology, the bond percolation threshold is `p_c = 0.1202` (`12.02%`). Even under a `55%` node shock, Kintsugi Gold (`Byte 251`) lateral routing preserves `86.14%` giant-component survival.
