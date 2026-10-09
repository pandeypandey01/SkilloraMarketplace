# Skillora Web Services — Tutorials 1 to 6

This package adapts the six uploaded Web Services assignments from the CampusEats wording to the user's Skillora project.

## Contents

- `tut1/` — HTTP by hand, Network analysis, project brief
- `tut2/` — service design, contracts, database schema
- `tut3/` — external SOAP partner, WSDL, SOAP request/response/fault
- `tut4/` — REST Orders service, OpenAPI, Flask implementation, tests
- `tut5/` — HTTP methods, headers, caching, ETags, retry safety
- `tut6/` — status codes, Problem Details, validation, curl verification

## Run the Orders service

From the directory containing `tut4`:

```bash
pip install flask pytest
python -m tut4.app
```

In another terminal:

```bash
pytest -q
```

## OpenAPI validation

Use Swagger Editor or:

```bash
pip install openapi-spec-validator
openapi-spec-validator tut4/openapi.yaml
```

## Important submission step
Team ID : 24

20251651069	Pranav Bhawsar	
20251651049	Jayesh Badole	
20251651082	Shivam Kumar	
20251651067	Pankaj Singh	
20251651068	Paras Pandey

with the real team information.

Also run the curl commands and replace command-only transcript sections with the exact outputs required by your instructor. The uploaded assignments explicitly require terminal captures for validation and HTTP behavior.
