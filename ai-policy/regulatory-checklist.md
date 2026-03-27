# Regulatory Checklist for AI-Assisted Development

> **WARNING: This checklist flags areas where AI tool adoption intersects with regulatory requirements. It is NOT a compliance audit. Each checked item requires review by your legal, compliance, or security team before you finalize your AI policy.**
>
> Complete this checklist before adopting the [AI Policy Template](ai-policy-template.md).

---

## How to Use This Checklist

For each section: read the question, check the box if it applies to your organization, and follow the guidance. If you check a box, that section of your AI policy likely needs modification — do not adopt the default policy language without legal review of that area.

---

## HIPAA — Health Insurance Portability and Accountability Act

- [ ] **Does your team handle protected health information (PHI)?**

If yes:

- AI tools that process code containing PHI (variable names, test fixtures, database schemas with patient data) may constitute a PHI disclosure to the AI provider.
- Verify that your AI tool provider will sign a **Business Associate Agreement (BAA)**. Most standard-tier AI tools do not offer BAAs — you may need an enterprise or self-hosted tier.
- Audit your test data: if test fixtures, seed data, or configuration files contain real or realistic PHI, AI tools will ingest them. Synthetic test data eliminates this risk.
- Add to your AI policy: "Teams handling PHI must use AI tools covered by a signed BAA. Code containing PHI identifiers, schemas, or test data must not be sent to AI providers without BAA coverage."

---

## SOC 2 — Service Organization Control 2

- [ ] **Is your organization SOC 2 certified (Type I or Type II)?**

If yes:

- SOC 2 requires audit trails for changes to systems in scope. AI-generated code must be traceable — who prompted it, who reviewed it, when it was merged.
- Verify that your AI tool provides **audit logs** of prompts and completions, or that your workflow produces equivalent traceability (e.g., PR descriptions that note AI assistance).
- Background/autonomous agents that generate PRs require the same change management controls as human-initiated changes. If your SOC 2 controls require approval workflows, AI-generated PRs must go through them.
- Add to your AI policy: "All AI-generated changes to SOC 2 in-scope systems must be traceable through standard change management workflows. AI tool audit logs must be retained per our SOC 2 retention policy."

---

## FedRAMP — Federal Risk and Authorization Management Program

- [ ] **Does your organization hold FedRAMP authorization or serve government contracts with FedRAMP requirements?**

If yes:

- FedRAMP imposes strict **data residency** requirements. Code sent to AI providers hosted outside approved boundaries may violate your authorization.
- Verify that your AI tool provider operates within your required FedRAMP boundary (e.g., AWS GovCloud, Azure Government). Most commercial AI coding tools do **not** currently have FedRAMP authorization.
- Self-hosted or on-premise AI models may be required for FedRAMP-scoped work.
- Add to your AI policy: "Code for FedRAMP-scoped systems must only be processed by AI tools operating within the authorized FedRAMP boundary. Commercial AI coding tools are prohibited for FedRAMP-scoped work unless the provider holds appropriate authorization."

---

## GDPR — General Data Protection Regulation

- [ ] **Does your team process personal data of EU/EEA residents?**

If yes:

- Sending code that contains personal data (or schemas/models that describe personal data structures) to an AI provider constitutes **data processing** under GDPR.
- Verify that your AI tool provider has a **Data Processing Agreement (DPA)** and that data transfers comply with GDPR transfer mechanisms (e.g., Standard Contractual Clauses, adequacy decisions).
- GDPR's right to erasure may apply to AI training data. Confirm that your provider's terms include a **no-training clause** — otherwise personal data in your code could become part of a model's weights, making erasure impossible.
- Add to your AI policy: "Teams processing EU personal data must verify AI tool providers have signed DPAs with GDPR-compliant transfer mechanisms. AI tools must operate under no-training agreements to preserve data subject rights."

---

## PCI DSS — Payment Card Industry Data Security Standard

- [ ] **Does your team handle payment card data or operate in a PCI DSS-scoped environment?**

If yes:

- PCI DSS restricts how cardholder data environments (CDEs) are accessed and modified. AI tools that have access to CDE code, configurations, or credentials must be treated as in-scope components.
- Verify that AI tool access to CDE code is logged and auditable, consistent with **PCI DSS Requirement 10** (track and monitor all access).
- AI tools must not have access to production cardholder data, encryption keys, or payment processing credentials — even indirectly through code context.
- Network segmentation requirements apply: AI tool traffic from CDE-scoped systems must comply with your segmentation controls.
- Add to your AI policy: "AI tools used on PCI DSS-scoped codebases must be included in the CDE scope assessment. Access must be logged per Requirement 10. AI tools must not process or have access to cardholder data, keys, or payment credentials."

---

## Industry-Specific Considerations

### Financial Services (SEC, FINRA, OCC)

- [ ] **Is your organization a regulated financial institution?**

If yes:
- Model risk management guidance (SR 11-7, OCC 2011-12) may apply to AI tools that generate code for risk calculations, trading systems, or regulatory reporting.
- Third-party risk management requirements apply to AI tool providers. They must be included in your vendor risk assessment process.
- Add to your AI policy: "AI-generated code for regulated financial systems (risk models, trading, reporting) requires review against model risk management guidelines."

### Healthcare (beyond HIPAA)

- [ ] **Does your software qualify as a medical device or support clinical decision-making?**

If yes:
- FDA guidance on AI/ML in medical devices applies. AI-generated code in device software requires the same design controls, verification, and validation as human-written code.
- Design history files must document AI involvement in code generation.
- Add to your AI policy: "AI-generated code in medical device software must be documented in the design history file and subject to full design control verification."

### Defense and Intelligence (ITAR, CMMC)

- [ ] **Does your team work with ITAR-controlled technical data or require CMMC certification?**

If yes:
- ITAR-controlled technical data **must not** be sent to AI providers unless the provider is ITAR-registered and the transfer is authorized.
- CMMC requirements for controlled unclassified information (CUI) apply to AI tool data flows. Commercial AI tools are almost certainly out of scope.
- Add to your AI policy: "AI tools are prohibited for ITAR-controlled or CUI-designated codebases unless the provider meets ITAR/CMMC requirements. No exceptions."

---

## Summary

| Framework | Key Question | Primary Risk |
|---|---|---|
| HIPAA | Does code contain or reference PHI? | Unauthorized PHI disclosure to AI provider |
| SOC 2 | Are AI changes auditable? | Gaps in change management audit trail |
| FedRAMP | Is the AI tool in the authorized boundary? | Data residency violation |
| GDPR | Does code contain EU personal data? | Unlawful data processing/transfer |
| PCI DSS | Does AI touch cardholder data environment? | Expanded CDE scope, access logging gaps |
| Financial | Does AI generate regulated system code? | Model risk / vendor risk non-compliance |
| Healthcare | Is the software a medical device? | Design control documentation gaps |
| Defense | Does code contain controlled technical data? | ITAR/CUI unauthorized disclosure |

**If you checked any box above, do not adopt the AI policy template without legal review of the flagged sections.**
