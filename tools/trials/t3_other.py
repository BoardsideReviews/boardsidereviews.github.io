# Trial and Error bank, part 3: pulmonary, ID, GI/hepatology, nephrology, endocrine, neurology, heme/onc, general.
from _t import T

# ---------- Pulmonary ----------
T("nlst","NLST","N Engl J Med",2011,"Reduced lung-cancer mortality with low-dose computed tomographic screening","Pulmonary",
  "53454 adults 55 to 74 with 30 or more pack-years, current smokers or quit within 15 years",
  "Three annual low-dose CT scans",
  "Three annual chest radiographs",
  "Lung cancer mortality",
  "pos","Lung cancer deaths fell 20.0% with low-dose CT. All-cause mortality fell 6.7%.",
  "Low-dose CT screening saves lives in heavy smokers. It is the basis of today's screening guidelines.")

T("nelson","NELSON","N Engl J Med",2020,"Reduced Lung-Cancer Mortality with Volume CT Screening in a Randomized Trial","Pulmonary",
  "13195 men (plus a smaller group of women) 50 to 74 with heavy smoking history",
  "Volume CT screening at baseline, 1, 3, and 5.5 years",
  "No screening",
  "Lung cancer mortality at 10 years",
  "pos","Lung cancer mortality rate ratio 0.76 at 10 years. False positives were low with volume-based nodule management.",
  "Confirmed NLST in Europe and showed that volume-based nodule rules keep false positives down.")

T("inpulsis","INPULSIS","N Engl J Med",2014,"Efficacy and safety of nintedanib in idiopathic pulmonary fibrosis","Pulmonary",
  "1066 patients with IPF in two replicate trials",
  "Nintedanib 150 mg twice daily",
  "Placebo",
  "Annual rate of FVC decline",
  "pos","FVC decline −114.7 vs −239.9 mL per year in INPULSIS-1, with similar results in INPULSIS-2. Diarrhea was common.",
  "Nintedanib roughly halves FVC decline in IPF.")

T("ascend-ipf","ASCEND","N Engl J Med",2014,"A phase 3 trial of pirfenidone in patients with idiopathic pulmonary fibrosis","Pulmonary",
  "555 patients with IPF",
  "Pirfenidone 2403 mg daily",
  "Placebo",
  "Change in FVC or death at week 52",
  "pos","Pirfenidone gave a 47.9% relative reduction in the share of patients with an FVC drop of 10 points or more, or death.",
  "Pirfenidone slows IPF. Watch for GI upset, photosensitivity, and liver tests.")

T("panther-ipf","PANTHER-IPF (triple therapy)","N Engl J Med",2012,"Prednisone, azathioprine, and N-acetylcysteine for pulmonary fibrosis","Pulmonary",
  "Patients with mild-to-moderate IPF",
  "Prednisone, azathioprine, and N-acetylcysteine",
  "Placebo",
  "Change in FVC over 60 weeks",
  "neg","Deaths 8 vs 1 and hospitalizations 23 vs 7 at interim analysis. The triple-therapy arm was stopped for harm.",
  "Immunosuppression harms IPF patients. IPF is not an inflammatory disease to treat with steroids.")

T("inbuild","INBUILD","N Engl J Med",2019,"Nintedanib in Progressive Fibrosing Interstitial Lung Diseases","Pulmonary",
  "663 patients with progressive fibrosing ILD other than IPF",
  "Nintedanib 150 mg twice daily",
  "Placebo",
  "Annual rate of FVC decline",
  "pos","FVC decline −80.8 vs −187.8 mL per year.",
  "Progressive pulmonary fibrosis responds to antifibrotics regardless of the underlying ILD.")

T("senscis","SENSCIS","N Engl J Med",2019,"Nintedanib for Systemic Sclerosis-Associated Interstitial Lung Disease","Pulmonary",
  "576 patients with systemic sclerosis-associated ILD",
  "Nintedanib 150 mg twice daily",
  "Placebo",
  "Annual rate of FVC decline",
  "pos","FVC decline −52.4 vs −93.3 mL per year. No effect on skin disease.",
  "Nintedanib slows lung function loss in scleroderma ILD.")

T("torch","TORCH","N Engl J Med",2007,"Salmeterol and fluticasone propionate and survival in chronic obstructive pulmonary disease","Pulmonary",
  "6112 patients with moderate-to-severe COPD",
  "Salmeterol plus fluticasone",
  "Placebo",
  "All-cause mortality at 3 years",
  "neu","Mortality 12.6% combination vs 15.2% placebo (P=0.052). Exacerbations fell. More pneumonia with fluticasone.",
  "A famous near miss. ICS/LABA reduced exacerbations but not, statistically, death.")

T("uplift","UPLIFT","N Engl J Med",2008,"A 4-year trial of tiotropium in chronic obstructive pulmonary disease","Pulmonary",
  "5993 patients with COPD",
  "Tiotropium",
  "Placebo (other inhalers allowed)",
  "Rate of decline in FEV1",
  "neu","No difference in the rate of FEV1 decline. Exacerbations fell and quality of life improved.",
  "LAMAs help symptoms and exacerbations but do not change the slope of lung function loss.")

T("impact","IMPACT","N Engl J Med",2018,"Once-Daily Single-Inhaler Triple versus Dual Therapy in Patients with COPD","Pulmonary",
  "10355 patients with symptomatic COPD and prior exacerbations",
  "Fluticasone furoate, umeclidinium, and vilanterol (triple therapy)",
  "Dual therapy (fluticasone/vilanterol or umeclidinium/vilanterol)",
  "Annual rate of moderate or severe exacerbations",
  "pos","Exacerbation rate 0.91 triple vs 1.07 ICS/LABA vs 1.21 LAMA/LABA. More pneumonia with ICS.",
  "Triple therapy cuts exacerbations in frequent exacerbators, especially with higher eosinophils.")

T("azithro-copd","Azithromycin for COPD","N Engl J Med",2011,"Azithromycin for prevention of exacerbations of COPD","Pulmonary",
  "1142 patients with COPD at increased risk of exacerbations",
  "Azithromycin 250 mg daily for 1 year",
  "Placebo",
  "Time to first exacerbation",
  "pos","Median time to first exacerbation 266 vs 174 days. Hearing decrements were more common.",
  "Daily azithromycin prevents exacerbations. Check hearing, QT, and nontuberculous mycobacteria first.")

T("reduce-copd","REDUCE","JAMA",2013,"Short-term vs conventional glucocorticoid therapy in acute exacerbations of chronic obstructive pulmonary disease","Pulmonary",
  "314 patients with an acute COPD exacerbation in the ED",
  "Prednisone 40 mg daily for 5 days",
  "Prednisone 40 mg daily for 14 days",
  "Re-exacerbation within 180 days (noninferiority)",
  "pos","Re-exacerbation 35.9% with 5 days vs 36.8% with 14 days, meeting noninferiority.",
  "Five days of prednisone is enough for COPD exacerbations.")

T("lott","LOTT","N Engl J Med",2016,"A Randomized Trial of Long-Term Oxygen for COPD with Moderate Desaturation","Pulmonary",
  "738 patients with COPD and moderate resting or exercise-induced desaturation",
  "Long-term supplemental oxygen",
  "No supplemental oxygen",
  "Time to death or first hospitalization",
  "neu","Hazard ratio 0.94. No benefit in any subgroup.",
  "Long-term oxygen helps only severe resting hypoxemia, not moderate desaturation.")

T("boreas","BOREAS","N Engl J Med",2023,"Dupilumab for COPD with Type 2 Inflammation Indicated by Eosinophil Counts","Pulmonary",
  "939 patients with COPD and blood eosinophils 300 or more on triple therapy",
  "Dupilumab every 2 weeks",
  "Placebo",
  "Annual rate of moderate or severe exacerbations",
  "pos","Exacerbation rate 0.78 vs 1.10 per year. FEV1 and quality of life improved.",
  "The first biologic shown to reduce exacerbations in eosinophilic COPD.")

T("mensa","MENSA","N Engl J Med",2014,"Mepolizumab treatment in patients with severe eosinophilic asthma","Pulmonary",
  "576 patients with severe eosinophilic asthma and recurrent exacerbations",
  "Mepolizumab IV or subcutaneous",
  "Placebo",
  "Rate of clinically significant exacerbations",
  "pos","Exacerbations fell 47% with IV and 53% with subcutaneous mepolizumab.",
  "Anti-IL-5 therapy halves exacerbations in eosinophilic asthma.")

