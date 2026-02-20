---
title: RFP Intelligence Analysis
updated: 2026-02-18 22:10:11 UTC
---

<style>
	@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');

	:root {
		--meg-navy:    #242337; /* MEG hero / nav dark background        */
		--meg-olive:   #393d32; /* MEG primary text / dark body colour   */
		--meg-cream:   #f1e3c8; /* MEG warm text on dark backgrounds     */
		--meg-fill:    #f1f3ee; /* MEG light section fill                */
		--meg-white:   #ffffff;
		--meg-blue:    #0088cb; /* MEG colour_4 — primary link / button  */
		--meg-blue-lt: #7fccf7; /* MEG light-blue hover                  */
		--meg-border:  #e2e2e2;
		--meg-muted:   #8f8f8f;
		--meg-shadow:  0 4px 12px rgba(36, 35, 55, 0.12);
	}

	/* ── Base ── */
	html {
		background: var(--meg-navy);
	}

	body,
	.markdown-body {
		background: var(--meg-navy) !important;
		color: var(--meg-olive) !important;
		font-family: 'Lato', Arial, sans-serif !important;
		font-size: 15.5px;
		line-height: 1.6;
	}

	.markdown-body {
		max-width: 960px;
		margin: 0 auto;
		padding: 0 0 4rem;
		background: var(--meg-navy);
		border: none;
		border-radius: 0;
		box-shadow: none;
	}

	/* ── Content wrapper (light card on dark navy page) ── */
	.markdown-body > *:not(style):not(nav) {
		background: var(--meg-fill);
	}

	/* Hero / page-title band at the top of content */
	.markdown-body > em:first-of-type {
		display: block;
		background: var(--meg-navy);
		margin: 0;
		padding: 0.5rem 2.5rem 1rem;
		color: var(--meg-cream) !important;
		font-size: 0.8rem;
		font-weight: 300;
		font-style: normal;
		text-align: right;
		letter-spacing: 0.04em;
	}

	/* Main content wrapper – sits on the fill inside the navy page */
	.markdown-body > h2,
	.markdown-body > h3,
	.markdown-body > p,
	.markdown-body > ul,
	.markdown-body > ol {
		margin-left: 0;
		margin-right: 0;
	}

	/* Wrap all main body content after the nav in a light panel */
	.meg-content {
		background: var(--meg-fill);
		padding: 2.5rem 2.5rem 5rem;
	}

	/* ── Typography ── */
	.markdown-body h1,
	.markdown-body h2,
	.markdown-body h3,
	.markdown-body h4 {
		font-family: 'Lato', Arial, sans-serif !important;
		font-weight: 900;
		color: var(--meg-navy);
		letter-spacing: -0.01em;
		line-height: 1.2;
	}

	.markdown-body h1 {
		font-size: 2.8rem;
		margin-top: 0;
		margin-bottom: 0.75rem;
		color: var(--meg-cream);
		padding: 2.5rem 2.5rem 1.5rem;
		background: var(--meg-navy);
	}

	.markdown-body h2 {
		font-size: 1.55rem;
		font-weight: 700;
		margin-top: 0;
		margin-bottom: 1.25rem;
		padding: 2rem 2.5rem 0.6rem;
		border-bottom: 3px solid var(--meg-blue);
		color: var(--meg-navy);
		background: var(--meg-fill);
	}

	.markdown-body h3 {
		font-size: 1.05rem;
		font-weight: 700;
		margin-top: 0;
		color: var(--meg-navy);
	}

	.markdown-body p,
	.markdown-body li {
		color: var(--meg-olive);
	}

	.markdown-body ul,
	.markdown-body ol {
		padding-left: 1.4rem;
	}

	.markdown-body strong {
		color: var(--meg-navy);
		font-weight: 700;
	}

	/* ── Links ── */
	.markdown-body a {
		color: var(--meg-blue);
		text-decoration: none;
		font-weight: 700;
	}

	.markdown-body a:hover {
		color: var(--meg-blue-lt);
		text-decoration: underline;
	}

	/* ── Opportunity cards ── */
	.markdown-body h3 {
		background: var(--meg-navy);
		color: var(--meg-cream) !important;
		border: none;
		border-radius: 10px 10px 0 0;
		box-shadow: none;
		padding: 0.9rem 1.4rem 0.7rem;
		margin: 0 2.5rem 0;
	}

	.markdown-body h3 a {
		color: var(--meg-blue-lt) !important;
	}

	.markdown-body h3 a:hover {
		color: #ffffff !important;
	}

	.markdown-body h3 + ul {
		background: var(--meg-white);
		border: 1px solid var(--meg-border);
		border-top: none;
		border-radius: 0 0 10px 10px;
		box-shadow: var(--meg-shadow);
		padding: 0.9rem 1.5rem 1.1rem;
		list-style: none;
		margin: 0 2.5rem 2.5rem;
	}

	.markdown-body h3 + ul li {
		color: var(--meg-olive);
		padding: 0.22rem 0;
		font-size: 0.88rem;
		border-bottom: 1px solid var(--meg-border);
	}

	.markdown-body h3 + ul li:last-child {
		border-bottom: none;
	}

	/* ── Metric / summary list rows ── */
	.markdown-body h2 + ul,
	.markdown-body h2 + p + ul {
		background: var(--meg-white);
		border: 1px solid var(--meg-border);
		border-radius: 8px;
		padding: 0.75rem 2.5rem;
		list-style: none;
		margin: 0 0 0.5rem;
		box-shadow: var(--meg-shadow);
	}

	.markdown-body h2 + ul li,
	.markdown-body h2 + p + ul li {
		padding: 0.3rem 0;
		border-bottom: 1px solid var(--meg-border);
		font-size: 0.88rem;
		color: var(--meg-olive);
	}

	.markdown-body h2 + ul li:last-child,
	.markdown-body h2 + p + ul li:last-child {
		border-bottom: none;
	}

	/* ── Sticky Navigation — dark navy matching MEG header ── */
	nav[aria-label='MarketEdge Global'] {
		position: sticky;
		top: 0;
		z-index: 200;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.2rem;
		padding: 0.75rem 2.5rem;
		background: var(--meg-navy);
		border-bottom: 2px solid var(--meg-blue);
		box-shadow: 0 4px 16px rgba(36, 35, 55, 0.45);
	}

	nav[aria-label='MarketEdge Global'] a {
		color: var(--meg-cream) !important;
		font-family: 'Lato', Arial, sans-serif;
		font-size: 0.75rem;
		font-weight: 700;
		padding: 0.4rem 0.75rem;
		border-radius: 4px;
		background: transparent;
		border: none;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		text-decoration: none;
		transition: color 0.15s, background 0.15s;
	}

	nav[aria-label='MarketEdge Global'] a:hover {
		color: #ffffff !important;
		background: rgba(0, 136, 203, 0.25);
		text-decoration: none;
	}

	nav[aria-label='MarketEdge Global'] a:focus-visible {
		outline: 2px solid var(--meg-blue);
		outline-offset: 2px;
	}

	nav[aria-label='MarketEdge Global'] a.nav-cta {
		background: var(--meg-blue);
		color: #ffffff !important;
		border-radius: 4px;
		margin-left: auto;
		padding: 0.4rem 1.1rem;
	}

	nav[aria-label='MarketEdge Global'] a.nav-cta:hover {
		background: #006fa8;
		color: #ffffff !important;
	}

	/* ── Responsive ── */
	@media (max-width: 768px) {
		.markdown-body h1 {
			font-size: 2.1rem;
			padding: 2rem 1.25rem 1.25rem;
		}

		.markdown-body h2 {
			font-size: 1.25rem;
			padding: 1.5rem 1.25rem 0.5rem;
		}

		.markdown-body h3,
		.markdown-body h3 + ul {
			margin-left: 1.25rem;
			margin-right: 1.25rem;
		}

		.markdown-body h2 + ul,
		.markdown-body h2 + p + ul {
			padding-left: 1.25rem;
			padding-right: 1.25rem;
		}

		nav[aria-label='MarketEdge Global'] {
			padding: 0.6rem 1rem;
		}

		nav[aria-label='MarketEdge Global'] a {
			font-size: 0.68rem;
			padding: 0.35rem 0.55rem;
		}

		nav[aria-label='MarketEdge Global'] a.nav-cta {
			margin-left: 0;
		}
	}
