# Trial and Error bank, part 1: critical care.
# T(id, name, journal, year, pubmed_title, area, pop, int, ctl, out, ans, res, sum)
# ans: "pos" = met its primary endpoint (including noninferiority when that was the goal)
#      "neu" = no significant difference on the primary endpoint
#      "neg" = worse on the primary endpoint, or stopped early for harm
from _t import T

T("arma","ARDSNet ARMA","N Engl J Med",2000,"Ventilation with lower tidal volumes as compared with traditional tidal volumes for acute lung injury and the acute respiratory distress syndrome","Critical care",
  "861 ventilated adults with acute lung injury or ARDS",
  "Tidal volume 6 mL/kg predicted body weight, plateau pressure 30 cm H2O or less",
  "Tidal volume 12 mL/kg predicted body weight, plateau pressure 50 cm H2O or less",
  "Death before discharge home breathing without assistance",
  "pos","Mortality 31.0% with low tidal volumes vs 39.8% with traditional volumes. The trial stopped early for benefit.",
  "Lung-protective ventilation saves lives in ARDS. Size tidal volumes to predicted (not actual) body weight and keep plateau pressure at 30 or below.")

T("proseva","PROSEVA","N Engl J Med",2013,"Prone positioning in severe acute respiratory distress syndrome","Critical care",
  "466 adults with severe ARDS (PaO2/FiO2 under 150 on FiO2 0.6 or more, PEEP 5 or more) after 12 to 24 hours of stabilization",
  "Early prone positioning for at least 16 consecutive hours a day",
  "Supine positioning",
  "28-day all-cause mortality",
  "pos","28-day mortality 16.0% prone vs 32.8% supine.",
  "In severe ARDS, prone early and for long sessions (16 hours or more). Earlier trials with short sessions and milder patients had missed this benefit.")

T("gattinoni-prone","Prone-Supine I","N Engl J Med",2001,"Effect of prone positioning on the survival of patients with acute respiratory failure","Critical care",
  "304 adults with acute lung injury or ARDS",
  "Prone positioning about 7 hours a day for 10 days",
  "Conventional supine positioning",
  "Mortality at 10 days, ICU discharge, and 6 months",
  "neu","Oxygenation improved, but mortality did not differ at any time point.",
  "Short daily prone sessions in a mixed-severity population did not save lives. PROSEVA later showed benefit with longer sessions in severe ARDS.")

T("acurasys","ACURASYS","N Engl J Med",2010,"Neuromuscular blockers in early acute respiratory distress syndrome","Critical care",
  "340 adults with early, severe ARDS (PaO2/FiO2 under 150) on deep sedation",
  "Cisatracurium infusion for 48 hours",
  "Placebo",
  "90-day mortality, adjusted for baseline severity",
  "pos","Adjusted hazard ratio for death at 90 days 0.68 (95% CI 0.48 to 0.98). Crude mortality 31.6% vs 40.7%.",
  "A positive single trial whose control arm was deeply sedated. The larger ROSE trial, with lighter sedation in controls, did not reproduce the benefit.")

T("rose","ROSE","N Engl J Med",2019,"Early neuromuscular blockade in the acute respiratory distress syndrome","Critical care",
  "1006 adults with moderate-to-severe ARDS (PaO2/FiO2 under 150) on a high-PEEP strategy",
  "Cisatracurium infusion for 48 hours with deep sedation",
  "Usual care with lighter sedation targets and no routine paralysis",
  "In-hospital death by day 90",
  "neu","90-day in-hospital mortality 42.5% vs 42.8%.",
  "Routine early paralysis does not improve survival in moderate-to-severe ARDS. Save it for specific problems like severe ventilator dyssynchrony.")

T("cesar","CESAR","Lancet",2009,"Efficacy and economic assessment of conventional ventilatory support versus extracorporeal membrane oxygenation for severe adult respiratory failure (CESAR)","Critical care",
  "180 adults with severe but potentially reversible respiratory failure (Murray score above 3 or pH under 7.20)",
  "Referral to a single ECMO center for consideration of ECMO",
  "Continued conventional management at the referring hospital",
  "Death or severe disability at 6 months",
  "pos","Survival without severe disability at 6 months 63% with referral vs 47% with conventional care (relative risk of death or disability 0.69).",
  "Transfer to an experienced ECMO center helped. Only 75% of the referred patients actually received ECMO, so the trial tested the center as much as the machine.")

T("eolia","EOLIA","N Engl J Med",2018,"Extracorporeal membrane oxygenation for severe acute respiratory distress syndrome","Critical care",
  "249 adults with very severe ARDS despite optimized ventilation",
  "Early venovenous ECMO",
  "Conventional lung-protective ventilation, with rescue ECMO allowed",
  "60-day mortality",
  "neu","60-day mortality 35% vs 46% (relative risk 0.76, P=0.09). 28% of controls crossed over to rescue ECMO.",
  "Not statistically significant, but the trend and heavy crossover keep ECMO in play for very severe ARDS at expert centers.")

T("oscillate","OSCILLATE","N Engl J Med",2013,"High-frequency oscillation in early acute respiratory distress syndrome","Critical care",
  "548 adults with early moderate-to-severe ARDS",
  "Early high-frequency oscillatory ventilation (HFOV)",
  "Conventional low tidal volume ventilation with high PEEP",
  "In-hospital mortality",
  "neg","In-hospital mortality 47% with HFOV vs 35% with conventional ventilation. The trial stopped early.",
  "Early routine HFOV increases mortality in ARDS and needed more sedatives, paralytics, and vasopressors. It is no longer a first-line strategy.")

T("oscar","OSCAR","N Engl J Med",2013,"High-frequency oscillation for acute respiratory distress syndrome","Critical care",
  "795 adults with ARDS (PaO2/FiO2 200 or less)",
  "High-frequency oscillatory ventilation",
  "Usual ventilatory care",
  "30-day all-cause mortality",
  "neu","30-day mortality 41.7% vs 41.1%.",
  "HFOV gave no survival benefit. Together with OSCILLATE, it ended routine oscillation for adult ARDS.")

T("art","ART","JAMA",2017,"Effect of Lung Recruitment and Titrated Positive End-Expiratory Pressure (PEEP) vs Low PEEP on Mortality in Patients With Acute Respiratory Distress Syndrome","Critical care",
  "1010 adults with moderate-to-severe ARDS",
  "Stepwise lung recruitment maneuver plus PEEP titrated to best compliance",
  "Low PEEP strategy (ARDSNet table)",
  "28-day all-cause mortality",
  "neg","28-day mortality 55.3% with recruitment vs 49.3% (hazard ratio 1.20).",
  "Aggressive recruitment maneuvers with titrated PEEP increased death. Avoid routine high-pressure recruitment in ARDS.")

T("alveoli","ALVEOLI","N Engl J Med",2004,"Higher versus lower positive end-expiratory pressures in patients with the acute respiratory distress syndrome","Critical care",
  "549 adults with acute lung injury or ARDS on 6 mL/kg tidal volumes",
  "Higher PEEP/FiO2 table",
  "Lower PEEP/FiO2 table",
  "Death before discharge home breathing without assistance",
  "neu","Mortality 24.9% with lower PEEP vs 27.5% with higher PEEP.",
  "Once tidal volumes are low, routinely pushing PEEP higher did not change survival.")