T("ambition","AMBITION","N Engl J Med",2015,"Initial Use of Ambrisentan plus Tadalafil in Pulmonary Arterial Hypertension","Pulmonary",
  "500 treatment-naive patients with PAH, WHO functional class II or III",
  "Initial combination of ambrisentan plus tadalafil",
  "Ambrisentan or tadalafil monotherapy",
  "Time to clinical failure",
  "pos","Hazard ratio 0.50 for clinical failure, mostly fewer hospitalizations.",
  "Start most PAH patients on upfront dual oral therapy.")

T("griphon","GRIPHON","N Engl J Med",2015,"Selexipag for the Treatment of Pulmonary Arterial Hypertension","Pulmonary",
  "1156 patients with PAH, most on background therapy",
  "Selexipag (oral prostacyclin receptor agonist)",
  "Placebo",
  "Death or a complication related to PAH",
  "pos","Primary outcome 27.0% vs 41.6%. Mortality did not differ.",
  "Selexipag reduced PAH progression and hospitalizations when added to background therapy.")

T("stellar","STELLAR","N Engl J Med",2023,"Phase 3 Trial of Sotatercept for Treatment of Pulmonary Arterial Hypertension","Pulmonary",
  "323 patients with PAH on stable background therapy",
  "Sotatercept every 3 weeks",
  "Placebo",
  "Change in 6-minute walk distance at week 24",
  "pos","6-minute walk distance improved 40.8 m more than placebo. Telangiectasias and higher hemoglobin were common.",
  "A new mechanism (activin signaling) that improved exercise capacity on top of triple therapy.")

T("seraphin","SERAPHIN","N Engl J Med",2013,"Macitentan and morbidity and mortality in pulmonary arterial hypertension","Pulmonary",
  "742 patients with PAH",
  "Macitentan 3 mg or 10 mg daily",
  "Placebo",
  "Time to first morbidity or mortality event",
  "pos","Hazard ratio 0.55 with 10 mg. Anemia was more common.",
  "The first PAH trial built around a long-term outcome endpoint rather than walk distance.")

T("chest-1","CHEST-1","N Engl J Med",2013,"Riociguat for the treatment of chronic thromboembolic pulmonary hypertension","Pulmonary",
  "261 patients with inoperable or persistent post-surgical CTEPH",
  "Riociguat",
  "Placebo",
  "Change in 6-minute walk distance at week 16",
  "pos","6-minute walk distance increased 39 m with riociguat and fell 6 m with placebo (difference 46 m).",
  "Riociguat is the approved drug for inoperable or residual CTEPH. Surgery remains first-line when feasible.")

T("peitho","PEITHO","N Engl J Med",2014,"Fibrinolysis for patients with intermediate-risk pulmonary embolism","Pulmonary",
  "1005 normotensive PE patients with RV dysfunction and positive troponin",
  "Tenecteplase plus heparin",
  "Placebo plus heparin",
  "Death or hemodynamic decompensation within 7 days",
  "pos","Primary outcome 2.6% vs 5.6%. Major extracranial bleeding 6.3% vs 1.2%; stroke 2.4% vs 0.2%.",
  "Full-dose lysis prevents decompensation in intermediate-high-risk PE but causes too much bleeding to give routinely.")

T("prepic2","PREPIC2","JAMA",2015,"Effect of a retrievable inferior vena cava filter plus anticoagulation vs anticoagulation alone on risk of recurrent pulmonary embolism","Pulmonary",
  "399 patients with acute PE and DVT plus at least one severity criterion, able to be anticoagulated",
  "Retrievable IVC filter plus anticoagulation",
  "Anticoagulation alone",
  "Recurrent PE at 3 months",
  "neu","Recurrent PE 3.0% filter vs 1.5% anticoagulation alone.",
  "If a patient can be anticoagulated, adding an IVC filter does not help.")

T("attract","ATTRACT","N Engl J Med",2017,"Pharmacomechanical Catheter-Directed Thrombolysis for Deep-Vein Thrombosis","Pulmonary",
  "692 patients with acute proximal DVT",
  "Pharmacomechanical catheter-directed thrombolysis plus anticoagulation",
  "Anticoagulation alone",
  "Post-thrombotic syndrome at 6 to 24 months",
  "neu","Post-thrombotic syndrome 47% vs 48%. More major bleeding with thrombolysis.",
  "Routine catheter-directed lysis does not prevent post-thrombotic syndrome.")

T("mist1","MIST1","N Engl J Med",2005,"U.K. controlled trial of intrapleural streptokinase for pleural infection","Pulmonary",
  "454 patients with pleural infection",
  "Intrapleural streptokinase",
  "Placebo",
  "Death or need for surgical drainage at 3 months",
  "neu","No difference in death, surgery, radiographic outcome, or length of stay.",
  "A fibrinolytic alone does not help pleural infection. MIST2 later tested tPA with DNase.")

T("mist2","MIST2","N Engl J Med",2011,"Intrapleural use of tissue plasminogen activator and DNase in pleural infection","Pulmonary",
  "210 patients with pleural infection",
  "Intrapleural tPA plus DNase",
  "Placebo, tPA alone, or DNase alone (factorial)",
  "Change in pleural opacity on chest radiograph at day 7",
  "pos","Opacity fell 29.5% with tPA plus DNase vs 17.2% with placebo. Neither drug alone helped. Surgical referral and hospital stay fell.",
  "Use tPA and DNase together for complicated parapneumonic effusion or empyema.")

T("brown-ptx","Conservative management of pneumothorax","N Engl J Med",2020,"Conservative versus Interventional Treatment for Spontaneous Pneumothorax","Pulmonary",
  "316 patients 14 to 50 with a first moderate-to-large primary spontaneous pneumothorax",
  "Conservative management (observation, no drain)",
  "Interventional management (chest drain)",
  "Lung re-expansion within 8 weeks (noninferiority)",
  "pos","Re-expansion 94.4% conservative vs 98.5% interventional, meeting noninferiority in the main analysis, with fewer complications and recurrences.",
  "Many stable primary spontaneous pneumothoraces can be watched without a drain.")

T("save","SAVE","N Engl J Med",2016,"CPAP for Prevention of Cardiovascular Events in Obstructive Sleep Apnea","Pulmonary",
  "2717 adults with moderate-to-severe OSA and coronary or cerebrovascular disease",
  "CPAP plus usual care",
  "Usual care alone",
  "Cardiovascular death, MI, stroke, or hospitalization for HF, ACS, or TIA",
  "neu","Primary outcome 17.0% CPAP vs 15.4% usual care. Mean CPAP use was only 3.3 hours a night. Sleepiness and mood improved.",
  "Treat OSA for symptoms and quality of life. CPAP has not been shown to prevent cardiovascular events.")

T("surmount-osa","SURMOUNT-OSA","N Engl J Med",2024,"Tirzepatide for the Treatment of Obstructive Sleep Apnea and Obesity","Pulmonary",
  "469 adults with moderate-to-severe OSA and obesity, in two trials (with and without CPAP)",
  "Tirzepatide weekly",
  "Placebo",
  "Change in apnea-hypopnea index at 52 weeks",
  "pos","AHI fell substantially more with tirzepatide in both trials, along with marked weight loss.",
  "The first drug approved for OSA. Weight loss treats the cause.")

T("elexacaftor","ETI for cystic fibrosis","N Engl J Med",2019,"Elexacaftor-Tezacaftor-Ivacaftor for Cystic Fibrosis with a Single Phe508del Allele","Pulmonary",
  "403 patients 12 or older with CF, one Phe508del allele, and a minimal-function mutation",
  "Elexacaftor-tezacaftor-ivacaftor",
  "Placebo",
  "Change in percent predicted FEV1 at week 4",
  "pos","FEV1 improved 13.8 percentage points at week 4. Sweat chloride and exacerbations fell sharply.",
  "Highly effective CFTR modulation changed the course of cystic fibrosis for about 90% of patients.")

