# International Standard Music Number claim audit

This offline static audit compares documented music-number capability claims with Python call patterns. It reads the root README and Markdown files under docs, excluding fenced code; inline code counts. It never executes source code or accesses the network.

Install and run:

```sh
ismn-validation-claim-audit audit .
python3 -m ismn_validation_claim_audit audit . --json
```

Use `--ignore PREFIX` repeatedly to omit paths, `--fail-on medium` to include test-only findings, and `--verbose` for additional context. The default threshold is high. Exit status is 0 for a pass, 2 for a finding at the threshold, and 1 for a usage or I/O error. Use `--version` for the version.

The finding identifiers are:

```
documented-ismn-validation-claim-false
documented-no-ismn-validation-claim-false
```

A positive claim without production evidence is high severity, or medium when evidence occurs only in tests. A denial with production evidence is high severity. A positive claim without any Python files is high severity; a denial without source passes.

The recognized library calls are:

```
from stdnum import ismn
ismn.validate(value)
ismn.is_valid(value)
ismn.ismn_type(value)
```

Generic named calls are also recognized when imported or used as attributes. Imports and aliases are resolved within one module; local definitions and rebinding can shadow imports. Test files count separately, while fixtures, examples, documentation, symlinks and invalid syntax do not provide production evidence.

## Differentiation

This audit does not cover generic input checking.

This audit does not cover ISBN book-number checks, which share the EAN algorithm but require a distinct prefix; the music-number route checks 9790.

This audit does not cover ISSN serial-number checks.

This audit does not cover IBAN bank account checks.

This audit does not cover UUID checks.

This audit does not cover semantic version checks.

This audit does not cover hardware address checks.

This audit does not cover BIC checks.

This audit does not cover cron schedule checks.

This audit does not cover describing a cron schedule.

This audit does not cover scheduled execution.

This audit does not cover calendar date checks.

This audit does not cover timeouts.

This audit does not cover card payment processing.

This audit does not cover card detail extraction.

This audit does not cover one-time-code and confirmation-link authentication.

This audit does not cover password verification.

This audit does not cover password hashing.

This audit does not cover password generation.

This audit does not cover PDF encryption.

This audit does not cover sending email.

This audit does not cover sending SMS.

This audit does not cover document extraction.

This audit does not cover barcode decoding.

This audit does not cover email address checks.

This audit does not cover phone number checks.

This audit does not cover password strength.

This audit does not cover JSON Schema checks.

This audit does not cover card number checks.

This audit does not cover domain checks.

This audit does not cover URL checks.

This audit does not cover IP address checks.

This audit does not cover JSON parsing.

This audit does not cover regular expression matching.

This audit does not cover URL parsing.

This audit does not cover web fetching.

This audit does not cover DNS resolution.

This audit does not cover barcode generation.

This audit does not cover account number extraction.

This audit does not cover vehicle number extraction.

This audit does not cover vehicle number decoding.

This audit does not cover vehicle history lookup.

This audit does not cover hexadecimal color checks.

This audit does not cover ORCID checks.

This audit does not cover ISNI checks.

This audit does not cover DOI checks and resolution.

This audit does not cover CUSIP checks.

This audit does not cover SEDOL checks.

This audit does not cover ISIN checks.

This audit does not cover security record lookup.

This audit does not cover securities identifier extraction.

This audit does not cover IMEI checks.

This audit does not cover MEID checks.

This audit does not cover Electronic Serial Number checks.

This audit does not cover ISAN audiovisual identifier checks.

This audit does not cover GRid release identifier checks.

This audit does not cover EAN checks, which lack a 9790 prefix leg and also accept ISBN-13.

This audit does not cover general serial-number checks.

This audit does not cover score registry lookup.

This audit does not cover music-number extraction from documents or photos.

This audit does not cover spreadsheet reading.
This audit does not cover spreadsheet generation.
This audit does not cover word document reading.
This audit does not cover word document generation.
This audit does not cover presentation reading.
This audit does not cover presentation generation.
This audit does not cover PDF extraction.
This audit does not cover PDF generation.
This audit does not cover PDF merging.
This audit does not cover PDF splitting.
This audit does not cover PDF rotation.
This audit does not cover PDF form filling.
This audit does not cover PDF watermarking.
This audit does not cover PDF redaction.
This audit does not cover PDF compression.
This audit does not cover PDF annotation.
This audit does not cover table extraction.
This audit does not cover OCR.
This audit does not cover e-signature.
This audit does not cover screen recording.
This audit does not cover video generation.
This audit does not cover QR code generation.
This audit does not cover barcode scanning.
This audit does not cover audio mixing.
This audit does not cover audio generation.
This audit does not cover audio editing.
This audit does not cover source separation.
This audit does not cover speech recognition.
This audit does not cover text to speech.
This audit does not cover noise suppression.
This audit does not cover music generation.
This audit does not cover music transcription.

