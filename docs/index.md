---
title: RFP Intelligence Analysis
updated: 2026-02-23 10:02:18 UTC
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

*Last updated: 2026-02-23 10:02:18 UTC*

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
- **Qualifying opportunities:** 10
- **Priority split:** High 0, Medium 8, Low 2
- **Top sources:** ReliefWeb - Updates (5), United Nations Global Marketplace (4), UN News - Global perspective Human stories (1)

## Pipeline Metrics

- **Fetched:** 136
- **After filtering:** 10
- **After deduplication:** 10
- **Selected top results:** 10
- **Dropped by age:** 53
- **Dropped by invalid date:** 0
- **Dropped by region:** 73
- **Region matched (annotated):** 10
- **Region unmatched (kept):** 73

## Scoring Summary

- **Entries scored:** 10
- **Average score:** 0.384
- **Highest score:** 0.435
- **Lowest score:** 0.227

## Priority Bands

- **High Priority (score ≥ 0.600):** Best-fit opportunities
- **Medium Priority (0.400–0.599):** Relevant but needs review
- **Low Priority (score < 0.400):** Monitor only
- **Current distribution:** High 0, Medium 8, Low 2

## Region Coverage

- **Matched region groups:** EAP (2), LAC (2), MENAP (7), SAR (6)

## Filtering Notes

- **Region handling:** Region criteria are used as a scoring signal.
- **Unmatched entries:** Items without region matches are retained and counted as Region unmatched (kept).

## Top Opportunities