# ---------- Infectious diseases ----------
T("de-gans","Dexamethasone in bacterial meningitis","N Engl J Med",2002,"Dexamethasone in adults with bacterial meningitis","Infectious disease",
  "301 adults with suspected bacterial meningitis",
  "Dexamethasone 10 mg every 6 hours for 4 days, first dose before or with antibiotics",
  "Placebo",
  "Unfavorable outcome (Glasgow Outcome Scale) at 8 weeks",
  "pos","Unfavorable outcome relative risk 0.59; death relative risk 0.48. In pneumococcal meningitis, unfavorable outcome 26% vs 52%.",
  "Give dexamethasone before or with the first antibiotic dose in suspected bacterial meningitis.")

T("recovery-dex","RECOVERY (dexamethasone)","N Engl J Med",2021,"Dexamethasone in Hospitalized Patients with Covid-19","Infectious disease",
  "6425 patients hospitalized with COVID-19",
  "Dexamethasone 6 mg daily for up to 10 days",
  "Usual care",
  "28-day mortality",
  "pos","28-day mortality 22.9% vs 25.7%. The benefit was largest in ventilated patients. Patients not on oxygen did not benefit.",
  "The first drug shown to lower COVID-19 mortality, but only for patients needing oxygen.")

T("recovery-hcq","RECOVERY (hydroxychloroquine)","N Engl J Med",2020,"Effect of Hydroxychloroquine in Hospitalized Patients with Covid-19","Infectious disease",
  "4716 patients hospitalized with COVID-19",
  "Hydroxychloroquine",
  "Usual care",
  "28-day mortality",
  "neu","28-day mortality 27.0% hydroxychloroquine vs 25.0% usual care.",
  "Hydroxychloroquine does not help hospitalized COVID-19.")

T("actt-1","ACTT-1","N Engl J Med",2020,"Remdesivir for the Treatment of Covid-19 - Final Report","Infectious disease",
  "1062 adults hospitalized with COVID-19 and lower respiratory tract involvement",
  "Remdesivir for up to 10 days",
  "Placebo",
  "Time to recovery",
  "pos","Median recovery 10 days remdesivir vs 15 days placebo.",
  "Remdesivir shortens recovery, mostly in patients on low-flow oxygen.")

T("recovery-toci","RECOVERY (tocilizumab)","Lancet",2021,"Tocilizumab in patients admitted to hospital with COVID-19 (RECOVERY)","Infectious disease",
  "4116 hypoxic patients with COVID-19 and CRP 75 mg/L or more",
  "Tocilizumab plus usual care",
  "Usual care",
  "28-day mortality",
  "pos","28-day mortality 31% tocilizumab vs 35% usual care. 82% were also on steroids.",
  "IL-6 blockade added to steroids lowers mortality in hypoxic, inflamed COVID-19.")

T("together-ivm","TOGETHER (ivermectin)","N Engl J Med",2022,"Effect of Early Treatment with Ivermectin among Patients with Covid-19","Infectious disease",
  "1358 symptomatic outpatients with COVID-19 and a risk factor for progression",
  "Ivermectin for 3 days",
  "Placebo",
  "Hospitalization or prolonged ED observation within 28 days",
  "neu","No significant reduction in the primary outcome (relative risk 0.90).",
  "Ivermectin does not treat COVID-19.")

T("cape-cod","CAPE COD","N Engl J Med",2023,"Hydrocortisone in Severe Community-Acquired Pneumonia","Infectious disease",
  "800 ICU adults with severe community-acquired pneumonia (septic shock patients excluded)",
  "Hydrocortisone 200 mg/day for 4 or 8 days, then taper",
  "Placebo",
  "28-day mortality",
  "pos","28-day mortality 6.2% hydrocortisone vs 11.9% placebo. Fewer intubations and vasopressor starts.",
  "Early hydrocortisone helps severe CAP in the ICU. Influenza and septic shock were excluded.")

T("merino","MERINO","JAMA",2018,"Effect of Piperacillin-Tazobactam vs Meropenem on 30-Day Mortality for Patients With E coli or Klebsiella pneumoniae Bloodstream Infection and Ceftriaxone Resistance","Infectious disease",
  "379 adults with ceftriaxone-resistant E. coli or Klebsiella bloodstream infection",
  "Piperacillin-tazobactam",
  "Meropenem",
  "30-day mortality (noninferiority)",
  "neg","30-day mortality 12.3% piperacillin-tazobactam vs 3.7% meropenem. Noninferiority was not shown.",
  "For ESBL bacteremia, use a carbapenem, not piperacillin-tazobactam.")

T("balance","BALANCE","N Engl J Med",2025,"Seven versus 14 Days of Antibiotic Therapy for Bloodstream Infections","Infectious disease",
  "3608 hospitalized adults with bloodstream infection (mostly gram-negative), excluding S. aureus and severe immunosuppression",
  "7 days of antibiotics",
  "14 days of antibiotics",
  "90-day mortality (noninferiority)",
  "pos","90-day mortality 14.5% with 7 days vs 16.1% with 14 days, meeting noninferiority.",
  "For most uncomplicated bacteremias, 7 days is enough.")

T("poet","POET","N Engl J Med",2019,"Partial Oral versus Intravenous Antibiotic Treatment of Endocarditis","Infectious disease",
  "400 stable patients with left-sided endocarditis (strep, E. faecalis, S. aureus, or CoNS)",
  "Switch to oral antibiotics after at least 10 days of IV therapy",
  "Continued IV antibiotics",
  "Death, unplanned surgery, embolic events, or relapse (noninferiority)",
  "pos","Primary outcome 9.0% oral step-down vs 12.1% IV, meeting noninferiority.",
  "Stable endocarditis patients can step down to oral antibiotics.")

T("oviva","OVIVA","N Engl J Med",2019,"Oral versus Intravenous Antibiotics for Bone and Joint Infection","Infectious disease",
  "1054 adults with bone or joint infection",
  "Oral antibiotics within 7 days of surgery or starting antibiotics",
  "IV antibiotics for the first 6 weeks",
  "Definitive treatment failure at 1 year (noninferiority)",
  "pos","Treatment failure 13.2% oral vs 14.6% IV, meeting noninferiority. Fewer IV catheter complications.",
  "Oral antibiotics work for bone and joint infections and spare patients a PICC line.")

T("ease","EASE","N Engl J Med",2012,"Early surgery versus conventional treatment for infective endocarditis","Infectious disease",
  "76 patients with left-sided endocarditis, severe valve disease, and large vegetations",
  "Early surgery within 48 hours",
  "Conventional treatment (surgery only if complications arose)",
  "In-hospital death or embolic events within 6 weeks",
  "pos","Primary outcome 3% early surgery vs 23% conventional treatment, driven by fewer embolic events.",
  "Large vegetations with severe valve disease warrant early surgery.")

T("pneuma","PneumA","JAMA",2003,"Comparison of 8 vs 15 days of antibiotic therapy for ventilator-associated pneumonia in adults","Infectious disease",
  "401 patients with microbiologically confirmed ventilator-associated pneumonia",
  "8 days of antibiotics",
  "15 days of antibiotics",
  "Mortality, recurrent infection, and antibiotic-free days (noninferiority)",
  "pos","8 days was noninferior for mortality and recurrence, with more antibiotic-free days. Non-fermenters such as Pseudomonas recurred more.",
  "8 days is enough for most VAP.")

T("prorata","PRORATA","Lancet",2010,"Use of procalcitonin to reduce patients' exposure to antibiotics in intensive care units (PRORATA trial)","Infectious disease",
  "621 ICU patients with suspected bacterial infection",
  "Procalcitonin-guided starting and stopping of antibiotics",
  "Standard antibiotic practice",
  "Mortality at days 28 and 60 (noninferiority) and antibiotic-free days",
  "pos","Antibiotic-free days 14.3 vs 11.6, with noninferior mortality.",
  "Procalcitonin can safely shorten antibiotic courses in the ICU.")

T("proact","ProACT","N Engl J Med",2018,"Procalcitonin-Guided Use of Antibiotics for Lower Respiratory Tract Infection","Infectious disease",
  "1656 ED patients with suspected lower respiratory tract infection",
  "Procalcitonin-guided antibiotic recommendations",
  "Usual care",
  "Antibiotic-days by day 30",
  "neu","Mean antibiotic-days 4.2 procalcitonin vs 4.3 usual care.",
  "Where antibiotic use is already low, procalcitonin guidance added little.")