T("factt-fluids","FACTT (fluids)","N Engl J Med",2006,"Comparison of two fluid-management strategies in acute lung injury","Critical care",
  "1000 adults with acute lung injury, after shock had resolved",
  "Conservative fluid strategy (diuresis guided by CVP or wedge pressure)",
  "Liberal fluid strategy",
  "60-day mortality",
  "neu","60-day mortality 25.5% conservative vs 28.4% liberal. Ventilator-free days were higher with the conservative strategy (14.6 vs 12.1).",
  "Survival did not change, but a dry-side strategy after shock resolves gets patients off the ventilator sooner without more kidney injury.")

T("factt-pac","FACTT (catheter)","N Engl J Med",2006,"Pulmonary-artery versus central venous catheter to guide treatment of acute lung injury","Critical care",
  "1000 adults with acute lung injury",
  "Pulmonary artery catheter to guide fluid and hemodynamic management",
  "Central venous catheter",
  "60-day mortality",
  "neu","60-day mortality 27.4% with the PA catheter vs 26.3% with the CVC. PA catheters caused about twice as many catheter-related complications.",
  "Routine PA catheters do not improve outcomes in acute lung injury.")

T("lasrs","LaSRS","N Engl J Med",2006,"Efficacy and safety of corticosteroids for persistent acute respiratory distress syndrome","Critical care",
  "180 adults with ARDS persisting at least 7 days",
  "Methylprednisolone",
  "Placebo",
  "60-day mortality",
  "neu","60-day mortality 29.2% steroids vs 28.6% placebo. Starting steroids 14 or more days after ARDS onset raised mortality.",
  "Late steroids for persistent ARDS did not help survival and may harm when started after two weeks.")

T("nice-sugar","NICE-SUGAR","N Engl J Med",2009,"Intensive versus conventional glucose control in critically ill patients","Critical care",
  "6104 ICU adults expected to stay 3 or more days",
  "Intensive glucose control, target 81 to 108 mg/dL",
  "Conventional control, target 180 mg/dL or less",
  "90-day all-cause mortality",
  "neg","90-day mortality 27.5% intensive vs 24.9% conventional (odds ratio 1.14). Severe hypoglycemia 6.8% vs 0.5%.",
  "Tight glucose targets kill in the ICU. Aim for about 140 to 180 mg/dL.")

T("leuven-1","Leuven I","N Engl J Med",2001,"Intensive insulin therapy in critically ill patients","Critical care",
  "1548 ventilated adults in a surgical ICU, mostly after cardiac surgery",
  "Intensive insulin, glucose 80 to 110 mg/dL",
  "Conventional insulin only when glucose exceeded 215 mg/dL",
  "ICU mortality",
  "pos","ICU mortality 4.6% intensive vs 8.0% conventional.",
  "A single-center trial with heavy IV glucose feeding. It launched tight glucose control, which the much larger NICE-SUGAR later reversed.")

T("rivers","Rivers EGDT","N Engl J Med",2001,"Early goal-directed therapy in the treatment of severe sepsis and septic shock","Critical care",
  "263 ED adults with severe sepsis or septic shock",
  "6 hours of early goal-directed therapy targeting CVP, MAP, and central venous O2 saturation of 70% or more",
  "Standard care",
  "In-hospital mortality",
  "pos","In-hospital mortality 30.5% EGDT vs 46.5% standard care.",
  "Single center, very high control mortality. It shaped sepsis care for a decade until ProCESS, ARISE, and ProMISe found no benefit of the protocol over modern usual care.")

T("process","ProCESS","N Engl J Med",2014,"A randomized trial of protocol-based care for early septic shock","Critical care",
  "1341 ED adults with septic shock",
  "Protocolized EGDT, or a less aggressive protocol-based standard therapy",
  "Usual care",
  "60-day in-hospital mortality",
  "neu","60-day mortality 21.0% EGDT, 18.2% protocol-based standard therapy, 18.9% usual care.",
  "Once early antibiotics and fluids became routine, rigid EGDT protocols added nothing.")

T("arise","ARISE","N Engl J Med",2014,"Goal-directed resuscitation for patients with early septic shock","Critical care",
  "1600 ED adults with early septic shock in Australia and New Zealand",
  "Early goal-directed therapy",
  "Usual care",
  "90-day all-cause mortality",
  "neu","90-day mortality 18.6% EGDT vs 18.8% usual care.",
  "EGDT did not reduce death, confirming ProCESS.")

T("promise","ProMISe","N Engl J Med",2015,"Trial of early, goal-directed resuscitation for septic shock","Critical care",
  "1260 ED adults with early septic shock in England",
  "6 hours of early goal-directed therapy",
  "Usual care",
  "90-day all-cause mortality",
  "neu","90-day mortality 29.5% EGDT vs 29.2% usual care. EGDT cost more.",
  "The third negative trial of EGDT. Protocolized ScvO2-guided resuscitation is not needed.")

T("annane-2002","Annane hydrocortisone-fludrocortisone","JAMA",2002,"Effect of treatment with low doses of hydrocortisone and fludrocortisone on mortality in patients with septic shock","Critical care",
  "300 adults with vasopressor-dependent septic shock",
  "Hydrocortisone 50 mg IV every 6 hours plus fludrocortisone 50 mcg daily for 7 days",
  "Placebo",
  "28-day mortality in patients who failed a corticotropin stimulation test",
  "pos","In corticotropin nonresponders, 28-day mortality 53% steroids vs 63% placebo (hazard ratio 0.67).",
  "Low-dose steroids helped refractory septic shock. The corticotropin test is no longer used to select patients.")

T("corticus","CORTICUS","N Engl J Med",2008,"Hydrocortisone therapy for patients with septic shock","Critical care",
  "499 adults with septic shock, many not on high-dose vasopressors",
  "Hydrocortisone 50 mg IV every 6 hours for 5 days, then taper",
  "Placebo",
  "28-day mortality in corticotropin nonresponders",
  "neu","28-day mortality in nonresponders 39.2% hydrocortisone vs 36.1% placebo. Shock reversed faster with hydrocortisone.",
  "Hydrocortisone speeds shock reversal but did not reduce death in this less-sick population.")

T("adrenal","ADRENAL","N Engl J Med",2018,"Adjunctive glucocorticoid therapy in patients with septic shock","Critical care",
  "3800 ventilated adults with septic shock",
  "Hydrocortisone 200 mg/day continuous infusion for 7 days",
  "Placebo",
  "90-day all-cause mortality",
  "neu","90-day mortality 27.9% hydrocortisone vs 28.8% placebo. Shock resolved faster and ventilation was shorter.",
  "Hydrocortisone shortens shock and ventilation without changing survival. Use it for patients on escalating vasopressors.")