</style>

<nav aria-label="MarketEdge Global">
	<a href="https://www.marketedgeglobal.com/">Home</a>
	<a href="https://www.marketedgeglobal.com/services-3">What We Offer</a>
	<a href="https://www.marketedgeglobal.com/sealeaders">Programs</a>
	<a href="https://www.marketedgeglobal.com/partnerai">PartnerAI</a>
	<a href="https://www.marketedgeglobal.com/partners">Our Work</a>
	<a href="https://www.marketedgeglobal.com/team">About Us</a>
	<a class="nav-cta" href="https://www.marketedgeglobal.com/contact-7">Contact</a>
</nav>

## Executive Summary

- **Total scanned:** 136
- **Qualifying opportunities:** 2
- **Priority split:** High 0, Medium 1, Low 1
- **Top sources:** United Nations Global Marketplace (2)

## Top Opportunities

### 1. [Supply and Delivery of Device Scene Incident Management (DSIM) Carry Packs for Islamabad, Pakistan](https://www.ungm.org/Public/Notice/291586)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-18
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Tender description: Supply and Delivery of Device Scene Incident Management (DSIM) Carry Packs for Islamabad, Pakistan UNOPS requirements are comprised of the following: Supply and Delivery of Device Scene Incident Management (DSIM) Carry Packs IMPORTANT NOTE: Interested vendors must respond to this tender using the UNOPS eSourcing system , via the UNGM portal. In order to access the full UNOPS tender details, request clarifications on the tender, and submit a vendor response to a tender using the system, vendors need to be registered as a UNOPS vendor at the UNGM portal and be logged into UNGM. For guidance on how to register on UNGM and submit responses to UNOPS tenders in the UNOPS eSourcing system, please refer to the user guide and other resources available at: https://esourcing.unops.org/#/Help/Guides