### 1. [oPt: QRCS provides Ramadan Iftar, promotes food security for vulnerable families [EN/AR]](https://reliefweb.int/report/occupied-palestinian-territory/qrcs-provides-ramadan-iftar-promotes-food-security-vulnerable-families-enar)
- **Score:** 0.435 (Medium)
- **Published:** 2026-02-23
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** LAC, MENAP, SAR
- **Summary:** Country: occupied Palestinian territory Source: Qatar Red Crescent Society Please refer to the attached files. February 21st, 2026 ― Doha, Qatar: As part of its “Keep Your Balance of Good Deeds Alive” Ramadan Campaign 2026/1447 AH, Qatar Red Crescent Society (QRCS) has initiated the Ramadan Iftar projects, through its foreign representation offices/missions and in collaboration with sister National Societies and partners in the target countries. Under these projects, diverse one-month food parcels will be distributed to more than 300,000 beneficiaries in 17 countries: Palestine (Gaza and the West Bank), Sudan, Syria, Somalia, Chad, Afghanistan, Tanzania, Djibouti, Yemen, Niger, Bangladesh, Lebanon, Jordan, Mauritania, Albania, Kazakhstan, and Uganda. In Qatar, QRCS’s community care and development teams are implementing several Ramadan projects/initiatives, including Ramadan Iftar, Zakat Al-Mal, Stand Together, Joy of Eid, On-the-Go Iftar, and Hero Meals. Overall, these projects/initiatives will reach out to no less than 30,000 people, including expatriate workers, vulnerable families, talabat riders, and the general public. In a statement, Mohamed Bader Al-Sada, Assistant Secretary-General for Relief and International Development at QRCS, explained the importance of food security projects: “For literally everyone, having something to eat is a critical issue, so we do our best to find a job and earn a living for ourselves and our families. In the context of crises and disasters, safe people lose their livelihoods and, by extension, nutrition, finding themselves in a life-or-death situation. That is why QRCS pays great attention to enhancing food security as a key relief intervention to alleviate the impact of crises or disasters on the victims, help them remain strong, and preserve their dignity from hunger and helplessness”. Apart from Ramadan Iftar projects during Ramadan 1447 AH, Mr. Al-Sada said, QRCS is planning to implement 15 year-round food security projects, at a total cost of QR 49,615,560, for the benefit of 781,236 people in 10 countries: Syria, Yemen, Palestine (Gaza and the West Bank), Somalia, Niger, Bangladesh, Jordan, Afghanistan, Sudan, and Lebanon. These projects include the provision of food parcels and hot meals, flour for bakeries to produce daily bread for families, therapeutic food items for malnourished children, and food for orphanages and nursing homes. Back in 2025, QRCS implemented a total of 70 food security projects, at a total cost of QR 59,874,044, for the benefit of 2,839,511 people in 17 countries: Bangladesh, Jordan, Palestine (Gaza and the West Bank), Syria, Uganda, Chad, Lebanon, Tanzania, Somalia, Sudan, Yemen, Niger, Djibouti, Tajikistan, Gambia, Mauritania, and Afghanistan. To maximize the vital impact of food security projects on the lives and health of beneficiaries, QRCS welcomes donations via its website ( https://qrcs.qa/cc ), mobile app ( https://qrcs.qa/apps ), donor service (66666364), home donation collection (33998898), or bank transfer as follows: QNB (IBAN: QA21QNBA000000000850020196062), QIIB (IBAN: QA66QIIB000000001111126666003), Al Rayan Bank (IBAN: QA18MAFR000000000011199980003), Dukhan Bank (IBAN: QA37BRWA000000000200000094340), or QIB (IBAN: QA51QISB000000000110575190014). ##End of Text## About Qatar Red Crescent Society (QRCS) Established in 1978, Qatar Red Crescent Society (QRCS) is Qatar’s first humanitarian and volunteering organization that aims to assist and empower vulnerable individuals and communities without partiality or discrimination. QRCS is a member of the International Red Cross and Red Crescent Movement, which consists of the International Federation of Red Cross and Red Crescent Societies (IFRC), the International Committee of the Red Cross (ICRC), and 191 National Societies. It is also a member of several GCC, Arab, and Islamic organizations, such as the Islamic Committee of International Crescent (ICIC) and the Arab Red Crescent and Red Cross Organization (ARCO). In this legally recognized capacity, QRCS has access to disaster and conflict zones, thus serving as an auxiliary to the State of Qatar in its humanitarian and social efforts — a role that distinguishes it from other local charities and NGOs. Both locally and internationally, QRCS has relief and development operations in numerous countries throughout the Middle East, Asia, Africa, Europe, and Central and South America. Its humanitarian mandates include disaster preparedness, response, recovery, and risk reduction. To mitigate the impact of disasters and improve the livelihoods of affected populations, QRCS provides medical services, food, water, shelter, and other needs of local communities. It is also active at the humanitarian diplomacy and advocacy front. With the help of a vast network of trained, committed staff and volunteers, QRCS aspires to improve the lives of vulnerable people by mobilizing the power of humanity, inspired by the seven Fundamental Principles of humanitarian action: humanity, impartiality, neutrality, independence, voluntary service, unity, and universality.

### 2. [Indonesia: ASEAN Weekly Disaster Update Week 6 | 16 – 22 Feb 2026](https://reliefweb.int/report/indonesia/asean-weekly-disaster-update-week-6-16-22-feb-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** EAP
- **Summary:** Countries: Indonesia, Philippines, Thailand Source: ASEAN Coordinating Centre for Humanitarian Assistance Please refer to the attached Infographic. REGIONAL SUMMARY: During the eighth week of 2026, a total of 27 disaster events were reported across the ASEAN region, including droughts, floods, landslides, storms, and strong winds in Indonesia, Malaysia, the Philippines, and Thailand, as well as Kanlaon volcanic activity. In Indonesia, Badan Nasional Penanggulangan Bencana ( BNPB ) reported incidents across West Java, Central Java, East Java, West Kalimantan, West Nusa Tenggara, North Sumatra, and Yogyakarta. In Malaysia, Agensi Pengurusan Bencana Negara ( NADMA ) reported flooding situations in Sabah and Sarawak. Meanwhile, in the Philippines, National Disaster Risk Reduction and Management Council ( NDRRMC ) and Department of Social Welfare and Development ( DSWD ) reported flooding incidents in Regions XI, XII, and CARAGA, as well as volcanic activity at Kanlaon Volcano in NIR. In Thailand, Department of Disaster Prevention and Mitigation ( DDPM ) reported storms and strong winds in Nan, Phayao, Chiang Mai, and Mae Hong Son. In addition, Civil Protection Authority ( CPA ) of Timor-Leste reported flooding in Dili, with data collection on impacts and damages currently ongoing. HIGHLIGHT: In the Philippines, continuous moderate to heavy rainfall associated with a shear line caused flooding in several parts of the Davao Region on 19 February 2026. The same weather system continued to bring significant rainfall on 20 February 2026, resulting in further flooding, triggering landslides, and forcing the evacuation of residents in several areas of the CARAGA Region ( PAGASA , DSWD ). As a result of these conditions, according to DSWD , as of 23 February 2026 at 0500H UTC+7, around 197.8K families (740.7K persons) have been affected across 469 barangays in Regions XI and CARAGA, with around 27K families (10K persons) are currently taking temporary shelter in 74 evacuation centres. In terms of damages, reports indicate that 80 houses were damaged, including 27 totally damaged and 53 partially damaged houses. Relevant authorities have undertaken the necessary response actions to address the situation. HYDRO-METEO-CLIMATOLOGICAL: For the past week, data from the ASEAN Specialised Meteorological Centre ( ASMC ) indicated medium to high 7-day average rainfall across Brunei Darussalam, Indonesia, Malaysia, the Philippines, and Timor-Leste. As of this reporting, tropical disturbance INVEST 91B, is currently under monitoring for its potential development over the Bay of Bengal ( JTWC ). GEOPHYSICAL: Six (6) significant earthquakes (M>5.0) were recorded by Indonesia’s Badan Meteorologi, Klimatologi, dan Geofisika ( BMKG ) and Jabatan Meteorologi Malaysia ( JMM ). Among them, a M6.8 earthquake with a depth of 678 km and an epicentre located in the waters off Kota Kinabalu, Sabah, Malaysia, was reported by JMM on 22 February at 1157H UTC+7, reported by AEIC with a magnitude of 7.0 and a depth of 630 km. As of this reporting, no significant impacts or damages have been reported from the earthquake. Mount Marapi (alert level II), Semeru (alert level III), Ili Lewotolok (alert level III), and Ibu (alert level II) in Indonesia, and Taal (alert level 1), Mayon (alert level 3), and Kanlaon (alert level 2) volcanoes in the Philippines reported recent volcanic activity according to Pusat Vulkanologi dan Mitigasi Bencana Geologi ( PVMBG ) and the Philippines Institute of Volcanology and Seismology ( PHIVOLCS ). OUTLOOK: According to the ASEAN Specialised Meteorological Centre ( ASMC ), for the coming week, wetter conditions are predicted over parts of the northeastern Maritime Continent; and drier than usual conditions are predicted over much of the western and central equatorial region. For the regional assessment of extremes, a small increase in chance of very heavy rainfall is predicted over parts of northeastern Borneo; and a small increase in chance of extreme hot conditions is predicted for parts of the equatorial region, in particular parts of Peninsular Malaysia, central Sumatra, Sulawesi, southern Philippines and the Maluku Islands. La Niña conditions are predicted to weaken in February 2026 and transition to ENSO-neutral conditions in March 2026. Models predict the ENSO-neutral conditions to persist at least until May 2026, with either ENSO-neutral continuing or El Niño conditions developing in June-July 2026. Sources: ASEAN Disaster Monitoring & Response System (DMRS); ASEAN Disaster Information Network (ADINet); ASEAN Specialised Meteorological Centre (ASMC); ASEAN Earthquake Information Centre (AEIC); Joint Typhoon Warning Centre (JTWC); Indonesia: BNPB, BMKG, PVMBG; Malaysia: NADMA, JMM; Philippines: NDRRMC, PHIVOLCS, DSWD; Thailand: DDPM; Timor-Leste: CPA; Various news agencies.

### 3. [DR Congo: Équipe d’Analyse des Crises - RD Congo : Rapport mensuel de déplacement, janvier 2026](https://reliefweb.int/report/democratic-republic-congo/equipe-danalyse-des-crises-rd-congo-rapport-mensuel-de-deplacement-janvier-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** LAC
- **Summary:** Country: Democratic Republic of the Congo Source: Mercy Corps Please refer to the attached file. Tendances de déplacement en janvier 2026 Baisse de 4% du nombre de ménages déplacés en janvier 2026 par rapport au mois précédent selon les alertes rapportées au cours du mois, soit un total de 218 933 ménages déplacés dans les cinq provinces de l’Est de la RDC. Le Nord d-Kivu a recensé 91 023 ménages déplacés, suivi du Sud-Kivu avec 87 247 ménages, du Maniema avec 21 079 ménages, de l’Ituri avec 12 834 ménages et du Tanganyika avec 6 750 ménages. En décembre, 11% des mouvements observés, soit 25 124 ménages, correspondent à des retours vers les localités d’origine, principalement dans le territoire de Mahagi, Djugu (en Ituri), Rutshuru (au Nord-Kivu), Walungu, Uvira et Fizi (au Sud-Kivu). On observe une persistance des tensions armées dans les zones sous contrôle du M23, marquée par des affrontements récurrents, notamment dans les territoires de Rutshuru, Masisi et Walikale. Par ailleurs, la poursuite des combats entre FARDC et ses alliés au Sud-Kivu, continue de provoquer de nouveaux mouvements de population. La province du Nord-Kivu a été la plus fortement affectée par les déplacements, avec les territoires de Rutshuru, Masisi et Walikale fortement touchés par des combats récurrents entre le M23 et les FARDC alliés au VDP et Wazalendo. Ces affrontements, conjugués aux frappes aériennes et à l’intensifaction des opérations M23 contre les FDLR et Nyatura CMC, ont provoqué des déplacements massifs de civils, notamment dans les zones de santé de Kibirizi, Rutshuru, Mweso, Masisi, Kirotshe, Pinga et Kibua. Bien qu’une accalmie relative ait permis le retour d’une partie des ménages dans le territoire de Rutshuru, la tendance générale reste dominée par des déplacements récents et une forte instabilité sécuritaire. Par ailleurs, une intensification de la menace ADF dans le Grand Nord-Kivu a occasionné un déplacement des populations en territoire de Beni. En janvier 2026, les déplacements au Sud-Kivu sont restés élevés, principalement en raison des affrontements persistants entre le M23, les FARDC et leurs alliés, ainsi que des violences impliquant d’autres groupes armés locaux. Les territoires de Mwenga, Walungu, Uvira et Fizi ont été les plus affectés. La situation a également été marquée par des retours limités, souvent motivés par la dégradation des conditions de vie dans les zones d’accueil et par des accalmies sécuritaires localisées, dans un contexte de besoins humanitaires croissants et d’accès toujours contraint. En Ituri, les déplacements sont restés alimentés par l’activisme des groupes armés, notamment la CRP/Zaïre et les ADF, entraînant de nouveaux déplacements à Mahagi et Mambasa. La période a aussi été marquée par des retours localisés, favorisés par des accalmies sécuritaires relatives et la réduction de l’assistance humanitaire, dans un contexte de besoins toujours élevés. Au Tanganyika, les mouvements de population ont été marqués par l’extension du conflit dans le Sud-Kivu, notamment l’avancée du M23 vers Fizi après la prise d’Uvira en décembre. Cette dynamique a entraîné l’arrivée de ménages déplacés en provenance d’Uvira et de Fizi vers Kalemie et les localités du littoral du lac Tanganyika, dans un contexte de recherche de sécurité et de pression croissante sur les zones d’accueil. Dans la province du Maniema, les déplacemen ont été principalement liés aux dynamiques sécuritaires, notamment les tensions entre groupes Maï-Maï et FARDC ainsi que les effets de débordement de la crise M23 depuis le Sud-Kivu. La période a également été marquée par des déplacements provoqués par des aléas climatiques à Kindu, aggravant la vulnérabilité des populations et la pression sur les zones d’accueil.

### 4. [Iraq: Beyond the Flames: Environmental Impact, Climate Stress, and Community Realities in Basra](https://reliefweb.int/report/iraq/beyond-flames-environmental-impact-climate-stress-and-community-realities-basra)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** MENAP
- **Summary:** Country: Iraq Source: Aid Gate Organization Please refer to the attached file. This comprehensive assessment, conducted between December 2025 and January 2026, presents evidence-based findings from 1,096 household surveys and eight Focus Group Discussions across Basra Governorate. The report examines the intersection of climate stress, environmental degradation, oil-sector impacts, and community resilience, providing timely insights into one of Iraq’s most climate-vulnerable regions.

### 5. [Afghanistan: Asia and the Pacific 2026 Regional Focus Model (January 2026)](https://reliefweb.int/report/afghanistan/asia-and-pacific-2026-regional-focus-model-january-2026)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** ReliefWeb - Updates
- **Budget:** Not detected
- **Matched Regions:** EAP, MENAP, SAR
- **Summary:** Countries: Afghanistan, Australia, Bangladesh, Bhutan, Brunei Darussalam, Cambodia, China, Democratic People's Republic of Korea, Fiji, India, Indonesia, Japan, Kiribati, Lao People's Democratic Republic (the), Malaysia, Maldives, Marshall Islands, Micronesia (Federated States of), Mongolia, Myanmar, Nauru, Nepal, New Zealand, Pakistan, Palau, Papua New Guinea, Philippines, Republic of Korea, Samoa, Singapore, Somalia, Sri Lanka, Thailand, Timor-Leste, Tonga, Tuvalu, Vanuatu, Viet Nam Source: UN Office for the Coordination of Humanitarian Affairs Please refer to the attached Infographic. A key challenge faced by humanitarian agencies is how to ensure that limited available resources are allocated where they are most needed and are efficiently delivered in a principled manner. Decisions to allocate resources must strike a balance between meeting the immediate needs of crisis affected communities and supporting efforts to strengthen resilience and response preparedness to future emergencies. To support humanitarian partners address some of these challenges, the OCHA Regional Office for Asia and the Pacific (ROAP) produces the Regional Focus Model (RFM). The model is based on INFORM, a global risk index that identifies and analyzes where crises requiring international assistance may occur. It can be used to support decisions about disaster risk reduction, emergency preparedness and response. The model identifies hazard-prone countries that combine high vulnerability and low capacity to respond, and are therefore more likely to request and accept support from the international community. The model also includes a "Humanitarian" component, reflecting issues more directly related to OCHA's coordination work. This humanitarian component is combined with INFORM to produce a Focus score. The result is to provide a practical tool to inform and guide disaster managers, by providing an evidence base on which to base discussions and prioritization. In 2026, the RFM covers analysis of 38 countries in the Asia-Pacific region under ROAP in Bangkok, Thailand and the Office of the Pacific (OP) in Suva, Fiji.

### 6. [ITB#135790 Package # 31 – AF2 WSM: Construction of 1. Khaibar and 2. Chelgazi Check Dams in 1. Khaibar and 2. Chelgazi Districts of Faryab Province, North/Mazar Regional Office of Afghanistan](https://www.ungm.org/Public/Notice/291877)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** ITB#135790 Package # 31 – AF2 WSM: Construction of 1. Khaibar and 2. Chelgazi Check Dams in 1. Khaibar and 2. Chelgazi Districts of Faryab Province, North/Mazar Regional Office of Afghanistan.

### 7. [ITB#135789 Package # 29 – AF2 WSM: Construction of 1. Alburs and 2. Marmul Check Dams in 1. Alburs and 2. Marmul Districts of Balkh Province, North/Mazar Regional Office of Afghanistan](https://www.ungm.org/Public/Notice/291875)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** ITB#135789 Package # 29 – AF2 WSM: Construction of 1. Alburs and 2. Marmul Check Dams in 1. Alburs and 2. Marmul Districts of Balkh Province, North/Mazar Regional Office of Afghanistan

### 8. [Establishment of Blanket Purchase Agreements (BPAs) for Cleaning and Accommodation Items for UNOPS Afghanistan (2 Lots)](https://www.ungm.org/Public/Notice/291876)
- **Score:** 0.400 (Medium)
- **Published:** 2026-02-23
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP, SAR
- **Summary:** Tender description: Establishment of Blanket Purchase Agreements (BPAs) for Cleaning and Accommodation Items for UNOPS Afghanistan (2 Lots) ----- IMPORTANT NOTE: Interested vendors must respond to this tender using the UNOPS eSourcing system , via the UNGM portal. In order to access the full UNOPS tender details, request clarifications on the tender, and submit a vendor response to a tender using the system, vendors need to be registered as a UNOPS vendor at the UNGM portal and be logged into UNGM. For guidance on how to register on UNGM and submit responses to UNOPS tenders in the UNOPS eSourcing system, please refer to the user guide and other resources available at: https://esourcing.unops.org/#/Help/Guides Interested in improving your knowledge of what UNOPS procures, how we procure and how to become a vendor to supply to our organization? Learn more about our free online course on “Doing business with UNOPS” here

### 9. [Grain ATMs and hunger maps: AI innovations spotlighted at UN agency showcase in India](https://news.un.org/feed/view/en/story/2026/02/1166992)
- **Score:** 0.373 (Low)
- **Published:** 2026-02-18
- **Source:** UN News - Global perspective Human stories
- **Budget:** Not detected
- **Matched Regions:** SAR
- **Summary:** Artificial intelligence solutions that transform the way food assistance reaches people facing hunger were on display during an exhibition at an AI meeting this week in New Delhi, India.

### 10. [Supply and delivery of materials for 10 workshops at Ninawa Agriculture School and Intisar Vocational School in Ninewa, Iraq.](https://www.ungm.org/Public/Notice/289708)
- **Score:** 0.227 (Low)
- **Published:** 2026-01-28
- **Source:** United Nations Global Marketplace
- **Budget:** Not detected
- **Matched Regions:** MENAP
- **Summary:** UNESCO Invitation to Bid (ITB) – Ref: IRQ/ITB/26/08 Date: 28 January 2026 Deadline for Submission: 27 February 2026, 18:00 Baghdad Time Submission Email: baghdad.proc@unesco.org Scope: Supply and delivery of materials for 10 workshops at Ninawa Agriculture School and Intisar Vocational School in Ninewa, Iraq.


## Run Metadata

- **Output file:** `docs/index.md`
- **Metadata file:** `data/last_run.json`
- **Timezone:** UTC