T("aprocchss","APROCCHSS","N Engl J Med",2018,"Hydrocortisone plus fludrocortisone for adults with septic shock","Critical care",
  "1241 adults with septic shock",
  "Hydrocortisone 50 mg IV every 6 hours plus fludrocortisone 50 mcg daily for 7 days",
  "Placebo",
  "90-day all-cause mortality",
  "pos","90-day mortality 43.0% steroids vs 49.1% placebo.",
  "In sicker septic shock, hydrocortisone plus fludrocortisone lowered mortality. Some use this regimen, others hydrocortisone alone, based on ADRENAL.")

T("vasst","VASST","N Engl J Med",2008,"Vasopressin versus norepinephrine infusion in patients with septic shock","Critical care",
  "778 adults with septic shock on at least 5 mcg/min of norepinephrine",
  "Low-dose vasopressin (0.01 to 0.03 U/min) added to open-label vasopressors",
  "Norepinephrine added to open-label vasopressors",
  "28-day mortality",
  "neu","28-day mortality 35.4% vasopressin vs 39.3% norepinephrine.",
  "Vasopressin is a reasonable second agent to spare norepinephrine, but it does not lower mortality.")

T("soap-2","SOAP II","N Engl J Med",2010,"Comparison of dopamine and norepinephrine in the treatment of shock","Critical care",
  "1679 adults with shock of any cause",
  "Dopamine as the first vasopressor",
  "Norepinephrine as the first vasopressor",
  "28-day mortality",
  "neu","28-day mortality 52.5% dopamine vs 48.5% norepinephrine (not significant). Arrhythmias 24.1% vs 12.4%. Cardiogenic shock subgroup did worse with dopamine.",
  "No overall mortality difference, but dopamine caused twice the arrhythmias. Norepinephrine is the first-line vasopressor.")

T("vanish","VANISH","JAMA",2016,"Effect of Early Vasopressin vs Norepinephrine on Kidney Failure in Patients With Septic Shock","Critical care",
  "409 adults with septic shock",
  "Early vasopressin (with hydrocortisone or placebo in a factorial design)",
  "Norepinephrine",
  "Kidney failure-free days during the 28 days after randomization",
  "neu","No difference in kidney failure-free days. Vasopressin patients needed less renal replacement therapy, a secondary finding.",
  "Early vasopressin does not protect the kidneys enough to change the primary outcome.")

T("athos-3","ATHOS-3","N Engl J Med",2017,"Angiotensin II for the treatment of vasodilatory shock","Critical care",
  "344 adults with vasodilatory shock on high-dose vasopressors",
  "Synthetic human angiotensin II infusion",
  "Placebo",
  "MAP response at hour 3 (MAP 75 or more, or a rise of 10 or more)",
  "pos","MAP response 69.9% angiotensin II vs 23.4% placebo.",
  "Angiotensin II raises blood pressure in catecholamine-resistant shock. The trial was not powered for mortality.")

T("sepsispam","SEPSISPAM","N Engl J Med",2014,"High versus low blood-pressure target in patients with septic shock","Critical care",
  "776 adults with septic shock",
  "MAP target 80 to 85 mm Hg",
  "MAP target 65 to 70 mm Hg",
  "28-day mortality",
  "neu","28-day mortality 36.6% high target vs 34.0% low target. More new atrial fibrillation with the high target.",
  "A MAP of 65 is enough for most. Patients with chronic hypertension needed less dialysis at the higher target.")

T("sixty-five","65 trial","JAMA",2020,"Effect of Reduced Exposure to Vasopressors on 90-Day Mortality in Older Critically Ill Patients With Vasodilatory Hypotension","Critical care",
  "2600 ICU patients aged 65 or older with vasodilatory hypotension",
  "Permissive hypotension, MAP target 60 to 65 mm Hg",
  "Usual care MAP targets",
  "90-day all-cause mortality",
  "neu","90-day mortality 41.0% permissive vs 43.8% usual care (not significant).",
  "In older adults, lower MAP targets were safe and reduced vasopressor exposure, without changing mortality.")

T("safe","SAFE","N Engl J Med",2004,"A comparison of albumin and saline for fluid resuscitation in the intensive care unit","Critical care",
  "6997 ICU adults needing fluid resuscitation",
  "4% albumin",
  "0.9% saline",
  "28-day all-cause mortality",
  "neu","Deaths 726 with albumin vs 729 with saline (relative risk 0.99). Traumatic brain injury patients did worse with albumin in a subgroup analysis.",
  "Albumin and saline are equivalent for general ICU resuscitation. Avoid albumin in traumatic brain injury.")

T("albios","ALBIOS","N Engl J Med",2014,"Albumin replacement in patients with severe sepsis or septic shock","Critical care",
  "1818 adults with severe sepsis or septic shock",
  "20% albumin to keep serum albumin at 3.0 g/dL or more, plus crystalloids",
  "Crystalloids alone",
  "28-day mortality",
  "neu","28-day mortality 31.8% albumin vs 32.0% crystalloid.",
  "Albumin replacement does not improve survival in sepsis.")

T("6s","6S","N Engl J Med",2012,"Hydroxyethyl starch 130/0.42 versus Ringer's acetate in severe sepsis","Critical care",
  "798 adults with severe sepsis",
  "6% hydroxyethyl starch 130/0.42",
  "Ringer's acetate",
  "Death or dependence on dialysis at 90 days",
  "neg","Death at 90 days 51% with starch vs 43% with Ringer's (relative risk 1.17). More dialysis with starch.",
  "Hydroxyethyl starch increases death and kidney injury in sepsis. Do not use it.")

T("chest-hes","CHEST","N Engl J Med",2012,"Hydroxyethyl starch or saline for fluid resuscitation in intensive care","Critical care",
  "7000 ICU adults needing fluid resuscitation",
  "6% hydroxyethyl starch 130/0.4",
  "0.9% saline",
  "90-day all-cause mortality",
  "neu","90-day mortality 18.0% starch vs 17.0% saline. More renal replacement therapy with starch (7.0% vs 5.8%).",
  "No survival benefit, more kidney harm. Together with 6S, this led regulators to restrict starches.")

T("smart","SMART","N Engl J Med",2018,"Balanced crystalloids versus saline in critically ill adults","Critical care",
  "15802 adults in five ICUs (cluster-crossover)",
  "Balanced crystalloids (lactated Ringer's or Plasma-Lyte A)",
  "0.9% saline",
  "Major adverse kidney events within 30 days (MAKE30): death, new dialysis, or persistent kidney dysfunction",
  "pos","MAKE30 14.3% balanced vs 15.4% saline (odds ratio 0.91).",
  "A small absolute benefit that adds up across millions of patients. Many ICUs now default to balanced crystalloids.")

T("basics","BaSICS","JAMA",2021,"Effect of Intravenous Fluid Treatment With a Balanced Solution vs 0.9% Saline Solution on Mortality in Critically Ill Patients","Critical care",
  "11052 ICU adults in Brazil",
  "Balanced solution (Plasma-Lyte 148)",
  "0.9% saline",
  "90-day mortality",
  "neu","90-day mortality 26.4% balanced vs 27.2% saline.",
  "No mortality difference. Traumatic brain injury patients may do worse with balanced solutions, which are hypotonic.")