T("arrest-rif","ARREST (rifampicin)","Lancet",2018,"Adjunctive rifampicin for Staphylococcus aureus bacteraemia (ARREST)","Infectious disease",
  "758 adults with S. aureus bacteremia",
  "Adjunctive rifampicin for 2 weeks",
  "Placebo",
  "Bacteriologic failure or recurrence, or death, by week 12",
  "neu","Primary outcome 17% rifampicin vs 18% placebo. More drug interactions.",
  "Do not add rifampin routinely for S. aureus bacteremia.")

T("fidaxomicin","Fidaxomicin vs vancomycin","N Engl J Med",2011,"Fidaxomicin versus vancomycin for Clostridium difficile infection","Infectious disease",
  "629 adults with C. difficile infection",
  "Fidaxomicin 200 mg twice daily for 10 days",
  "Vancomycin 125 mg four times daily for 10 days",
  "Clinical cure (noninferiority)",
  "pos","Clinical cure 88.2% fidaxomicin vs 85.8% vancomycin (noninferior). Recurrence 15.4% vs 25.3%.",
  "Fidaxomicin cures as well as vancomycin and prevents more recurrences.")

T("van-nood","Fecal transplant for recurrent C. difficile","N Engl J Med",2013,"Duodenal infusion of donor feces for recurrent Clostridium difficile","Infectious disease",
  "43 patients with recurrent C. difficile infection",
  "Short vancomycin course, bowel lavage, then duodenal infusion of donor feces",
  "Vancomycin alone, or vancomycin with bowel lavage",
  "Cure without relapse at 10 weeks",
  "pos","Cure 81% after one infusion vs 31% with vancomycin alone. Stopped early for benefit.",
  "Fecal microbiota transplant is highly effective for recurrent C. difficile.")

T("modify","MODIFY I and II","N Engl J Med",2017,"Bezlotoxumab for Prevention of Recurrent Clostridium difficile Infection","Infectious disease",
  "2655 adults on standard therapy for C. difficile infection",
  "Single infusion of bezlotoxumab (anti-toxin B antibody)",
  "Placebo",
  "Recurrent infection within 12 weeks",
  "pos","Recurrence 17% vs 28% in MODIFY I and 16% vs 26% in MODIFY II.",
  "A toxin B antibody lowers C. difficile recurrence.")

T("smart-hiv","SMART","N Engl J Med",2006,"CD4+ count-guided interruption of antiretroviral treatment","Infectious disease",
  "5472 patients with HIV and CD4 above 350",
  "Drug conservation: stop ART and restart when CD4 fell below 250",
  "Continuous viral suppression with ART",
  "Opportunistic disease or death",
  "neg","Opportunistic disease or death hazard ratio 2.6 with treatment interruption. Stopped early.",
  "Never interrupt HIV therapy. Uncontrolled virus harms even when CD4 counts look fine.")

T("start","START","N Engl J Med",2015,"Initiation of Antiretroviral Therapy in Early Asymptomatic HIV Infection","Infectious disease",
  "4685 HIV-positive adults with CD4 above 500",
  "Immediate ART",
  "Deferred ART until CD4 fell to 350 or AIDS developed",
  "Serious AIDS-related or non-AIDS-related events or death",
  "pos","Hazard ratio 0.43 with immediate ART.",
  "Treat everyone with HIV as soon as possible, whatever the CD4 count.")

T("hptn-052","HPTN 052","N Engl J Med",2011,"Prevention of HIV-1 infection with early antiretroviral therapy","Infectious disease",
  "1763 serodiscordant couples",
  "Immediate ART for the HIV-positive partner",
  "Delayed ART",
  "Linked HIV transmission to the partner",
  "pos","Only 1 of 28 linked transmissions occurred in the early-therapy group (hazard ratio 0.04).",
  "Treatment is prevention: undetectable means untransmittable.")

T("coda","CODA","N Engl J Med",2020,"A Randomized Trial Comparing Antibiotics with Appendectomy for Appendicitis","Infectious disease",
  "1552 adults with appendicitis",
  "Antibiotics first",
  "Appendectomy",
  "30-day health status (EQ-5D) (noninferiority)",
  "pos","Antibiotics were noninferior for health status at 30 days. 29% of the antibiotic group had an appendectomy by 90 days, more often with an appendicolith.",
  "Antibiotics are a reasonable first choice for many with uncomplicated appendicitis, especially without an appendicolith.")

T("ptc-cap","PTC (3 days for CAP)","Lancet",2021,"Discontinuing beta-lactam treatment after 3 days for patients with community-acquired pneumonia in non-critical care wards (PTC)","Infectious disease",
  "310 adults on the ward with CAP who were clinically stable at day 3",
  "Stop beta-lactam after 3 days (placebo for 5 more days)",
  "Continue beta-lactam for 8 days total",
  "Cure at day 15 (noninferiority)",
  "pos","Cure 77% with 3 days vs 68% with 8 days, meeting noninferiority.",
  "Stable ward patients with CAP can stop antibiotics after 3 days.")

T("sort-sbp","Albumin in SBP","N Engl J Med",1999,"Effect of intravenous albumin on renal impairment and mortality in patients with cirrhosis and spontaneous bacterial peritonitis","GI/Hepatology",
  "126 patients with cirrhosis and spontaneous bacterial peritonitis",
  "Cefotaxime plus IV albumin (1.5 g/kg day 1, 1 g/kg day 3)",
  "Cefotaxime alone",
  "Renal impairment",
  "pos","Renal impairment 10% vs 33%. In-hospital mortality 10% vs 29%.",
  "Give albumin on days 1 and 3 for SBP, especially with renal dysfunction or high bilirubin.")

# ---------- GI / Hepatology ----------
T("villanueva","Transfusion in upper GI bleeding","N Engl J Med",2013,"Transfusion strategies for acute upper gastrointestinal bleeding","GI/Hepatology",
  "921 adults with severe acute upper GI bleeding",
  "Restrictive transfusion (threshold 7 g/dL)",
  "Liberal transfusion (threshold 9 g/dL)",
  "Death within 45 days",
  "pos","Survival at 6 weeks 95% restrictive vs 91% liberal. Less rebleeding, especially in cirrhosis.",
  "Over-transfusing GI bleeds raises portal pressure and rebleeding. Use 7 g/dL.")

T("rifaximin-he","Rifaximin for hepatic encephalopathy","N Engl J Med",2010,"Rifaximin treatment in hepatic encephalopathy","GI/Hepatology",
  "299 patients with cirrhosis in remission from recurrent hepatic encephalopathy",
  "Rifaximin 550 mg twice daily (91% also on lactulose)",
  "Placebo",
  "Breakthrough hepatic encephalopathy",
  "pos","Breakthrough HE 22.1% vs 45.9% (hazard ratio 0.42). HE hospitalizations fell.",
  "Add rifaximin to lactulose after recurrent hepatic encephalopathy.")

T("early-tips","Early TIPS","N Engl J Med",2010,"Early use of TIPS in patients with cirrhosis and variceal bleeding","GI/Hepatology",
  "63 high-risk cirrhotic patients (Child C, or Child B with active bleeding) with acute variceal bleeding",
  "Early covered TIPS within 72 hours",
  "Standard therapy (drugs plus endoscopic ligation, rescue TIPS if needed)",
  "Rebleeding or failure to control bleeding",
  "pos","Bleeding failure or rebleeding fell sharply with early TIPS. 1-year survival 86% vs 61%.",
  "In high-risk variceal bleeding, place a TIPS early rather than as a rescue.")

T("confirm","CONFIRM","N Engl J Med",2021,"Terlipressin plus Albumin for the Treatment of Type 1 Hepatorenal Syndrome","GI/Hepatology",
  "300 patients with cirrhosis and type 1 hepatorenal syndrome",
  "Terlipressin plus albumin",
  "Placebo plus albumin",
  "Verified reversal of hepatorenal syndrome",
  "pos","HRS reversal 32% terlipressin vs 17% placebo. More respiratory failure and deaths from respiratory disorders.",
  "Terlipressin reverses HRS but can cause respiratory failure. Watch volume status closely.")

T("attire","ATTIRE","N Engl J Med",2021,"A Randomized Trial of Albumin Infusions in Hospitalized Patients with Cirrhosis","GI/Hepatology",
  "777 hospitalized patients with decompensated cirrhosis and albumin under 3.0 g/dL",
  "Daily 20% albumin infusions to raise serum albumin to 3.5 g/dL or more",
  "Standard care",
  "Infection, renal dysfunction, or death (days 3 to 15)",
  "neu","Primary outcome 29.7% albumin vs 30.2% standard care. More pulmonary edema with albumin.",
  "Targeted albumin infusions do not help hospitalized cirrhotic patients. Use albumin for specific indications only.")