## Limitations

```
validate ismn
```

The bare phrase above can describe a manual runbook step rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn validation
```

The bare phrase above can describe a roadmap feature rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn validator
```

The bare phrase above can describe a hosted page rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn check
```

The bare phrase above can describe a field-presence lint rule rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
check ismn
```

The bare phrase above can describe a manual runbook step rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
verify ismn
```

The bare phrase above can describe a visual edition confirmation rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn code validation
```

The bare phrase above can describe a field-presence check rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
valid ismn
```

The bare phrase above can describe an example value rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn is valid
```

The bare phrase above can describe example output rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn is invalid
```

The bare phrase above can describe example error text rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn validity
```

The bare phrase above can describe a configuration flag or column name rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn format validation
```

The bare phrase above can describe a format description rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
validate ismn number
```

The bare phrase above can describe a generic 13-digit shape check without the 9790 prefix rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn number validation
```

The bare phrase above can describe a specification section without code rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
validate ismn code
```

The bare phrase above can describe a manual runbook step rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
check ismn code
```

The bare phrase above can describe a manual runbook step rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
validate ismn10
```

The bare phrase above can describe a manual runbook step rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn13 validation
```

The bare phrase above can describe a specification section without code rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn number check
```

The bare phrase above can describe a cataloguing checklist item rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn validation
```

The bare phrase above can describe an external service result rather than an implemented capability, so it can produce a false positive requiring human judgment.

```
ismn
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
ismn number
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
validate identifier
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
check digit
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
luhn
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
publisher element
```

The bare phrase above is not recognized because it does not establish the specific capability.

```
item element
```

The bare phrase above is not recognized because it does not establish the specific capability.

A compact call only removes separators and changes case, so it is not evidence.

A format call only reformats the digits, so it is not evidence.

A to_ismn13 call converts the legacy 10-character form to the 13-digit form, so it is not evidence.

A split call separates components without checking the final digit, so it is not evidence.

A bare EAN check has no 9790 leg, so an ISBN-13 passes it too; the music-number route itself checks the 9790 prefix.

A Luhn call alone does not establish this capability.

The library accepts the legacy 10-character form and the 13-digit form as the same identifier, and to_ismn13 converts silently.

The library does not check whether the publisher element names a registered publisher.

ISBN checks are not evidence.

ISSN checks are not evidence.

ISAN checks are not evidence.

GRid checks are not evidence.

A registry lookup is not evidence.

A length check alone is not evidence.

A publisher-element membership check alone is not evidence.

A regular expression match alone is not evidence.

A generic validate method on an unknown base may be missed even if its object performs the desired operation.

A bare import is not evidence.

A roadmap, changelog or TODO in scanned prose still counts as a claim.

A denial outside the listed phrases may be missed.

A document outside the root README and docs directories is not scanned.

Evidence split across modules is missed.

A local definition shadows the corresponding route name.

Dead code counts as evidence.

A subprocess invocation is not evidence.

Alias chains that cannot be resolved are missed.

Matching is static and exact, not semantic.

A generic input check alone is not evidence of a music-number judgment.

An email check alone is not evidence of a music-number judgment.

A phone check alone is not evidence of a music-number judgment.

A URL check alone is not evidence of a music-number judgment.

An IP address check alone is not evidence of a music-number judgment.

A domain check alone is not evidence of a music-number judgment.

An ISBN check alone is not evidence of a music-number judgment.

An ISSN check alone is not evidence of a music-number judgment.

An IBAN check alone is not evidence of a music-number judgment.

An ISIN check alone is not evidence of a music-number judgment.

An IMEI check alone is not evidence of a music-number judgment.

An MEID check alone is not evidence of a music-number judgment.

An ISAN check alone is not evidence of a music-number judgment.

A GRid check alone is not evidence of a music-number judgment.

An EAN check alone is not evidence of a music-number judgment.