T("plus","PLUS","N Engl J Med",2022,"Balanced Multielectrolyte Solution versus Saline in Critically Ill Adults","Critical care",
  "5037 ICU adults in Australia and New Zealand",
  "Balanced multielectrolyte solution (Plasma-Lyte 148)",
  "0.9% saline",
  "90-day all-cause mortality",
  "neu","90-day mortality 21.8% balanced vs 22.0% saline.",
  "Either fluid is acceptable for most ICU patients. Pooled data slightly favor balanced solutions.")

T("clovers","CLOVERS","N Engl J Med",2023,"Early Restrictive or Liberal Fluid Management for Sepsis-Induced Hypotension","Critical care",
  "1563 adults with sepsis-induced hypotension after 1 to 3 L of fluid",
  "Restrictive fluids with early vasopressors",
  "Liberal fluids with later vasopressors",
  "Death from any cause before discharge home by day 90",
  "neu","Mortality 14.0% restrictive vs 14.9% liberal.",
  "After initial resuscitation, an early-vasopressor approach is as safe as giving more fluid. Individualize.")

T("classic","CLASSIC","N Engl J Med",2022,"Restriction of Intravenous Fluid in ICU Patients with Septic Shock","Critical care",
  "1554 ICU adults with septic shock",
  "Restrictive IV fluids (only for severe hypoperfusion or losses)",
  "Standard IV fluid therapy",
  "90-day all-cause mortality",
  "neu","90-day mortality 42.3% restrictive vs 42.1% standard.",
  "Restricting fluid after ICU admission did not change survival or serious adverse events.")

T("feast","FEAST","N Engl J Med",2011,"Mortality after fluid bolus in African children with severe infection","Critical care",
  "3141 febrile children in East Africa with impaired perfusion",
  "Fluid bolus of 5% albumin or 0.9% saline (20 to 40 mL/kg)",
  "No bolus (maintenance fluids only)",
  "48-hour mortality",
  "neg","48-hour mortality 10.6% albumin bolus, 10.5% saline bolus, 7.3% no bolus. The trial stopped early for harm.",
  "In settings without ICU support, fluid boluses killed febrile children. Fluids are a drug with real harms.")

T("tricc","TRICC","N Engl J Med",1999,"A multicenter, randomized, controlled clinical trial of transfusion requirements in critical care","Critical care",
  "838 euvolemic ICU adults with hemoglobin under 9 g/dL",
  "Restrictive transfusion, threshold 7 g/dL (target 7 to 9)",
  "Liberal transfusion, threshold 10 g/dL (target 10 to 12)",
  "30-day all-cause mortality",
  "neu","30-day mortality 18.7% restrictive vs 23.3% liberal (P=0.11).",
  "Restrictive transfusion is at least as safe and uses far less blood. It made 7 g/dL the standard ICU threshold.")

T("triss","TRISS","N Engl J Med",2014,"Lower versus higher hemoglobin threshold for transfusion in septic shock","Critical care",
  "1005 ICU adults with septic shock",
  "Transfuse at hemoglobin 7 g/dL or less",
  "Transfuse at hemoglobin 9 g/dL or less",
  "90-day mortality",
  "neu","90-day mortality 43.0% lower threshold vs 45.0% higher threshold.",
  "A 7 g/dL threshold is safe in septic shock and halves blood use.")

T("prowess","PROWESS","N Engl J Med",2001,"Efficacy and safety of recombinant human activated protein C for severe sepsis","Critical care",
  "1690 adults with severe sepsis",
  "Drotrecogin alfa (activated protein C) for 96 hours",
  "Placebo",
  "28-day all-cause mortality",
  "pos","28-day mortality 24.7% drotrecogin vs 30.8% placebo. More serious bleeding.",
  "Approved on this trial alone, then withdrawn after PROWESS-SHOCK failed to confirm it. A lesson in replication.")

T("prowess-shock","PROWESS-SHOCK","N Engl J Med",2012,"Drotrecogin alfa (activated) in adults with septic shock","Critical care",
  "1697 adults with septic shock",
  "Drotrecogin alfa (activated protein C)",
  "Placebo",
  "28-day all-cause mortality",
  "neu","28-day mortality 26.4% drotrecogin vs 24.2% placebo.",
  "No benefit. The drug was withdrawn from the market worldwide.")

T("lovit","LOVIT","N Engl J Med",2022,"Intravenous Vitamin C in Adults with Sepsis in the Intensive Care Unit","Critical care",
  "872 ICU adults with sepsis on vasopressors",
  "IV vitamin C 50 mg/kg every 6 hours for up to 4 days",
  "Placebo",
  "Death or persistent organ dysfunction at day 28",
  "neg","Death or persistent organ dysfunction 44.5% vitamin C vs 38.5% placebo (risk ratio 1.21).",
  "High-dose IV vitamin C caused harm in sepsis. Do not give it outside a trial.")

T("vitamins","VITAMINS","JAMA",2020,"Effect of Vitamin C, Hydrocortisone, and Thiamine vs Hydrocortisone Alone on Time Alive and Free of Vasopressor Support Among Patients With Septic Shock","Critical care",
  "216 adults with septic shock",
  "IV vitamin C, hydrocortisone, and thiamine",
  "Hydrocortisone alone",
  "Time alive and free of vasopressors at day 7",
  "neu","No difference in vasopressor-free time (122.1 vs 124.6 hours).",
  "The HAT cocktail did not hold up in a randomized trial.")

T("takala-gh","Growth hormone in critical illness","N Engl J Med",1999,"Increased mortality associated with growth hormone treatment in critically ill adults","Critical care",
  "532 adults with prolonged critical illness after surgery, trauma, or respiratory failure (two parallel trials)",
  "High-dose recombinant growth hormone",
  "Placebo",
  "Length of ICU and hospital stay; mortality",
  "neg","In-hospital mortality 44% vs 18% in the Finnish trial and 39% vs 20% in the multinational trial.",
  "An anabolic idea that roughly doubled death. Biologic plausibility is not proof.")

T("balti-2","BALTI-2","Lancet",2012,"Effect of intravenous beta-2 agonist treatment on clinical outcomes in acute respiratory distress syndrome (BALTI-2)","Critical care",
  "326 ventilated adults with ARDS",
  "IV salbutamol (albuterol) for up to 7 days",
  "Placebo",
  "28-day mortality",
  "neg","28-day mortality 34% salbutamol vs 23% placebo. The trial stopped early for harm.",
  "IV beta-agonists to clear lung edema in ARDS caused harm, mostly from arrhythmias and tachycardia.")

T("sails","SAILS","N Engl J Med",2014,"Rosuvastatin for sepsis-associated acute respiratory distress syndrome","Critical care",
  "745 adults with sepsis-associated ARDS",
  "Rosuvastatin",
  "Placebo",
  "In-hospital mortality before discharge home or day 60",
  "neu","Mortality 28.5% rosuvastatin vs 24.9% placebo. Stopped for futility.",
  "Statins do not treat ARDS.")

T("ttm","TTM","N Engl J Med",2013,"Targeted temperature management at 33°C versus 36°C after cardiac arrest","Critical care",
  "950 unconscious adults after out-of-hospital cardiac arrest of presumed cardiac cause",
  "Targeted temperature 33°C",
  "Targeted temperature 36°C",
  "All-cause mortality through end of trial",
  "neu","Mortality 50% at 33°C vs 48% at 36°C.",
  "33°C was no better than 36°C. Strict fever prevention is what matters.")

