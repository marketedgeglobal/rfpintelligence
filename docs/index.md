---
title: RFP Intelligence Analysis
updated: 2026-02-18 22:10:11 UTC
---

<style>
	@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

	:root {
		--meg-white: #ffffff;
		--meg-charcoal: #1a1a1a;
		--meg-teal: #00a3da;
		--meg-teal-dark: #0085b2;
		--meg-gray-bg: #f4f4f4;
		--meg-gray-text: #555555;
		--meg-border: #e5e7eb;
		--meg-shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.05);
		--meg-shadow-md: 0 8px 24px rgba(0, 0, 0, 0.08);
	}

	/* ── Base ── */
	body,
	.markdown-body {
		background: var(--meg-white) !important;
		color: var(--meg-charcoal) !important;
		font-family: 'Montserrat', Arial, sans-serif !important;
		font-size: 15.5px;
		line-height: 1.6;
	}

	.markdown-body {
		max-width: 960px;
		margin: 0 auto;
		padding: 0 2.5rem 6rem;
		background: var(--meg-white);
		border: none;
		border-radius: 0;
		box-shadow: none;
	}

	/* ── Typography ── */
	.markdown-body h1,
	.markdown-body h2,
	.markdown-body h3,
	.markdown-body h4 {
		font-family: 'Montserrat', Arial, sans-serif !important;
		font-weight: 800;
		color: var(--meg-charcoal);
		letter-spacing: -0.01em;
		line-height: 1.2;
	}

	.markdown-body h1 {
		font-size: 3rem;
		margin-top: 2.5rem;
		margin-bottom: 0.75rem;
	}

	.markdown-body h2 {
		font-size: 1.75rem;
		font-weight: 700;
		margin-top: 5rem;
		margin-bottom: 1.5rem;
		padding-bottom: 0.5rem;
		border-bottom: 2px solid var(--meg-teal);
		color: var(--meg-charcoal);
	}

	.markdown-body h3 {
		font-size: 1.1rem;
		font-weight: 700;
		margin-top: 0;
		color: var(--meg-charcoal);
	}

	.markdown-body p,
	.markdown-body li {
		color: #444444;
	}

	.markdown-body ul,
	.markdown-body ol {
		padding-left: 1.4rem;
	}

	.markdown-body strong {
		color: var(--meg-charcoal);
		font-weight: 700;
	}

	/* ── Links ── */
	.markdown-body a {
		color: var(--meg-teal);
		text-decoration: none;
		font-weight: 600;
	}

	.markdown-body a:hover {
		color: var(--meg-teal-dark);
		text-decoration: underline;
	}

	/* ── Opportunity cards ── */
	.markdown-body h3 {
		background: var(--meg-white);
		border: 1px solid var(--meg-border);
		border-bottom: none;
		border-radius: 12px 12px 0 0;
		box-shadow: var(--meg-shadow-sm);
		padding: 1rem 1.4rem 0.5rem;
		margin-bottom: 0;
	}

	.markdown-body h3 + ul {
		background: var(--meg-gray-bg);
		border: 1px solid var(--meg-border);
		border-top: none;
		border-radius: 0 0 12px 12px;
		box-shadow: var(--meg-shadow-sm);
		padding: 1rem 1.5rem 1.25rem;
		list-style: none;
		margin: 0 0 2rem;
	}

	.markdown-body h3 + ul li {
		color: #444444;
		padding: 0.2rem 0;
		font-size: 0.9rem;
	}

	/* ── Metric / summary list rows ── */
	.markdown-body h2 + ul,
	.markdown-body h2 + p + ul {
		background: var(--meg-gray-bg);
		border: 1px solid var(--meg-border);
		border-radius: 10px;
		padding: 1rem 1.5rem;
		list-style: none;
		margin-bottom: 0.5rem;
		box-shadow: var(--meg-shadow-sm);
	}

	.markdown-body h2 + ul li,
	.markdown-body h2 + p + ul li {
		padding: 0.25rem 0;
		border-bottom: 1px solid var(--meg-border);
		font-size: 0.9rem;
		color: #444444;
	}

	.markdown-body h2 + ul li:last-child,
	.markdown-body h2 + p + ul li:last-child {
		border-bottom: none;
	}

	/* ── Timestamp ── */
	.markdown-body em:first-of-type {
		display: inline-block;
		margin: 1rem 0 0.25rem;
		font-size: 0.82rem;
		color: #888888;
		font-weight: 500;
		font-style: normal;
	}

	/* ── Sticky Navigation ── */
	nav[aria-label='MarketEdge Global'] {
		position: sticky;
		top: 0;
		z-index: 200;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.15rem;
		margin: 0 -2.5rem 1rem;
		padding: 0.8rem 2.5rem;
		background: var(--meg-white);
		border-bottom: 1px solid var(--meg-border);
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
	}

	nav[aria-label='MarketEdge Global'] a {
		color: var(--meg-charcoal) !important;
		font-family: 'Montserrat', Arial, sans-serif;
		font-size: 0.75rem;
		font-weight: 600;
		padding: 0.4rem 0.8rem;
		border-radius: 4px;
		background: transparent;
		border: none;
		text-transform: uppercase;
		letter-spacing: 0.07em;
		text-decoration: none;
		transition: color 0.15s, background 0.15s;
	}

	nav[aria-label='MarketEdge Global'] a:hover {
		color: var(--meg-teal) !important;
		background: rgba(0, 163, 218, 0.08);
		text-decoration: none;
	}

	nav[aria-label='MarketEdge Global'] a:focus-visible {
		outline: 2px solid var(--meg-teal);
		outline-offset: 2px;
	}

	nav[aria-label='MarketEdge Global'] a.nav-cta {
		background: var(--meg-teal);
		color: #ffffff !important;
		border-radius: 6px;
		margin-left: auto;
		padding: 0.42rem 1rem;
	}

	nav[aria-label='MarketEdge Global'] a.nav-cta:hover {
		background: var(--meg-teal-dark);
		color: #ffffff !important;
	}

	/* ── Responsive ── */
	@media (max-width: 768px) {
		.markdown-body {
			padding: 0 1.25rem 3rem;
		}

		.markdown-body h1 {
			font-size: 2.1rem;
		}

		.markdown-body h2 {
			font-size: 1.35rem;
			margin-top: 3rem;
		}

		nav[aria-label='MarketEdge Global'] {
			margin: 0 -1.25rem 1rem;
			padding: 0.65rem 1.25rem;
		}

		nav[aria-label='MarketEdge Global'] a {
			font-size: 0.7rem;
			padding: 0.35rem 0.6rem;
		}

		nav[aria-label='MarketEdge Global'] a.nav-cta {
			margin-left: 0;
		}
	}
</style>

*Last updated: 2026-02-18 22:10:11 UTC*

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


## Run Metadata

- **Output file:** `docs/index.md`
- **Metadata file:** `data/last_run.json`
- **Timezone:** UTC
