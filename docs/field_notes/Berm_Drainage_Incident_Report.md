# Incident Report: The Berm-Drainage Over-Engineering Incident

* **Author:** Justin D. Grimm ([ORCID: 0009-0000-5299-0243](https://orcid.org/0009-0000-5299-0243))
* **Workspace Source:** [Berm-Drainage Incident Report](https://docs.google.com/document/d/1sTt6NTZVjFguzgPrwpvr44dGnDfbY9PbLw1cWf-BtW0/edit?usp=drivesdk&ouid=108041868247398199219)

## Post-Mortem & First-Principles Resolution

* **The Failure Mode:** An ESP32/Arduino moisture-sensor relay array in a weatherized ammo can driving a salvaged 12V bilge pump clogged on red Alabama clay and decaying mulch within 4 seconds during a 2:00 AM downpour, locking the relay open until thermal failure while water carved a trench across the patio.
* **The Kelvin Error & Final Fix:** Assuming complex software logic can override mud, debris, and fluid dynamics. Stripped out the microcontrollers and relays entirely and installed a passive gravity-drop rock bed. Namaste.