T("ttm2","TTM2","N Engl J Med",2021,"Hypothermia versus Normothermia after Out-of-Hospital Cardiac Arrest","Critical care",
  "1900 comatose adults after out-of-hospital cardiac arrest",
  "Hypothermia to 33°C, then rewarming",
  "Normothermia with early treatment of fever (37.8°C or above)",
  "6-month all-cause mortality",
  "neu","6-month mortality 50% hypothermia vs 48% normothermia. More arrhythmias with hypothermia.",
  "Active fever prevention is enough for most out-of-hospital arrest survivors.")

T("haca","HACA","N Engl J Med",2002,"Mild therapeutic hypothermia to improve the neurologic outcome after cardiac arrest","Critical care",
  "275 adults resuscitated from VF or pulseless VT arrest",
  "Cooling to 32 to 34°C for 24 hours",
  "Normothermia (no temperature control)",
  "Favorable neurologic outcome at 6 months",
  "pos","Favorable neurologic outcome 55% hypothermia vs 39% normothermia.",
  "This trial and a companion Australian trial launched therapeutic hypothermia. Its control arm let fevers run, which later trials controlled.")

T("hyperion","HYPERION","N Engl J Med",2019,"Targeted Temperature Management for Cardiac Arrest with Nonshockable Rhythm","Critical care",
  "584 comatose adults after cardiac arrest with a nonshockable rhythm",
  "Hypothermia at 33°C",
  "Targeted normothermia at 37°C",
  "Survival with good neurologic outcome (CPC 1 or 2) at day 90",
  "pos","Good neurologic outcome 10.2% at 33°C vs 5.7% at 37°C.",
  "A small absolute gain with a fragile result. TTM2 later found no benefit in a broader population.")

T("paramedic2","PARAMEDIC2","N Engl J Med",2018,"A Randomized Trial of Epinephrine in Out-of-Hospital Cardiac Arrest","Critical care",
  "8014 adults with out-of-hospital cardiac arrest",
  "Epinephrine",
  "Placebo",
  "30-day survival",
  "pos","30-day survival 3.2% epinephrine vs 2.4% placebo. Favorable neurologic outcome did not differ (2.2% vs 1.9%), and more epinephrine survivors had severe brain injury.",
  "Epinephrine restarts more hearts and slightly improves survival, but not good neurologic survival.")

T("coact","COACT","N Engl J Med",2019,"Coronary Angiography after Cardiac Arrest without ST-Segment Elevation","Critical care",
  "552 adults resuscitated from shockable out-of-hospital arrest without ST elevation",
  "Immediate coronary angiography",
  "Delayed angiography after neurologic recovery",
  "90-day survival",
  "neu","90-day survival 64.5% immediate vs 67.2% delayed.",
  "Without ST elevation, rushing to the cath lab after arrest does not improve survival.")

T("arrest-ecpr","ARREST","Lancet",2020,"Advanced reperfusion strategies for patients with out-of-hospital cardiac arrest and refractory ventricular fibrillation (ARREST)","Critical care",
  "30 adults with out-of-hospital cardiac arrest and refractory VF",
  "Early ECMO-facilitated resuscitation (ECPR)",
  "Standard ACLS",
  "Survival to hospital discharge",
  "pos","Survival to discharge 43% ECPR vs 7% standard ACLS. Stopped early after 30 patients.",
  "Dramatic benefit in a tiny, single-center trial with an expert team. INCEPTION, a larger multicenter trial, did not confirm it.")

T("inception","INCEPTION","N Engl J Med",2023,"Extracorporeal Cardiopulmonary Resuscitation for Refractory Out-of-Hospital Cardiac Arrest","Critical care",
  "134 adults with refractory out-of-hospital VF arrest in 10 Dutch centers",
  "Extracorporeal CPR (ECPR)",
  "Conventional CPR",
  "30-day survival with favorable neurologic outcome",
  "neu","Favorable 30-day survival 20% ECPR vs 16% conventional CPR.",
  "Across many centers, ECPR did not clearly help. Results depend on systems and speed.")

T("florali","FLORALI","N Engl J Med",2015,"High-flow oxygen through nasal cannula in acute hypoxemic respiratory failure","Critical care",
  "310 adults with non-hypercapnic acute hypoxemic respiratory failure",
  "High-flow nasal oxygen",
  "Standard face-mask oxygen, or noninvasive ventilation",
  "Intubation within 28 days",
  "neu","Intubation 38% high-flow, 47% standard oxygen, 50% NIV (P=0.18). 90-day mortality was lower with high-flow, a secondary outcome.",
  "The primary outcome missed, but high-flow nasal oxygen became first-line for hypoxemic respiratory failure.")

T("brochard-niv","Brochard NIV in COPD","N Engl J Med",1995,"Noninvasive ventilation for acute exacerbations of chronic obstructive pulmonary disease","Critical care",
  "85 adults with acute hypercapnic COPD exacerbation",
  "Noninvasive pressure-support ventilation by face mask",
  "Standard medical therapy",
  "Need for endotracheal intubation",
  "pos","Intubation 26% NIV vs 74% standard therapy. In-hospital mortality also fell.",
  "NIV is first-line for hypercapnic COPD exacerbations.")

T("helmet-niv","Helmet NIV","JAMA",2016,"Effect of Noninvasive Ventilation Delivered by Helmet vs Face Mask on the Rate of Endotracheal Intubation in Patients With Acute Respiratory Distress Syndrome","Critical care",
  "83 adults with ARDS on face-mask NIV for at least 8 hours",
  "NIV delivered by helmet",
  "NIV by face mask",
  "Endotracheal intubation",
  "pos","Intubation 18.2% helmet vs 61.5% face mask. Stopped early for efficacy.",
  "Helmet NIV is a promising option for hypoxemic failure, though data are from a small single-center trial.")

T("prevent-bmv","PreVent","N Engl J Med",2019,"Bag-Mask Ventilation during Tracheal Intubation of Critically Ill Adults","Critical care",
  "401 ICU adults undergoing tracheal intubation",
  "Bag-mask ventilation between induction and laryngoscopy",
  "No ventilation between induction and laryngoscopy",
  "Lowest oxygen saturation (severe hypoxemia SpO2 under 80% as a key secondary)",
  "pos","Higher lowest saturation with bag-mask ventilation. Severe hypoxemia 10.9% vs 22.8%. No increase in aspiration.",
  "Gentle bag-mask ventilation after induction prevents desaturation without more aspiration.")

T("device","DEVICE","N Engl J Med",2023,"Video versus Direct Laryngoscopy for Tracheal Intubation of Critically Ill Adults","Critical care",
  "1417 adults intubated in the ED or ICU",
  "Video laryngoscope",
  "Direct laryngoscope",
  "Successful intubation on the first attempt",
  "pos","First-attempt success 85.1% video vs 70.8% direct.",
  "Video laryngoscopy should be the default for emergency intubation of critically ill adults.")