T("answer","ANSWER","Lancet",2018,"Long-term albumin administration in decompensated cirrhosis (ANSWER)","GI/Hepatology",
  "440 outpatients with cirrhosis and uncomplicated ascites on diuretics",
  "Weekly human albumin plus standard medical treatment",
  "Standard medical treatment",
  "Overall survival at 18 months",
  "pos","18-month survival 77% albumin vs 66% standard care.",
  "An open-label signal for long-term outpatient albumin in ascites. Practice varies, and ATTIRE tested a different, inpatient question.")

T("stopah","STOPAH","N Engl J Med",2015,"Prednisolone or pentoxifylline for alcoholic hepatitis","GI/Hepatology",
  "1103 patients with severe alcoholic hepatitis",
  "Prednisolone and/or pentoxifylline (factorial)",
  "Placebo",
  "28-day mortality",
  "neu","28-day mortality 14% prednisolone alone vs 17% placebo (odds ratio for prednisolone 0.72, P=0.06). Pentoxifylline did not help. No benefit at 90 days or 1 year.",
  "Steroids may give a small short-term benefit in severe alcoholic hepatitis. Pentoxifylline does not help.")

T("waterfall","WATERFALL","N Engl J Med",2022,"Aggressive or Moderate Fluid Resuscitation in Acute Pancreatitis","GI/Hepatology",
  "249 adults with acute pancreatitis",
  "Aggressive lactated Ringer's (20 mL/kg bolus then 3 mL/kg/h)",
  "Moderate lactated Ringer's (10 mL/kg bolus if hypovolemic, then 1.5 mL/kg/h)",
  "Development of moderately severe or severe pancreatitis",
  "neg","Moderately severe or severe pancreatitis 22.1% aggressive vs 17.3% moderate (not significant). Fluid overload 20.5% vs 6.3%. Stopped early for harm.",
  "Aggressive fluids cause fluid overload in pancreatitis without benefit. Resuscitate moderately and reassess.")

T("python","PYTHON","N Engl J Med",2014,"Early versus on-demand nasoenteric tube feeding in acute pancreatitis","GI/Hepatology",
  "208 patients with acute pancreatitis at high risk of complications",
  "Early nasoenteric tube feeding within 24 hours",
  "Oral diet at 72 hours, with tube feeding only if not tolerated",
  "Major infection or death within 6 months",
  "neu","Primary outcome 30% early vs 27% on-demand.",
  "There is no need to rush tube feeding in pancreatitis. Try an oral diet first.")

T("lau-ugib","Urgent endoscopy for UGIB","N Engl J Med",2020,"Timing of Endoscopy for Acute Upper Gastrointestinal Bleeding","GI/Hepatology",
  "516 patients with acute upper GI bleeding at high risk (Glasgow-Blatchford 12 or more)",
  "Urgent endoscopy within 6 hours of GI consultation",
  "Early endoscopy 6 to 24 hours after consultation",
  "30-day all-cause mortality",
  "neu","30-day mortality 8.9% urgent vs 6.6% early.",
  "Resuscitate first. Endoscopy within 24 hours is enough for most high-risk UGIB.")

T("halt-it","HALT-IT","Lancet",2020,"Effects of a high-dose 24-h infusion of tranexamic acid on death and thromboembolic events in patients with acute gastrointestinal bleeding (HALT-IT)","GI/Hepatology",
  "12009 patients with significant upper or lower GI bleeding",
  "High-dose tranexamic acid over 24 hours",
  "Placebo",
  "Death from bleeding within 5 days",
  "neu","Bleeding death 4% in both groups. More venous thromboembolism and seizures with tranexamic acid.",
  "Tranexamic acid does not help GI bleeding and causes clots. Do not give it.")

T("sup-icu","SUP-ICU","N Engl J Med",2018,"Pantoprazole in Patients at Risk for Gastrointestinal Bleeding in the ICU","GI/Hepatology",
  "3298 ICU adults at risk of GI bleeding",
  "IV pantoprazole 40 mg daily",
  "Placebo",
  "90-day mortality",
  "neu","90-day mortality 31.1% pantoprazole vs 30.4% placebo. Clinically important bleeding fell, a secondary outcome.",
  "Stress ulcer prophylaxis does not change mortality but does lower bleeding.")

T("revise","REVISE","N Engl J Med",2024,"Stress Ulcer Prophylaxis during Invasive Mechanical Ventilation","GI/Hepatology",
  "4821 ventilated ICU adults",
  "IV pantoprazole 40 mg daily",
  "Placebo",
  "Clinically important upper GI bleeding at 90 days",
  "pos","Clinically important bleeding 1.0% vs 3.5%. No difference in 90-day mortality or pneumonia.",
  "Prophylaxis reduces bleeding in ventilated patients without the feared pneumonia increase.")

# ---------- Nephrology ----------
T("choir","CHOIR","N Engl J Med",2006,"Correction of anemia with epoetin alfa in chronic kidney disease","Nephrology",
  "1432 patients with CKD and anemia, not on dialysis",
  "Epoetin alfa targeting hemoglobin 13.5 g/dL",
  "Epoetin alfa targeting hemoglobin 11.3 g/dL",
  "Death, MI, HF hospitalization, or stroke",
  "neg","Primary outcome hazard ratio 1.34 with the higher target. Stopped early. Quality of life did not improve.",
  "Do not push hemoglobin to normal with ESAs in CKD.")

T("treat","TREAT","N Engl J Med",2009,"A trial of darbepoetin alfa in type 2 diabetes and chronic kidney disease","Nephrology",
  "4038 patients with diabetes, CKD, and anemia",
  "Darbepoetin targeting hemoglobin 13 g/dL",
  "Placebo with rescue darbepoetin below 9 g/dL",
  "Death or cardiovascular event, and death or ESKD",
  "neu","No reduction in either composite (hazard ratio 1.05 for the cardiovascular composite). Stroke nearly doubled (hazard ratio 1.92).",
  "ESA therapy to a high target did not help and raised stroke risk.")

T("credence","CREDENCE","N Engl J Med",2019,"Canagliflozin and Renal Outcomes in Type 2 Diabetes and Nephropathy","Nephrology",
  "4401 patients with type 2 diabetes and albuminuric CKD",
  "Canagliflozin 100 mg daily",
  "Placebo",
  "ESKD, doubling of creatinine, or renal or cardiovascular death",
  "pos","Hazard ratio 0.70. Stopped early for benefit.",
  "SGLT2 inhibitors protect the kidneys in diabetic kidney disease.")

T("dapa-ckd","DAPA-CKD","N Engl J Med",2020,"Dapagliflozin in Patients with Chronic Kidney Disease","Nephrology",
  "4304 patients with CKD (eGFR 25 to 75) and albuminuria, with or without diabetes",
  "Dapagliflozin 10 mg daily",
  "Placebo",
  "Sustained eGFR decline of 50% or more, ESKD, or renal or cardiovascular death",
  "pos","Hazard ratio 0.61. Benefit was the same with and without diabetes. All-cause death also fell.",
  "SGLT2 inhibitors are kidney drugs, diabetes or not.")

T("empa-kidney","EMPA-KIDNEY","N Engl J Med",2023,"Empagliflozin in Patients with Chronic Kidney Disease","Nephrology",
  "6609 patients with CKD, including many without diabetes or albuminuria",
  "Empagliflozin 10 mg daily",
  "Placebo",
  "Progression of kidney disease or cardiovascular death",
  "pos","Primary outcome 13.1% vs 16.9% (hazard ratio 0.72).",
  "Extended SGLT2 benefit to a broader CKD population.")

T("fidelio","FIDELIO-DKD","N Engl J Med",2020,"Effect of Finerenone on Chronic Kidney Disease Outcomes in Type 2 Diabetes","Nephrology",
  "5734 patients with type 2 diabetes and CKD on maximal RAS blockade",
  "Finerenone (nonsteroidal MRA)",
  "Placebo",
  "Kidney failure, sustained eGFR decline of 40% or more, or renal death",
  "pos","Primary outcome 17.8% vs 21.1% (hazard ratio 0.82). More hyperkalemia.",
  "Finerenone adds kidney protection on top of an ACE inhibitor or ARB in diabetic kidney disease.")

