PYTHON ?= python3

.PHONY: all verify clean

all: verify

verify:
	$(PYTHON) scripts/check_speedo_penance.py --seed 42 --board CRIMSON_SPEEDO_BOARD.md --punchcard waystation_punchcard.json
	$(PYTHON) waveguides/dandelion_communicator_madras_v5_0_0.py --verify
	env -u BASH_ENV bash "$(CURDIR)/scripts/audit_wfx_loot.sh" "$(CURDIR)"

clean:
	@true