T("preoxi","PREOXI","N Engl J Med",2024,"Noninvasive Ventilation for Preoxygenation during Emergency Intubation","Critical care",
  "1301 critically ill adults undergoing emergency intubation",
  "Preoxygenation with noninvasive ventilation",
  "Preoxygenation with an oxygen mask",
  "Hypoxemia (SpO2 under 85%) between induction and 2 minutes after intubation",
  "pos","Hypoxemia 9.1% NIV vs 18.5% oxygen mask. Cardiac arrest during intubation 0.2% vs 1.1%.",
  "Preoxygenate with NIV before emergency intubation when you can.")

T("bougie","BOUGIE","JAMA",2021,"Effect of Use of a Bougie vs Endotracheal Tube With Stylet on Successful Intubation on the First Attempt Among Critically Ill Adults","Critical care",
  "1106 critically ill adults intubated in the ED or ICU",
  "Bougie",
  "Endotracheal tube with stylet",
  "First-attempt success",
  "neu","First-attempt success 80.4% bougie vs 83.0% stylet.",
  "Routine bougie use did not improve first-pass success in critically ill adults.")

T("kress-sat","Daily sedation interruption","N Engl J Med",2000,"Daily interruption of sedative infusions in critically ill patients undergoing mechanical ventilation","Critical care",
  "128 ventilated adults on continuous sedative infusions",
  "Daily interruption of sedation until awake",
  "Sedation interrupted only at the clinicians' discretion",
  "Duration of mechanical ventilation",
  "pos","Median ventilation 4.9 days with daily interruption vs 7.3 days.",
  "Wake patients up every day. It shortens ventilation and ICU stay.")

T("abc","ABC","Lancet",2008,"Efficacy and safety of a paired sedation and ventilator weaning protocol for mechanically ventilated patients in intensive care (Awakening and Breathing Controlled trial)","Critical care",
  "336 ventilated ICU adults",
  "Daily spontaneous awakening trial paired with a spontaneous breathing trial",
  "Spontaneous breathing trial with usual sedation",
  "Ventilator-free breathing days",
  "pos","Ventilator-free days 14.7 vs 11.6. One-year mortality also fell (hazard ratio 0.68).",
  "Pair the sedation vacation with the breathing trial. Wake up and breathe.")

T("schweickert","Early mobilization","Lancet",2009,"Early physical and occupational therapy in mechanically ventilated, critically ill patients","Critical care",
  "104 sedated, ventilated adults who were independent at baseline",
  "Early physical and occupational therapy during daily sedation interruption",
  "Usual therapy as ordered by the primary team",
  "Return to independent functional status at hospital discharge",
  "pos","Independent at discharge 59% early therapy vs 35% control.",
  "Early mobilization is safe and improves function. TEAM later found no benefit of an even more intense approach.")

T("team","TEAM","N Engl J Med",2022,"Early Active Mobilization during Mechanical Ventilation in the ICU","Critical care",
  "750 ventilated ICU adults",
  "Early, high-intensity active mobilization",
  "Usual mobilization",
  "Days alive and out of hospital at day 180",
  "neu","Days alive out of hospital 143 vs 145. More adverse events with early active mobilization.",
  "Pushing mobilization harder did not help and caused more adverse events.")

T("spice-3","SPICE III","N Engl J Med",2019,"Early Sedation with Dexmedetomidine in Critically Ill Patients","Critical care",
  "4000 ventilated ICU adults",
  "Early dexmedetomidine as the primary sedative",
  "Usual care sedation (mostly propofol or midazolam)",
  "90-day all-cause mortality",
  "neu","90-day mortality 29.1% in both groups. More bradycardia and hypotension with dexmedetomidine.",
  "Dexmedetomidine as primary sedation does not save lives.")

T("mind-usa","MIND-USA","N Engl J Med",2018,"Haloperidol and Ziprasidone for Treatment of Delirium in Critical Illness","Critical care",
  "566 ICU adults with delirium",
  "IV haloperidol or ziprasidone",
  "Placebo",
  "Days alive without delirium or coma over 14 days",
  "neu","Median days alive without delirium or coma 7.9 haloperidol, 8.7 ziprasidone, 8.5 placebo.",
  "Antipsychotics do not shorten ICU delirium.")

T("aid-icu","AID-ICU","N Engl J Med",2022,"Haloperidol for the Treatment of Delirium in ICU Patients","Critical care",
  "1000 ICU adults with delirium",
  "IV haloperidol",
  "Placebo",
  "Days alive and out of hospital at 90 days",
  "neu","Days alive out of hospital 35.8 haloperidol vs 32.9 placebo (not significant).",
  "Haloperidol did not significantly improve outcomes in ICU delirium.")

T("epanic","EPaNIC","N Engl J Med",2011,"Early versus late parenteral nutrition in critically ill adults","Critical care",
  "4640 ICU adults at nutritional risk",
  "Late parenteral nutrition (withhold PN until day 8)",
  "Early parenteral nutrition (start within 48 hours)",
  "Duration of ICU stay",
  "pos","Late PN patients left the ICU alive sooner, with fewer infections and shorter ventilation.",
  "Do not rush parenteral nutrition in the first week of critical illness.")

T("calories","CALORIES","N Engl J Med",2014,"Trial of the route of early nutritional support in critically ill adults","Critical care",
  "2400 ICU adults needing nutrition",
  "Early parenteral nutrition",
  "Early enteral nutrition",
  "30-day all-cause mortality",
  "neu","30-day mortality 33.1% parenteral vs 34.2% enteral.",
  "The route of early nutrition did not change survival.")

T("eden","EDEN","JAMA",2012,"Initial trophic vs full enteral feeding in patients with acute lung injury","Critical care",
  "1000 adults with acute lung injury",
  "Trophic (low-volume) enteral feeding for 6 days",
  "Full enteral feeding",
  "Ventilator-free days to day 28",
  "neu","Ventilator-free days 14.9 trophic vs 15.0 full feeding.",
  "Trophic feeds for the first week are fine. You do not need to hit full calories early.")

T("tracman","TracMan","JAMA",2013,"Effect of early vs late tracheostomy placement on survival in patients receiving mechanical ventilation","Critical care",
  "909 ventilated adults expected to need at least 7 more days",
  "Early tracheostomy (within 4 days)",
  "Late tracheostomy (after 10 days, if still needed)",
  "30-day all-cause mortality",
  "neu","30-day mortality 30.8% early vs 31.5% late.",
  "Early tracheostomy does not improve survival. Most late-group patients never needed one.")

T("hot-icu","HOT-ICU","N Engl J Med",2021,"Lower or Higher Oxygenation Targets for Acute Hypoxemic Respiratory Failure","Critical care",
  "2928 ICU adults with acute hypoxemic respiratory failure",
  "Lower oxygenation target (PaO2 60 mm Hg)",
  "Higher oxygenation target (PaO2 90 mm Hg)",
  "90-day mortality",
  "neu","90-day mortality 42.9% lower target vs 42.4% higher target.",
  "Either target is acceptable. Avoid both hypoxemia and needless hyperoxia.")

