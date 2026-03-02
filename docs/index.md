---
title: RFP Intelligence Analysis
updated: 2026-03-02 09:58:19 UTC
---

<style>
	@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');

	:root {
		--meg-navy:    #242337;
		--meg-olive:   #393d32;
		--meg-cream:   #f1e3c8;
		--meg-fill:    #f1f3ee;
		--meg-white:   #ffffff;
		--meg-blue:    #0088cb;
		--meg-blue-lt: #7fccf7;
		--meg-border:  #e2e2e2;
		--meg-muted:   #8f8f8f;
		--meg-shadow:  0 4px 12px rgba(36, 35, 55, 0.12);
	}

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

	.markdown-body a {
		color: var(--meg-blue);
		text-decoration: none;
		font-weight: 700;
	}

	.markdown-body a:hover {
		color: var(--meg-blue-lt);
		text-decoration: underline;
	}

	.markdown-body em:first-of-type {
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

*Last updated: 2026-03-02 09:58:19 UTC*

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
- **Qualifying opportunities:** 16
- **Priority split:** High 2, Medium 7, Low 7
- **Top sources:** ReliefWeb - Updates (7), UN News - Global perspective Human stories (5), United Nations Global Marketplace (2)

## Pipeline Metrics

- **Fetched:** 136
- **After filtering:** 16
- **After deduplication:** 16
- **Selected top results:** 16
- **Dropped by age:** 50
- **Dropped by invalid date:** 0
- **Dropped by region:** 70
- **Region matched (annotated):** 16
- **Region unmatched (kept):** 70

## Scoring Summary

- **Entries scored:** 16
- **Average score:** 0.441
- **Highest score:** 0.841
- **Lowest score:** 0.327

## Priority Bands

- **High Priority (score ≥ 0.600):** Best-fit opportunities
- **Medium Priority (0.400–0.599):** Relevant but needs review
- **Low Priority (score < 0.400):** Monitor only
- **Current distribution:** High 2, Medium 7, Low 7

## Region Coverage

- **Matched region groups:** EAP (3), LAC (2), MENAP (6), SAR (11)

## Filtering Notes

- **Region handling:** Region criteria are used as a scoring signal.
- **Unmatched entries:** Items without region matches are retained and counted as Region unmatched (kept).

## Top Opportunities

### 1. [Argentina: UNICEF Latin America and the Caribbean Region Humanitarian Situation Report No. 2 (End of Year), 31 December 2025](https://reliefweb.int/report/argentina/unicef-latin-america-and-caribbean-region-humanitarian-situation-report-no-2-end-year-31-december-2025)
- **Score:** 0.841 (High)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** $8,000,000
- **Matched Regions:** LAC
- **Summary:** Countries: Argentina, Barbados, Belize, Bolivia (Plurinational State of), Brazil, Chile, Cuba, Dominican Republic, Easter Island (Chile), El Salvador, Jamaica, Mexico, Nicaragua, Peru, Venezuela (Bolivarian Republic of) Source: UN Children's Fund Please refer to the attached file. Highlights Throughout 2025, Latin America and the Caribbean faced overlapping climate-related and public health humanitarian emergencies. Floods, hurricanes, droughts and wildfires across Central America and the Caribbean, the Amazon basin and the Southern Cone disrupted access to safe water, education, health care and protection services, disproportionately affecting children in vulnerable, remote and underserved communities. Humanitarian needs escalated in the final quarter of the year following Hurricane Melissa, a catastrophic Category 5 hurricane that made landfall in Jamaica, before sweeping across Cuba and the Dominican Republic in October. The hurricane affected more than 8 million people across the subregion, including nearly one million children. In response, UNICEF and its partners scaled up emergency preparedness, anticipatory action and response across the region, adapting service delivery in high-risk contexts and reinforcing systems for child protection, health, nutrition, education and WASH in close coordination with national authorities, civil society organizations and other United Nations agencies. At regional and national levels, UNICEF strengthened institutional readiness for future emergencies, including through early-warning systems, simulation exercises, shock-responsive social protection mechanisms, sector coordination platforms and capacity building for government counterparts and frontline responders. Following Hurricane Melissa, UNICEF revised the 2025 Humanitarian Action for Children (HAC) appeal in November, increasing the regional funding requirement from US$19 million to US$42 million. By the end of 2025, approximately US$11.7 million in new humanitarian funding had been mobilized. While this enabled critical response and preparedness efforts, the revised funding requirement was not fully met, underscoring the continued need for sustained humanitarian financing to maintain readiness and respond effectively to future shocks across the region. SITUATION OVERVIEW AND HUMANITARIAN NEEDS In 2025, countries across Latin America and the Caribbean experienced a succession of overlapping climate-related and public health humanitarian emergencies that placed sustained pressure on national systems and disproportionately affected children in vulnerable, remote and underserved communities. Across Central America and the Caribbean, the Amazon basin and Southern Cone, floods, hurricanes, prolonged droughts and wildfires disrupted access to safe water, education, health care and protection services, driving displacement and compounding existing socioeconomic and protection risks. Within this broader regional context, several countries experienced acute climate shocks. Severe flooding affected Argentina, Bolivia, the Dominican Republic, Jamaica and parts of Mexico, damaging homes, schools and health facilities and interrupting essential services for children and families. At the same time, prolonged drought conditions in the Amazon regions of Brazil and Peru reduced water availability, heightened food and nutrition insecurity and increased health risks for Indigenous and riverine communities. These climate extremes also contributed to disease outbreaks, including dengue, chikungunya, oropouche, leptospirosis and yellow fever, further straining overstretched health systems and disproportionately affecting children, pregnant and lactating women and adolescents. The humanitarian situation escalated further in the final quarter of the year. In October 2025, Hurricane Melissa, a catastrophic Category 5 hurricane, struck Jamaica before sweeping across Cuba and the Dominican Republic, causing widespread flooding, infrastructure destruction and prolonged disruption of water, sanitation, energy, health and education systems. The hurricane affected more than 8 million people across the subregion, with millions requiring humanitarian assistance, including nearly one million children. According to EM-DAT, the International Disaster Database, an estimated 10.3 million people were affected by disasters across Latin America and the Caribbean in 2025, underscoring the persistent scale of humanitarian needs. In response, UNICEF and its partners scaled up emergency preparedness, anticipatory action and response throughout the year under the revised HAC appeal. Working in close coordination with national authorities, civil society organisations and United Nations partners, UNICEF adapted service delivery in high-risk contexts, reinforced child protection, health, nutrition, education and WASH systems and expanded capacity building to strengthen timely, coordinated and child-centred response. Across the region, emergency WASH interventions focused on restoring and safeguarding access to safe drinking water through the rehabilitation of systems, water quality monitoring and treatment, and the provision of household- and community-level infrastructure. Education continuity was supported through temporary learning spaces, school rehabilitation and the distribution of learning and early childhood development materials. Child protection and mental health and psychosocial support services were expanded through child-friendly spaces, community-based interventions and training of frontline responders in psychological first aid, safeguarding and protection from sexual exploitation and abuse. At regional and national levels, early-warning systems, simulation exercises, anticipatory action and shock-responsive social protection mechanisms were strengthened to reinforce institutional readiness for future emergencies. Despite these efforts, significant humanitarian needs persist. Recurrent and overlapping shocks continue to strain governments’ resilience capacities, delay recovery and increase risks for children, particularly in contexts facing structural vulnerabilities and high climate exposure. Addressing these challenges requires sustained investment in preparedness, anticipatory action and recovery to ensure that children across Latin America and the Caribbean can access safe water, essential services, protection and education before, during and after emergencies.

### 2. [Philippines | Earthquake and Typhoons 2025 - Operation Update #3 (MDRPH057)](https://reliefweb.int/report/philippines/philippines-earthquake-and-typhoons-2025-operation-update-3-mdrph057)
- **Score:** 0.753 (High)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** $13,000,000
- **Matched Regions:** EAP
- **Summary:** Country: Philippines Source: International Federation of Red Cross and Red Crescent Societies Please refer to the attached file. A. SITUATION ANALYSIS Description of the crisis In late 2025, the Philippines faced a series of overlapping disasters that significantly escalated the humanitarian needs on the ground. A powerful earthquake in Cebu province marked the onset of the humanitarian crisis, followed by Typhoons Tino (Kalmaegi) and Uwan (Fungwong) in quick succession. The compounding nature of these disasters left a trail of massive destruction across various regions displacing thousands of families, severely disrupting livelihoods, and access to essential services. As a result, the cumulative impacts of these disasters further intensified the vulnerabilities of affected communities, indicating that recovery will be a prolonged process. On 30 September 2025, a magnitude 6.9 earthquake, with thousands of struck off the coast of Bogo City in northern Cebu. The shallow depth of the quake resulted in intense ground shaking, leading to the collapse of homes, damage to roads and bridges, and widespread power outages. Several municipalities in the Cebu province, including Daanbantayan, Medellin, San Remigio, Borbon, and parts of Cebu City, were among the hardest hit. Based on the Situational report no. 30 issued by the National Disaster Risk Reduction and Management Council (NDRRMC) 1 , more than 217,910 families were affected in Cebu Province alone, houses either destroyed or partially damaged. Critical infrastructure such as schools, government buildings, health facilities, and transport networks also sustained significant damage, disrupting access to basic services. Many families were forced to seek temporary shelter in evacuation centres, while others remain in unsafe living conditions due to limited housing options. As communities were just beginning to mobilize relief following the aftermath of the earthquake, Typhoon Tino (Kalmaegi) entered the Philippine Area of Responsibility (PAR) on 02 November 2025. The storm rapidly intensified and made multiple landfalls across Visayas region and Palawan, brought strong winds, heavy rainfall, flooding, and landslides. Multiple areas in Central Cebu, Mimaropa, the Negros Islands Region, and parts of Caraga experienced severe flooding, further damaging homes, livelihoods, and infrastructure. A total of 1,526,203 families were affected, 263,712 people were displaced, and agricultural lands were inundated, affecting food security and income sources for many households. Shortly after, Super Typhoon Uwan swept through Luzon and nearby coastal provinces, unleashing destructive winds, torrential rains, and causing storm surges. This resulted in additional destruction in some of the repeatedly affected areas. The typhoon led to widespread flooding in low-lying and coastal areas, damaged hundreds of thousands of houses, and disrupted power, water, transport, and communication services. Pre-emptive evacuations helped reduce casualties, but prolonged displacement and slow restoration of essential services continued to place pressure on affected communities. According to the NDRRMC Sitrep no. 24, STY Uwan affected approximately 2,242,319 families across various regions, while 355,992 people remained displaced. As a result of these compounded disasters, an estimated 13 million people were left in need of humanitarian assistance. The scale of the needs on the grounds remains immense, as affected communities continue to face urgent needs in shelter, water and sanitation, health care, food security, and livelihood recovery. The complexity of this humanitarian crisis underscores the importance of sustained and coordinated assistance to enable families recover safely, rebuild disrupted livelihoods, and strengthen community resilience.

### 3. [UNICEF Philippines Humanitarian Situation Report No. 7 (Multiple typhoons and earthquakes) (Reporting period: 30 January 2026 to 26 February)](https://reliefweb.int/report/philippines/unicef-philippines-humanitarian-situation-report-no-7-multiple-typhoons-and-earthquakes-reporting-period-30-january-2026-26-february)
- **Score:** 0.418 (Medium)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** EAP
- **Summary:** Country: Philippines Source: UN Children's Fund Please refer to the attached file. Highlights Through its partnership with the Department of Social Welfare and Development, UNICEF provided emergency cash assistance to 5,776 typhoon-affected families in Catanduanes, enabling households to prioritize food, education, health care and shelter repairs. Post-distribution monitoring confirmed that families received the correct amounts, were satisfied with the process, and that government systems enabled timely delivery and learning for future emergency responses. UNICEF strengthened child protection and psychosocial support systems across four municipalities in Catanduanes by completing training-of-trainers on psychological First Aid and advancing integrated child protection and gender-based violence referral pathways. These efforts expanded community-level access to mental health and psychosocial support while reinforcing local government capacity to ensure continuity of care beyond the immediate emergency response. This is the seventh and final situation report on the Philippine Government-led response, supported by UNICEF, to the successive emergencies that unfolded in the second half of 2025, underscoring the United Nation agency for children’s continuous support before, during, and after disasters.

### 4. [Afghanistan: Assisted Afghan Returnees from Pakistan, Iran and other countries | Weekly Update 22 February – 28 February 2026](https://reliefweb.int/report/afghanistan/assisted-afghan-returnees-pakistan-iran-and-other-countries-weekly-update-22-february-28-february-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Countries: Afghanistan, Iran (Islamic Republic of), Pakistan, Tajikistan Source: UN High Commissioner for Refugees Please refer to the attached Infographic.

### 5. [Bangladesh: Common Feedback Platform (CFP): Monthly Sector Report (January 2026)](https://reliefweb.int/report/bangladesh/common-feedback-platform-cfp-monthly-sector-report-january-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** Countries: Bangladesh, Myanmar Source: International Organization for Migration Please refer to the attached Infographic. The Common Feedback Platform (CFP) is a joint inter-agency report that gives an overview of some of the community feedback that is raised within the Cox’s Bazar, Bangladesh, Rohingya response. Through Complaints and Feedback Mechanisms (CFMs), affected communities share challenges regarding programs, services, and the associated humanitarian response. The anonymized data from different organizations are then combined and consolidated on a monthly basis to produce these outputs. The CFP aims to contribute towards Accountability to Affected Populations (AAP) and inform programming. It was developed to improve complaint management and reporting through harmonized referral standards developed directly with the Sectors and main actors responsible for responding to complaints. They are updated regularly to maintain relevance to the current context of assistance. As per the Accountability Manifesto and CFP Referral Guidance, Site Management (SM) agencies and their partners collect and refer data to sectors and service providers at both the camp and Cox’s Bazar coordination levels. The CFP reports reflect data collected through certain CFMs and the usage of these CFMs; they are not necessarily a reflection of the overall needs or satisfaction of the Rohingya living in camps. Therefore, receiving more tickets in a site or for a sector does not consequently mean that there are more needs there; rather, it might imply that there is more CFM coverage, trust in the system, or a larger population in the location where tickets are received. This report is produced by Needs and Population Monitoring (NPM). For more information on the CFP, please contact npmbangladesh@iom.int.

### 6. [Bangladesh: Common Feedback Platform (CFP): Monthly Camp Report (January 2026)](https://reliefweb.int/report/bangladesh/common-feedback-platform-cfp-monthly-camp-report-january-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** Countries: Bangladesh, Myanmar Source: International Organization for Migration Please refer to the attached Infographic. The Common Feedback Platform (CFP) is a joint inter-agency report that gives an overview of some of the community feedback that is raised within the Cox’s Bazar, Bangladesh, Rohingya response. Through Complaints and Feedback Mechanisms (CFMs), affected communities share challenges regarding programs, services, and the associated humanitarian response. The anonymized data from different organizations are then combined and consolidated on a monthly basis to produce these outputs. The CFP aims to contribute towards Accountability to Affected Populations (AAP) and inform programming. It was developed to improve complaint management and reporting through harmonized referral standards developed directly with the Sectors and main actors responsible for responding to complaints. They are updated regularly to maintain relevance to the current context of assistance. As per the Accountability Manifesto and CFP Referral Guidance, Site Management (SM) agencies and their partners collect and refer data to sectors and service providers at both the camp and Cox’s Bazar coordination levels. The CFP reports reflect data collected through certain CFMs and the usage of these CFMs; they are not necessarily a reflection of the overall needs or satisfaction of the Rohingya living in camps. Therefore, receiving more tickets in a site or for a sector does not consequently mean that there are more needs there; rather, it might imply that there is more CFM coverage, trust in the system, or a larger population in the location where tickets are received. This report is produced by Needs and Population Monitoring (NPM). For more information on the CFP, please contact npmbangladesh@iom.int.

### 7. [WHO Afghanistan strengthens emergency care for communities in Balkh](https://reliefweb.int/report/afghanistan/who-afghanistan-strengthens-emergency-care-communities-balkh)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Country: Afghanistan Source: World Health Organization 1 March 2026, Kabul, Afghanistan, - WHO Afghanistan has been strengthening emergency care services across the country through its Basic Emergency Care (BEC) training programme, enabling frontline health workers to respond faster and more effectively to trauma and life-threatening emergencies. One of the most recent successfully completed training courses was in Balkh Province, where 54 health professionals from Balkh, Faryab, Jawzjan, Samangan and Sar-e-Pol provinces enhanced their lifesaving skills with the generous support of the People and Government of Japan. For many communities, district hospitals are the only point of care when emergencies happen. To address this, the BEC training focused on practical, hands-on skills that help health workers quickly assess injuries, stabilize patients and organize emergency response systems to save lives before referral to specialized facilities. Aminullah Safi, an emergency room nurse at Sholgara District Hospital in Balkh, applied the skills gained from the training immediately upon returning to his hospital. He implemented practical actions to reorganize surgical and emergency equipment and strengthen trauma management practices. “Before the training, we did our best with the equipment and knowledge we had,” he said. “Now, the knowledge learned has enabled us to use our existing equipment and limited resources much more efficiently, so people in my district no longer have to wait helplessly during emergencies. We are ready to provide lifesaving care from the moment patients arrive.” “Every minute matters in an emergency,” said Dr Edwin Ceniza Salvador, WHO Representative to Afghanistan. “By strengthening the skills of frontline health workers and improving emergency readiness in district hospitals, we are helping save lives where people live - especially in communities far from specialized care. This is the real impact of sustained donor support.” Through continued partnership with Japan and other health partners, WHO Afghanistan is bringing lifesaving emergency care closer to families, reducing preventable deaths and helping hospitals stand ready during emergencies. For more information, please contact: Mariam Amiry RCCE Officer, WHO Afghanistan (Kabul) Mob.: +93 784100496 E-mail: amirym@who.int

### 8. [Supply and delivery of Rice and Cooking Oil for CBPAHA](https://www.ungm.org/Public/Notice/292548)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Supply and delivery of Rice and Cooking Oil for CBPAHA beneficiaries in Kabul International Airport. Note: Only applicable for Afghanistan Vendors.

### 9. [Call for External Collaborator – Modelling Framework for Early Warning System (Indonesia)](https://www.ungm.org/Public/Notice/292541)
- **Score:** 0.400 (Medium)
- **Published:** 2026-03-02
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** EAP
- **Summary:** Design and implement a modelling framework to assess whether high-frequency indicators can function as a district-level early warning system. The work includes data cleaning, model estimation, performance evaluation, robustness analysis and production of reproducible code.

### 10. [Humanitarian pressures grow as Cuba continues to struggle with energy shortages](https://news.un.org/feed/view/en/story/2026/02/1167046)
- **Score:** 0.398 (Low)
- **Published:** 2026-02-26
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** LAC
- **Summary:** Cuba’s humanitarian situation is worsening as fuel shortages deepen nearly a month after Washington took measures to block oil supplies from entering the Caribbean nation, a senior UN official warned on Wednesday.

### 11. [‘AI Kid of India’ urges young people to embrace technology](https://news.un.org/feed/view/en/story/2026/02/1167027)
- **Score:** 0.393 (Low)
- **Published:** 2026-02-28
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** 16-year-old Raul John Aju – dubbed the “AI Kid of India” at home – is a business prodigy who advises government and industry and has created several innovative AI tools.

### 12. [Fears grow for ordinary Afghans after further clashes with Pakistan](https://news.un.org/feed/view/en/story/2026/02/1167049)
- **Score:** 0.387 (Low)
- **Published:** 2026-02-27
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Reports on Friday that major cities in Afghanistan have been bombed by the Pakistan military in a new escalation between the two countries have raised fears for civilians already struggling under the harsh rule of the de facto Taliban authorities.

### 13. [Today's top news: Afghanistan, Occupied Palestinian Territory, Sudan, Niger](https://www.unocha.org/news/todays-top-news-afghanistan-occupied-palestinian-territory-sudan-niger)
- **Score:** 0.387 (Low)
- **Published:** 2026-02-27
- **Source:** OCHA - United Nations Office for the Coordination of Humanitarian Affairs
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Today's top news: Afghanistan, Occupied Palestinian Territory, Sudan, Niger NER_102025_UNOCHA-Ner_102025_UNOCHA-Ner_102025_UNOCHA-0060.jpg Jaspreet Kindra 27 Feb. 2026 4.51 p.m. # Afghanistan

### 14. [Afghanistan Humanitarian Fund supports families facing a harsh winter](https://www.unocha.org/news/afghanistan-humanitarian-fund-supports-families-facing-harsh-winter)
- **Score:** 0.387 (Low)
- **Published:** 2026-02-27
- **Source:** OCHA - United Nations Office for the Coordination of Humanitarian Affairs
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Afghanistan Humanitarian Fund supports families facing a harsh winter AFG_102023_UNOCHA_08227_KBG.jpg Jaspreet Kindra 27 Feb. 2026 2.49 p.m.

### 15. [World News in Brief: Arab economies rise, rights experts call for police reform in India, Ukraine school closures, Myanmar airstrikes](https://news.un.org/feed/view/en/story/2026/02/1167035)
- **Score:** 0.373 (Low)
- **Published:** 2026-02-25
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** A new UN report forecasts that the Arab region is seeing a gradual economic recovery despite continuing geopolitical uncertainties.

### 16. [Grain ATMs and hunger maps: AI innovations spotlighted at UN agency showcase in India](https://news.un.org/feed/view/en/story/2026/02/1166992)
- **Score:** 0.327 (Low)
- **Published:** 2026-02-18
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** Artificial intelligence solutions that transform the way food assistance reaches people facing hunger were on display during an exhibition at an AI meeting this week in New Delhi, India.


## Run Metadata

- **Output file:** `docs/index.md`
- **Metadata file:** `data/last_run.json`
- **Timezone:** UTC