T("ideal","IDEAL","N Engl J Med",2010,"A randomized, controlled trial of early versus late initiation of dialysis","Nephrology",
  "828 adults with progressive CKD",
  "Early dialysis start (eGFR 10 to 14)",
  "Late dialysis start (eGFR 5 to 7)",
  "All-cause mortality",
  "neu","Hazard ratio 1.04. Most of the late group started earlier than planned because of symptoms.",
  "Start dialysis for symptoms, not for a number.")

T("hemo","HEMO","N Engl J Med",2002,"Effect of dialysis dose and membrane flux in maintenance hemodialysis","Nephrology",
  "1846 patients on thrice-weekly hemodialysis",
  "High dialysis dose and/or high-flux membrane (factorial)",
  "Standard dose and/or low-flux membrane",
  "All-cause mortality",
  "neu","Neither higher dose nor high-flux membranes lowered mortality.",
  "Beyond standard adequacy targets, more dialysis did not improve survival.")

T("preserve","PRESERVE","N Engl J Med",2018,"Outcomes after Angiography with Sodium Bicarbonate and Acetylcysteine","Nephrology",
  "4993 high-risk patients undergoing angiography",
  "IV sodium bicarbonate, and/or oral acetylcysteine (factorial)",
  "IV saline, and/or placebo",
  "Death, dialysis, or persistent kidney injury at 90 days",
  "neu","Primary outcome 4.4% bicarbonate vs 4.7% saline, and 4.6% acetylcysteine vs 4.5% placebo.",
  "Neither bicarbonate nor acetylcysteine prevents contrast-associated kidney injury. Use isotonic saline when indicated.")

# ---------- Endocrine ----------
T("accord","ACCORD (glycemia)","N Engl J Med",2008,"Effects of intensive glucose lowering in type 2 diabetes","Endocrine",
  "10251 adults with type 2 diabetes and high cardiovascular risk",
  "Intensive glucose lowering, HbA1c target under 6.0%",
  "Standard therapy, HbA1c target 7.0 to 7.9%",
  "Nonfatal MI, nonfatal stroke, or cardiovascular death",
  "neg","Primary outcome 352 vs 371 events (hazard ratio 0.90, P=0.16), but deaths rose: 257 vs 203 (hazard ratio 1.22). Intensive therapy was stopped early for harm.",
  "Pushing HbA1c below 6% in high-risk type 2 diabetes kills. Individualize targets.")

T("advance","ADVANCE","N Engl J Med",2008,"Intensive blood glucose control and vascular outcomes in patients with type 2 diabetes","Endocrine",
  "11140 adults with type 2 diabetes",
  "Intensive glucose control with gliclazide, HbA1c target 6.5% or less",
  "Standard glucose control",
  "Combined major macrovascular and microvascular events",
  "pos","Combined outcome 18.1% vs 20.0% (hazard ratio 0.90), driven by less nephropathy. No macrovascular benefit or mortality harm.",
  "Tighter control slowed kidney disease without ACCORD's mortality signal.")

T("vadt","VADT","N Engl J Med",2009,"Glucose control and vascular complications in veterans with type 2 diabetes","Endocrine",
  "1791 veterans with poorly controlled type 2 diabetes",
  "Intensive glucose control",
  "Standard glucose control",
  "Time to first major cardiovascular event",
  "neu","Hazard ratio 0.88 (not significant). More hypoglycemia with intensive control.",
  "Intensive control in long-standing type 2 diabetes did not prevent cardiovascular events.")

T("ukpds-33","UKPDS 33","Lancet",1998,"Intensive blood-glucose control with sulphonylureas or insulin compared with conventional treatment and risk of complications in patients with type 2 diabetes (UKPDS 33)","Endocrine",
  "3867 adults with newly diagnosed type 2 diabetes",
  "Intensive control with a sulfonylurea or insulin",
  "Conventional diet-based treatment",
  "Any diabetes-related endpoint",
  "pos","Any diabetes-related endpoint fell 12%, mostly from a 25% drop in microvascular complications. Macrovascular events did not significantly fall.",
  "Early glucose control prevents microvascular disease. The 10-year follow-up showed a legacy effect on MI and death.")

T("dcct","DCCT","N Engl J Med",1993,"The effect of intensive treatment of diabetes on the development and progression of long-term complications in insulin-dependent diabetes mellitus","Endocrine",
  "1441 patients with type 1 diabetes",
  "Intensive insulin therapy (pump or 3 or more injections daily)",
  "Conventional therapy (1 to 2 injections daily)",
  "Development and progression of retinopathy",
  "pos","Intensive therapy cut the risk of developing retinopathy by 76%. Nephropathy and neuropathy also fell. Severe hypoglycemia tripled.",
  "Tight glucose control prevents microvascular complications in type 1 diabetes.")

T("dpp","DPP","N Engl J Med",2002,"Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin","Endocrine",
  "3234 adults with prediabetes and overweight",
  "Intensive lifestyle intervention, or metformin 850 mg twice daily",
  "Placebo",
  "Development of type 2 diabetes",
  "pos","Lifestyle cut diabetes incidence 58%; metformin cut it 31%.",
  "Lifestyle change prevents diabetes better than metformin.")

T("look-ahead","Look AHEAD","N Engl J Med",2013,"Cardiovascular effects of intensive lifestyle intervention in type 2 diabetes","Endocrine",
  "5145 overweight or obese adults with type 2 diabetes",
  "Intensive lifestyle intervention for weight loss",
  "Diabetes support and education",
  "Cardiovascular death, MI, stroke, or angina hospitalization",
  "neu","Hazard ratio 0.95. Stopped for futility after a median of 9.6 years.",
  "Modest lifestyle weight loss improved many things but not cardiovascular events.")

T("empa-reg","EMPA-REG OUTCOME","N Engl J Med",2015,"Empagliflozin, Cardiovascular Outcomes, and Mortality in Type 2 Diabetes","Endocrine",
  "7020 adults with type 2 diabetes and established cardiovascular disease",
  "Empagliflozin",
  "Placebo",
  "Cardiovascular death, nonfatal MI, or nonfatal stroke",
  "pos","Primary outcome 10.5% vs 12.1% (hazard ratio 0.86). Cardiovascular death fell 38%.",
  "The trial that turned SGLT2 inhibitors into heart and kidney drugs.")

T("leader","LEADER","N Engl J Med",2016,"Liraglutide and Cardiovascular Outcomes in Type 2 Diabetes","Endocrine",
  "9340 adults with type 2 diabetes at high cardiovascular risk",
  "Liraglutide",
  "Placebo",
  "Cardiovascular death, nonfatal MI, or nonfatal stroke",
  "pos","Primary outcome 13.0% vs 14.9% (hazard ratio 0.87).",
  "GLP-1 receptor agonists reduce cardiovascular events in type 2 diabetes.")

T("select","SELECT","N Engl J Med",2023,"Semaglutide and Cardiovascular Outcomes in Obesity without Diabetes","Endocrine",
  "17604 adults with obesity or overweight and cardiovascular disease, without diabetes",
  "Semaglutide 2.4 mg weekly",
  "Placebo",
  "Cardiovascular death, nonfatal MI, or nonfatal stroke",
  "pos","Primary outcome 6.5% vs 8.0% (hazard ratio 0.80).",
  "Semaglutide prevents cardiovascular events even without diabetes.")

T("step-1","STEP 1","N Engl J Med",2021,"Once-Weekly Semaglutide in Adults with Overweight or Obesity","Endocrine",
  "1961 adults with obesity or overweight with a comorbidity, without diabetes",
  "Semaglutide 2.4 mg weekly plus lifestyle intervention",
  "Placebo plus lifestyle intervention",
  "Percent change in body weight at 68 weeks",
  "pos","Weight change −14.9% vs −2.4%.",
  "Semaglutide produces weight loss approaching bariatric surgery for some patients.")

T("surmount-1","SURMOUNT-1","N Engl J Med",2022,"Tirzepatide Once Weekly for the Treatment of Obesity","Endocrine",
  "2539 adults with obesity or overweight with a comorbidity, without diabetes",
  "Tirzepatide 5, 10, or 15 mg weekly",
  "Placebo",
  "Percent change in body weight at 72 weeks",
  "pos","Weight change −20.9% with 15 mg vs −3.1% with placebo.",
  "Dual GIP/GLP-1 agonism produces about 20% weight loss.")