T("icu-rox","ICU-ROX","N Engl J Med",2020,"Conservative Oxygen Therapy during Mechanical Ventilation in the ICU","Critical care",
  "1000 ventilated ICU adults",
  "Conservative oxygen therapy (avoid SpO2 above 97%)",
  "Usual oxygen therapy",
  "Ventilator-free days to day 28",
  "neu","Ventilator-free days 21.3 conservative vs 22.1 usual.",
  "Conservative oxygen did not change outcomes.")

T("starrt-aki","STARRT-AKI","N Engl J Med",2020,"Timing of Initiation of Renal-Replacement Therapy in Acute Kidney Injury","Critical care",
  "2927 ICU adults with severe AKI without urgent dialysis indications",
  "Accelerated renal replacement therapy (within 12 hours)",
  "Standard strategy (start only if indications developed or AKI persisted 72 hours)",
  "90-day all-cause mortality",
  "neu","90-day mortality 43.9% accelerated vs 43.7% standard. More dialysis dependence at 90 days with the accelerated strategy.",
  "Watchful waiting is safe. Many standard-arm patients never needed dialysis.")

T("akiki","AKIKI","N Engl J Med",2016,"Initiation Strategies for Renal-Replacement Therapy in the Intensive Care Unit","Critical care",
  "620 ICU adults with severe AKI on ventilation or vasopressors",
  "Early renal replacement therapy",
  "Delayed strategy (start only for urgent indications or prolonged oliguria)",
  "60-day mortality",
  "neu","60-day mortality 48.5% early vs 49.7% delayed. Half the delayed group never needed dialysis.",
  "Delaying dialysis until a clear indication appears is safe and avoids many treatments.")

T("atn","VA/NIH ATN","N Engl J Med",2008,"Intensity of renal support in critically ill patients with acute kidney injury","Critical care",
  "1124 critically ill adults with AKI",
  "Intensive renal support (CVVHDF 35 mL/kg/h or intermittent HD 6 times a week)",
  "Less intensive support (20 mL/kg/h or HD 3 times a week)",
  "60-day all-cause mortality",
  "neu","60-day mortality 53.6% intensive vs 51.5% less intensive.",
  "More dialysis dose is not better. About 20 to 25 mL/kg/h of delivered CRRT is enough.")

T("renal","RENAL","N Engl J Med",2009,"Intensity of continuous renal-replacement therapy in critically ill patients","Critical care",
  "1508 ICU adults with AKI",
  "Higher-intensity CRRT (40 mL/kg/h)",
  "Lower-intensity CRRT (25 mL/kg/h)",
  "90-day mortality",
  "neu","90-day mortality 44.7% in both groups.",
  "Higher CRRT intensity does not save lives, confirming ATN.")

T("anzics-dopamine","ANZICS low-dose dopamine","Lancet",2000,"Low-dose dopamine in patients with early renal dysfunction: a placebo-controlled randomised trial","Critical care",
  "328 ICU adults with SIRS and early renal dysfunction",
  "Low-dose ('renal-dose') dopamine 2 mcg/kg/min",
  "Placebo",
  "Peak serum creatinine during infusion",
  "neu","Peak creatinine 245 vs 249 µmol/L. No difference in dialysis need or survival.",
  "Renal-dose dopamine does not protect the kidneys. Stop using it.")

T("bicar-icu","BICAR-ICU","Lancet",2018,"Sodium bicarbonate therapy for patients with severe metabolic acidaemia in the intensive care unit (BICAR-ICU)","Critical care",
  "389 ICU adults with severe metabolic acidemia (pH 7.20 or less)",
  "IV 4.2% sodium bicarbonate to keep pH above 7.30",
  "No bicarbonate",
  "Death at day 28 or organ failure at day 7",
  "neu","Primary outcome 66% control vs 71% bicarbonate overall (not significant). In patients with AKI, bicarbonate lowered mortality and dialysis need.",
  "No overall benefit, but bicarbonate is reasonable for severe acidemia with AKI.")

T("andromeda","ANDROMEDA-SHOCK","JAMA",2019,"Effect of a Resuscitation Strategy Targeting Peripheral Perfusion Status vs Serum Lactate Levels on 28-Day Mortality Among Patients With Septic Shock","Critical care",
  "424 adults with early septic shock",
  "Resuscitation targeting capillary refill time",
  "Resuscitation targeting lactate normalization",
  "28-day all-cause mortality",
  "neu","28-day mortality 34.9% capillary refill vs 43.4% lactate (P=.06).",
  "Capillary refill time is a cheap, fast bedside target that did at least as well as chasing lactate.")

T("morelli-esmolol","Esmolol in septic shock","JAMA",2013,"Effect of heart rate control with esmolol on hemodynamic and clinical outcomes in patients with septic shock","Critical care",
  "154 adults with septic shock and heart rate 95 or more on norepinephrine",
  "Esmolol to keep heart rate 80 to 94",
  "Standard care",
  "Heart rate reduction to target",
  "pos","All esmolol patients reached the heart rate target. 28-day mortality 49.4% vs 80.5%, a secondary outcome.",
  "An intriguing single-center signal with an unusually high control mortality. Not standard care.")

T("leopards","LeoPARDS","N Engl J Med",2016,"Levosimendan for the Prevention of Acute Organ Dysfunction in Sepsis","Critical care",
  "516 adults with septic shock",
  "Levosimendan infusion",
  "Placebo",
  "Mean daily SOFA score in the ICU",
  "neu","No difference in mean SOFA score. More supraventricular tachyarrhythmias and less successful weaning from ventilation.",
  "Levosimendan does not prevent organ dysfunction in sepsis.")

T("pamper","PAMPer","N Engl J Med",2018,"Prehospital Plasma during Air Medical Transport in Trauma Patients at Risk for Hemorrhagic Shock","Critical care",
  "501 injured patients at risk of hemorrhagic shock during air transport",
  "2 units of thawed plasma before arrival",
  "Standard-care resuscitation",
  "30-day mortality",
  "pos","30-day mortality 23.2% plasma vs 33.0% standard care.",
  "Prehospital plasma saved lives when transport times were long.")

T("proppr","PROPPR","JAMA",2015,"Transfusion of plasma, platelets, and red blood cells in a 1:1:1 vs a 1:1:2 ratio and mortality in patients with severe trauma","Critical care",
  "680 severely injured adults predicted to need massive transfusion",
  "Plasma:platelets:red cells 1:1:1",
  "Plasma:platelets:red cells 1:1:2",
  "24-hour and 30-day mortality",
  "neu","24-hour mortality 12.7% vs 17.0%; 30-day mortality 22.4% vs 26.1%. Neither was significant. Fewer exsanguination deaths at 24 hours with 1:1:1.",
  "Balanced 1:1:1 resuscitation achieved hemostasis more often, without a significant overall survival difference.")

T("crash-2","CRASH-2","Lancet",2010,"Effects of tranexamic acid on death, vascular occlusive events, and blood transfusion in trauma patients with significant haemorrhage (CRASH-2)","Critical care",
  "20211 adult trauma patients with or at risk of significant bleeding",
  "Tranexamic acid 1 g over 10 minutes then 1 g over 8 hours",
  "Placebo",
  "In-hospital death within 4 weeks",
  "pos","All-cause mortality 14.5% TXA vs 16.0% placebo.",
  "Give tranexamic acid early in bleeding trauma, ideally within 3 hours of injury.")