### 2. [Supply and delivery of materials for 10 workshops at Ninawa Agriculture School and Intisar Vocational School in Ninewa, Iraq.](https://www.ungm.org/Public/Notice/289708)
- **Score:** 0.260 (Low)
- **Published:** 2026-01-28
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP
- **Summary:** UNESCO Invitation to Bid (ITB) – Ref: IRQ/ITB/26/08 Date: 28 January 2026 Deadline for Submission: 27 February 2026, 18:00 Baghdad Time Submission Email: baghdad.proc@unesco.org Scope: Supply and delivery of materials for 10 workshops at Ninawa Agriculture School and Intisar Vocational School in Ninewa, Iraq.

## Pipeline Metrics

- **Fetched:** 136
- **After filtering:** 2
- **After deduplication:** 2
- **Selected top results:** 2
- **Dropped by age:** 52
- **Dropped by invalid date:** 0
- **Dropped by region:** 82
- **Region matched (annotated):** 2
- **Region unmatched (kept):** 82

## Scoring Summary

- **Entries scored:** 2
- **Average score:** 0.330
- **Highest score:** 0.400
- **Lowest score:** 0.260

## Priority Bands

- **High Priority (score ≥ 0.600):** Best-fit opportunities
- **Medium Priority (0.400–0.599):** Relevant but needs review
- **Low Priority (score < 0.400):** Monitor only
- **Current distribution:** High 0, Medium 1, Low 1

## Region Coverage

- **Matched region groups:** MENAP (2), SAR (1)

## Filtering Notes

- **Region handling:** Region criteria are used as a scoring signal.
- **Unmatched entries:** Items without region matches are retained and counted as Region unmatched (kept).

## Run Metadata

- **Output file:** `docs/index.md`
- **Metadata file:** `data/last_run.json`
- **Timezone:** UTC

*Last updated: 2026-02-18 22:10:11 UTC*