T("savor","SAVOR-TIMI 53","N Engl J Med",2013,"Saxagliptin and cardiovascular outcomes in patients with type 2 diabetes mellitus","Endocrine",
  "16492 adults with type 2 diabetes and cardiovascular disease or risk",
  "Saxagliptin",
  "Placebo",
  "Cardiovascular death, MI, or ischemic stroke",
  "neu","Primary outcome 7.3% vs 7.2% (hazard ratio 1.00). HF hospitalization 3.5% vs 2.8%.",
  "DPP-4 inhibitors are cardiovascular-neutral, and saxagliptin raised HF admissions.")

T("flow","FLOW","N Engl J Med",2024,"Effects of Semaglutide on Chronic Kidney Disease Outcomes in Type 2 Diabetes","Endocrine",
  "3533 adults with type 2 diabetes and CKD",
  "Semaglutide 1 mg weekly",
  "Placebo",
  "Kidney failure, 50% eGFR decline, or kidney or cardiovascular death",
  "pos","Hazard ratio 0.76. Stopped early for efficacy. Death also fell.",
  "GLP-1 receptor agonists join SGLT2 inhibitors as kidney-protective drugs in diabetes.")

T("whi","WHI (estrogen plus progestin)","JAMA",2002,"Risks and benefits of estrogen plus progestin in healthy postmenopausal women: principal results From the Women's Health Initiative randomized controlled trial","Endocrine",
  "16608 postmenopausal women with a uterus",
  "Conjugated estrogens plus medroxyprogesterone",
  "Placebo",
  "Coronary heart disease (invasive breast cancer as the primary adverse outcome)",
  "neg","Coronary heart disease hazard ratio 1.29; breast cancer hazard ratio 1.26. Stroke and VTE also rose. Stopped early.",
  "Hormone therapy does not prevent heart disease. Use it for menopausal symptoms, not for prevention.")

T("hers","HERS","JAMA",1998,"Randomized trial of estrogen plus progestin for secondary prevention of coronary heart disease in postmenopausal women","Endocrine",
  "2763 postmenopausal women with coronary disease",
  "Conjugated estrogens plus medroxyprogesterone",
  "Placebo",
  "Nonfatal MI or coronary death",
  "neu","Relative hazard 0.99. More events early in year 1 and more VTE.",
  "Hormone therapy does not prevent recurrent coronary events.")

T("trust","TRUST","N Engl J Med",2017,"Thyroid Hormone Therapy for Older Adults with Subclinical Hypothyroidism","Endocrine",
  "737 adults 65 or older with persistent subclinical hypothyroidism",
  "Levothyroxine",
  "Placebo",
  "Change in hypothyroid symptoms and tiredness scores at 1 year",
  "neu","No difference in hypothyroid symptoms or tiredness.",
  "Do not treat mild subclinical hypothyroidism in older adults for symptoms.")

T("vital","VITAL","N Engl J Med",2019,"Vitamin D Supplements and Prevention of Cancer and Cardiovascular Disease","Endocrine",
  "25871 healthy US adults (men 50 or older, women 55 or older)",
  "Vitamin D3 2000 IU daily (and omega-3s in a factorial design)",
  "Placebo",
  "Invasive cancer and major cardiovascular events",
  "neu","Cancer hazard ratio 0.96; cardiovascular events hazard ratio 0.97.",
  "Vitamin D supplements do not prevent cancer or cardiovascular disease in the general population.")

T("aspree","ASPREE","N Engl J Med",2018,"Effect of Aspirin on Disability-free Survival in the Healthy Elderly","General IM",
  "19114 healthy adults 70 or older (65 or older for US minorities)",
  "Aspirin 100 mg daily",
  "Placebo",
  "Disability-free survival",
  "neu","Hazard ratio 1.01. Major bleeding was higher, and all-cause mortality was unexpectedly higher with aspirin.",
  "Do not start aspirin for primary prevention in healthy older adults.")

T("atbc","ATBC","N Engl J Med",1994,"The effect of vitamin E and beta carotene on the incidence of lung cancer and other cancers in male smokers","General IM",
  "29133 Finnish male smokers aged 50 to 69",
  "Beta carotene and/or vitamin E (factorial)",
  "Placebo",
  "Lung cancer incidence",
  "neg","Lung cancer incidence was 18% higher with beta carotene. Total mortality was also higher.",
  "Beta carotene raises lung cancer risk in smokers. Antioxidant pills are not prevention.")

T("caret","CARET","N Engl J Med",1996,"Effects of a combination of beta carotene and vitamin A on lung cancer and cardiovascular disease","General IM",
  "18314 smokers, former smokers, and asbestos-exposed workers",
  "Beta carotene plus vitamin A (retinyl palmitate)",
  "Placebo",
  "Lung cancer incidence",
  "neg","Lung cancer relative risk 1.28. Stopped early for harm.",
  "Confirmed ATBC: beta carotene causes lung cancer in high-risk smokers.")

T("traverse","TRAVERSE","N Engl J Med",2023,"Cardiovascular Safety of Testosterone-Replacement Therapy","Endocrine",
  "5246 men 45 to 80 with hypogonadism and cardiovascular disease or high risk",
  "Transdermal testosterone",
  "Placebo",
  "Cardiovascular death, MI, or stroke (noninferiority)",
  "pos","Primary outcome 7.0% vs 7.3%, meeting noninferiority. More atrial fibrillation, AKI, and pulmonary embolism.",
  "Testosterone for true hypogonadism did not raise major cardiovascular events.")

T("horizon","HORIZON","N Engl J Med",2007,"Once-yearly zoledronic acid for treatment of postmenopausal osteoporosis","Endocrine",
  "7765 postmenopausal women with osteoporosis",
  "Zoledronic acid 5 mg IV once a year",
  "Placebo",
  "New vertebral fractures and hip fractures",
  "pos","Morphometric vertebral fractures fell 70%; hip fractures fell 41%. More serious atrial fibrillation.",
  "One yearly infusion cuts fractures, a good option when oral bisphosphonates fail.")

# ---------- Neurology ----------
T("ninds","NINDS tPA","N Engl J Med",1995,"Tissue plasminogen activator for acute ischemic stroke","Neurology",
  "624 patients with acute ischemic stroke within 3 hours of onset",
  "IV alteplase 0.9 mg/kg",
  "Placebo",
  "Favorable outcome at 3 months (global test of four scales)",
  "pos","Favorable outcome odds ratio 1.7. Symptomatic intracerebral hemorrhage 6.4% vs 0.6%.",
  "The trial that started acute stroke thrombolysis. Time is brain.")

T("ecass-3","ECASS III","N Engl J Med",2008,"Thrombolysis with alteplase 3 to 4.5 hours after acute ischemic stroke","Neurology",
  "821 patients with ischemic stroke 3 to 4.5 hours from onset",
  "IV alteplase",
  "Placebo",
  "Favorable outcome (modified Rankin 0 to 1) at 90 days",
  "pos","Favorable outcome 52.4% vs 45.2%.",
  "Extended the IV alteplase window to 4.5 hours.")

T("mr-clean","MR CLEAN","N Engl J Med",2015,"A randomized trial of intraarterial treatment for acute ischemic stroke","Neurology",
  "500 patients with anterior proximal large-vessel occlusion within 6 hours",
  "Intra-arterial treatment (mostly stent retrievers) plus usual care",
  "Usual care (89% received IV alteplase)",
  "Modified Rankin score at 90 days",
  "pos","Functional independence 32.6% vs 19.1%.",
  "The first positive modern thrombectomy trial.")

T("dawn","DAWN","N Engl J Med",2018,"Thrombectomy 6 to 24 Hours after Stroke with a Mismatch between Deficit and Infarct","Neurology",
  "206 patients with large-vessel occlusion 6 to 24 hours after last known well, with clinical-imaging mismatch",
  "Thrombectomy plus standard care",
  "Standard care",
  "Utility-weighted modified Rankin score and functional independence at 90 days",
  "pos","Functional independence 49% vs 13%. Stopped early for benefit.",
  "Selected patients with salvageable brain benefit from thrombectomy up to 24 hours.")