T("crash","CRASH","Lancet",2004,"Effect of intravenous corticosteroids on death within 14 days in 10008 adults with clinically significant head injury","Critical care",
  "10008 adults with head injury and GCS 14 or less",
  "IV methylprednisolone for 48 hours",
  "Placebo",
  "Death within 14 days",
  "neg","Death within 14 days 21.1% steroids vs 17.9% placebo (relative risk 1.18). Stopped early.",
  "Steroids increase death after traumatic brain injury. Never use them for TBI.")

T("decra","DECRA","N Engl J Med",2011,"Decompressive craniectomy in diffuse traumatic brain injury","Critical care",
  "155 adults with severe diffuse TBI and refractory intracranial hypertension",
  "Early bifrontotemporoparietal decompressive craniectomy",
  "Standard medical care",
  "Functional outcome (extended Glasgow Outcome Scale) at 6 months",
  "neg","Craniectomy patients had worse functional scores (odds ratio 1.84) and more unfavorable outcomes (odds ratio 2.21), even though ICP was lower.",
  "Lowering ICP with early craniectomy worsened function. A better number is not always a better patient.")

T("eurotherm","Eurotherm3235","N Engl J Med",2015,"Hypothermia for Intracranial Hypertension after Traumatic Brain Injury","Critical care",
  "387 adults with TBI and ICP above 20 mm Hg despite first-line treatment",
  "Therapeutic hypothermia (32 to 35°C) plus standard care",
  "Standard care alone",
  "Extended Glasgow Outcome Scale at 6 months",
  "neg","Favorable outcome 26% hypothermia vs 37% standard care. Stopped early for safety.",
  "Hypothermia to control ICP after TBI worsened outcomes.")

T("bart","BART","N Engl J Med",2008,"A comparison of aprotinin and lysine analogues in high-risk cardiac surgery","Critical care",
  "2331 adults undergoing high-risk cardiac surgery",
  "Aprotinin",
  "Tranexamic acid or aminocaproic acid",
  "Massive postoperative bleeding",
  "neg","Massive bleeding was slightly lower with aprotinin, but 30-day death was higher (relative risk 1.53). Stopped early.",
  "Aprotinin was pulled from the market. Less bleeding is pointless if more patients die.")

T("lips-a","LIPS-A","JAMA",2016,"Effect of Aspirin on Development of ARDS in At-Risk Patients Presenting to the Emergency Department","Critical care",
  "390 ED adults at high risk for ARDS",
  "Aspirin 325 mg loading dose then 81 mg daily",
  "Placebo",
  "Development of ARDS by day 7",
  "neu","ARDS 10.3% aspirin vs 8.7% placebo.",
  "Aspirin does not prevent ARDS.")

T("synapse","SYNAPSE","N Engl J Med",2014,"A clinical trial of progesterone for severe traumatic brain injury","Critical care",
  "1195 patients 16 to 70 with severe TBI (GCS 8 or less, at least one reactive pupil)",
  "IV progesterone started within 8 hours of injury, for 120 hours",
  "Placebo",
  "Glasgow Outcome Scale at 6 months",
  "neu","Favorable outcome 50.4% progesterone vs 50.5% placebo (odds ratio 0.96).",
  "Progesterone, promising in animals and small trials, failed in severe TBI. ProTECT III reached the same conclusion.")

T("hernandez-hfnc","High-flow vs NIV after extubation","JAMA",2016,"Effect of Postextubation High-Flow Nasal Cannula vs Noninvasive Ventilation on Reintubation and Postextubation Respiratory Failure in High-Risk Patients","Critical care",
  "604 ICU adults at high risk of extubation failure",
  "High-flow nasal oxygen for 24 hours after extubation",
  "Noninvasive ventilation for 24 hours after extubation",
  "Reintubation and postextubation respiratory failure at 72 hours (noninferiority)",
  "pos","Reintubation 22.8% high-flow vs 19.1% NIV, meeting the noninferiority margin.",
  "High-flow is a reasonable alternative to NIV after extubation in high-risk patients.")

T("subira-sbt","PS vs T-piece SBT","JAMA",2019,"Effect of Pressure Support vs T-Piece Ventilation Strategies During Spontaneous Breathing Trials on Successful Extubation Among Patients Receiving Mechanical Ventilation","Critical care",
  "1153 ventilated adults ready for a breathing trial",
  "30-minute pressure support (8 cm H2O) breathing trial",
  "2-hour T-piece breathing trial",
  "Successful extubation (no reintubation within 72 hours)",
  "pos","Successful extubation 82.3% pressure support vs 74.0% T-piece.",
  "A short, less demanding breathing trial gets more patients extubated without more reintubation.")

T("prevent-vt","PReVENT (low tidal volume)","JAMA",2018,"Effect of a Low vs Intermediate Tidal Volume Strategy on Ventilator-Free Days in Intensive Care Unit Patients Without ARDS","Critical care",
  "961 ventilated ICU adults without ARDS",
  "Low tidal volume (target 6 mL/kg PBW)",
  "Intermediate tidal volume (target 10 mL/kg PBW)",
  "Ventilator-free days to day 28",
  "neu","Median ventilator-free days 21 in both groups.",
  "Outside ARDS, low tidal volume was not better than intermediate volumes.")

T("epvent-2","EPVent-2","JAMA",2019,"Effect of Titrating Positive End-Expiratory Pressure (PEEP) With an Esophageal Pressure-Guided Strategy vs an Empirical High PEEP-Fio2 Strategy on Death and Days Free From Mechanical Ventilation Among Patients With Acute Respiratory Distress Syndrome","Critical care",
  "200 adults with moderate-to-severe ARDS",
  "PEEP titrated by esophageal pressure",
  "Empirical high PEEP/FiO2 table",
  "Composite of death and days free from ventilation at day 28",
  "neu","No difference in the composite outcome.",
  "Esophageal manometry to set PEEP did not beat a high-PEEP table.")

T("ketased","KETASED","Lancet",2009,"Etomidate versus ketamine for rapid sequence intubation in acutely ill patients","Critical care",
  "655 acutely ill adults needing emergency intubation",
  "Ketamine for induction",
  "Etomidate for induction",
  "Maximum SOFA score during the first 3 days",
  "neu","No difference in maximum SOFA score or intubating conditions.",
  "Ketamine is a safe alternative to etomidate for emergency intubation.")

T("ascend-hf","ASCEND-HF","N Engl J Med",2011,"Effect of nesiritide in patients with acute decompensated heart failure","Critical care",
  "7141 adults hospitalized with acute decompensated heart failure",
  "Nesiritide plus standard care",
  "Placebo plus standard care",
  "Dyspnea and the composite of rehospitalization for HF or death at 30 days",
  "neu","No significant improvement in dyspnea or in 30-day death or rehospitalization (9.4% vs 10.1%). More hypotension.",
  "Nesiritide offers no meaningful benefit in acute heart failure.")