T("chance","CHANCE","N Engl J Med",2013,"Clopidogrel with aspirin in acute minor stroke or transient ischemic attack","Neurology",
  "5170 Chinese patients with minor stroke or high-risk TIA within 24 hours",
  "Clopidogrel plus aspirin for 21 days, then clopidogrel alone",
  "Aspirin alone",
  "Stroke at 90 days",
  "pos","Stroke 8.2% vs 11.7%. No increase in hemorrhage.",
  "Short-term dual antiplatelet therapy prevents early recurrent stroke after minor stroke or TIA.")

T("point","POINT","N Engl J Med",2018,"Clopidogrel and Aspirin in Acute Ischemic Stroke and High-Risk TIA","Neurology",
  "4881 patients with minor stroke or high-risk TIA within 12 hours",
  "Clopidogrel plus aspirin for 90 days",
  "Aspirin alone",
  "Ischemic stroke, MI, or ischemic vascular death at 90 days",
  "pos","Primary outcome 5.0% vs 6.5%. Major hemorrhage 0.9% vs 0.4%.",
  "DAPT works, but most of the benefit comes in the first weeks. Keep it short (about 21 days).")

T("sammpris","SAMMPRIS","N Engl J Med",2011,"Stenting versus aggressive medical therapy for intracranial arterial stenosis","Neurology",
  "451 patients with recent TIA or stroke from 70 to 99% intracranial stenosis",
  "Intracranial stenting plus aggressive medical management",
  "Aggressive medical management alone",
  "Stroke or death within 30 days, or stroke in the territory thereafter",
  "neg","30-day stroke or death 14.7% stenting vs 5.8% medical therapy. Stopped early.",
  "Aggressive medical therapy, not stenting, is the treatment for symptomatic intracranial stenosis.")

T("interact2","INTERACT2","N Engl J Med",2013,"Rapid blood-pressure lowering in patients with acute intracerebral hemorrhage","Neurology",
  "2839 patients with spontaneous intracerebral hemorrhage within 6 hours",
  "Intensive BP lowering (systolic under 140 within 1 hour)",
  "Guideline BP lowering (systolic under 180)",
  "Death or major disability (modified Rankin 3 to 6) at 90 days",
  "neu","Death or major disability 52.0% vs 55.6% (P=0.06). Ordinal analysis favored intensive lowering.",
  "Intensive BP lowering in ICH is safe and may modestly help.")

T("atach-2","ATACH-2","N Engl J Med",2016,"Intensive Blood-Pressure Lowering in Patients with Acute Cerebral Hemorrhage","Neurology",
  "1000 patients with ICH within 4.5 hours",
  "Intensive systolic target 110 to 139 mm Hg",
  "Standard systolic target 140 to 179 mm Hg",
  "Death or disability at 3 months",
  "neu","Death or disability 38.7% intensive vs 37.7% standard. More renal adverse events with intensive lowering.",
  "Very aggressive systolic lowering in ICH did not help. Aim for about 140, not lower.")

T("clots-3","CLOTS 3","Lancet",2013,"Effectiveness of intermittent pneumatic compression in reduction of risk of deep vein thrombosis in patients who have had a stroke (CLOTS 3)","Neurology",
  "2876 immobile patients with acute stroke",
  "Intermittent pneumatic compression plus routine care",
  "Routine care alone",
  "Proximal DVT within 30 days",
  "pos","Proximal DVT 8.5% vs 12.1%.",
  "Use pneumatic compression devices (not graduated stockings) to prevent DVT after stroke.")

T("esett","ESETT","N Engl J Med",2019,"Randomized Trial of Three Anticonvulsant Medications for Status Epilepticus","Neurology",
  "384 patients with benzodiazepine-refractory status epilepticus",
  "Levetiracetam, fosphenytoin, or valproate",
  "Each other (three-arm comparison)",
  "Cessation of seizures and improved responsiveness at 60 minutes",
  "neu","Success 47% levetiracetam, 45% fosphenytoin, 46% valproate.",
  "Any of the three works as a second-line drug. Pick by patient factors.")

T("rampart","RAMPART","N Engl J Med",2012,"Intramuscular versus intravenous therapy for prehospital status epilepticus","Neurology",
  "893 patients with status epilepticus treated by paramedics",
  "IM midazolam by autoinjector",
  "IV lorazepam",
  "Seizures stopped before ED arrival without rescue therapy (noninferiority)",
  "pos","Seizures stopped 73.4% IM midazolam vs 63.4% IV lorazepam.",
  "Don't wait for an IV. IM midazolam works at least as well.")

# ---------- Heme / Onc ----------
T("keynote-024","KEYNOTE-024","N Engl J Med",2016,"Pembrolizumab versus Chemotherapy for PD-L1-Positive Non-Small-Cell Lung Cancer","Heme/Onc",
  "305 patients with untreated advanced NSCLC, PD-L1 50% or more, no EGFR or ALK alterations",
  "Pembrolizumab",
  "Platinum-based chemotherapy",
  "Progression-free survival",
  "pos","Median PFS 10.3 vs 6.0 months. Overall survival also improved, with fewer adverse events.",
  "First-line immunotherapy alone for high PD-L1 NSCLC.")

T("apl","APL0406","N Engl J Med",2013,"Retinoic acid and arsenic trioxide for acute promyelocytic leukemia","Heme/Onc",
  "162 patients with low-to-intermediate-risk acute promyelocytic leukemia",
  "All-trans retinoic acid plus arsenic trioxide",
  "ATRA plus idarubicin chemotherapy",
  "Event-free survival at 2 years (noninferiority)",
  "pos","2-year event-free survival 97% vs 86%. Noninferiority met, and superiority was shown.",
  "Chemotherapy-free cure for most APL.")

T("clot","CLOT","N Engl J Med",2003,"Low-molecular-weight heparin versus a coumarin for the prevention of recurrent venous thromboembolism in patients with cancer","Heme/Onc",
  "Patients with active cancer and acute symptomatic VTE",
  "Dalteparin for 6 months",
  "Dalteparin then warfarin",
  "Recurrent symptomatic VTE",
  "pos","Recurrent VTE 9% dalteparin vs 17% warfarin, with similar bleeding.",
  "LMWH beat warfarin for cancer-associated VTE, the standard until DOACs.")

T("hokusai-cancer","Hokusai VTE Cancer","N Engl J Med",2018,"Edoxaban for the Treatment of Cancer-Associated Venous Thromboembolism","Heme/Onc",
  "1050 patients with cancer and acute VTE",
  "Edoxaban (after 5 days of LMWH)",
  "Dalteparin",
  "Recurrent VTE or major bleeding (noninferiority)",
  "pos","Primary outcome 12.8% edoxaban vs 13.5% dalteparin (noninferior). More major bleeding with edoxaban, mostly GI cancers.",
  "DOACs are an option for cancer VTE. Be cautious with GI and GU cancers.")

T("caravaggio","CARAVAGGIO","N Engl J Med",2020,"Apixaban for the Treatment of Venous Thromboembolism Associated with Cancer","Heme/Onc",
  "1155 patients with cancer and acute VTE",
  "Apixaban",
  "Dalteparin",
  "Recurrent VTE (noninferiority)",
  "pos","Recurrent VTE 5.6% apixaban vs 7.9% dalteparin, with no increase in major bleeding.",
  "Apixaban is a convenient, effective choice for cancer-associated VTE.")

T("erspc","ERSPC","N Engl J Med",2009,"Screening and prostate-cancer mortality in a randomized European study","Heme/Onc",
  "162243 men aged 55 to 69",
  "PSA screening, on average every 4 years",
  "No screening",
  "Prostate cancer mortality",
  "pos","Prostate cancer mortality fell 20%. 1410 men needed screening and 48 additional cancers treated to prevent one death.",
  "PSA screening saves some lives at a cost of considerable overdiagnosis. Shared decisions.")

T("plco-prostate","PLCO (prostate)","N Engl J Med",2009,"Mortality results from a randomized prostate-cancer screening trial","Heme/Onc",
  "76693 US men aged 55 to 74",
  "Annual PSA for 6 years and digital rectal exam for 4 years",
  "Usual care",
  "Prostate cancer mortality",
  "neu","No reduction in prostate cancer mortality. About half of the usual-care group had PSA testing anyway.",
  "Heavy screening in the control arm diluted any difference, which is why ERSPC and PLCO disagree.")
