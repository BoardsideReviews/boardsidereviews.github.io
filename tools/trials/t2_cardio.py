# Trial and Error bank, part 2: cardiology.
from _t import T

T("sprint","SPRINT","N Engl J Med",2015,"A Randomized Trial of Intensive versus Standard Blood-Pressure Control","Cardiology",
  "9361 adults 50 or older with high cardiovascular risk, without diabetes or prior stroke",
  "Intensive systolic target under 120 mm Hg",
  "Standard systolic target under 140 mm Hg",
  "MI, other ACS, stroke, heart failure, or cardiovascular death",
  "pos","Primary outcome 1.65% vs 2.19% per year (hazard ratio 0.75). All-cause death also fell. More hypotension, syncope, electrolyte problems, and AKI.",
  "In high-risk adults without diabetes, aiming for a systolic under 120 prevents events and deaths at the cost of more adverse effects.")

T("accord-bp","ACCORD BP","N Engl J Med",2010,"Effects of intensive blood-pressure control in type 2 diabetes mellitus","Cardiology",
  "4733 adults with type 2 diabetes at high cardiovascular risk",
  "Intensive systolic target under 120 mm Hg",
  "Standard systolic target under 140 mm Hg",
  "Nonfatal MI, nonfatal stroke, or cardiovascular death",
  "neu","Primary outcome 1.87% vs 2.09% per year (hazard ratio 0.88, not significant). Stroke was lower with intensive control.",
  "In diabetes, intensive BP control did not reduce the main composite. The trial may have been underpowered.")

T("cast","CAST","N Engl J Med",1989,"Preliminary report: effect of encainide and flecainide on mortality in a randomized trial of arrhythmia suppression after myocardial infarction","Cardiology",
  "Post-MI patients with asymptomatic ventricular ectopy that the drug suppressed",
  "Encainide or flecainide",
  "Placebo",
  "Death or cardiac arrest from arrhythmia",
  "neg","Arrhythmic and total deaths were more than doubled with encainide or flecainide. Those arms were stopped early.",
  "Suppressing PVCs after MI with class IC drugs kills. Treat patients, not the monitor.")

T("swords","SWORD","Lancet",1996,"Effect of d-sotalol on mortality in patients with left ventricular dysfunction after recent and remote myocardial infarction","Cardiology",
  "3121 patients with LVEF 40% or less after MI",
  "d-sotalol (pure potassium channel blocker)",
  "Placebo",
  "All-cause mortality",
  "neg","Mortality 5.0% d-sotalol vs 3.1% placebo. Stopped early.",
  "Another antiarrhythmic that increased death after MI.")

T("affirm","AFFIRM","N Engl J Med",2002,"A comparison of rate control and rhythm control in patients with atrial fibrillation","Cardiology",
  "4060 adults with atrial fibrillation at risk of stroke",
  "Rhythm control (antiarrhythmic drugs, cardioversion)",
  "Rate control",
  "All-cause mortality",
  "neu","Five-year mortality 23.8% rhythm control vs 21.3% rate control (P=0.08). More hospitalizations with rhythm control.",
  "Drug-based rhythm control did not beat rate control. Keep anticoagulation either way.")

T("race-2","RACE II","N Engl J Med",2010,"Lenient versus strict rate control in patients with atrial fibrillation","Cardiology",
  "614 adults with permanent atrial fibrillation",
  "Lenient rate control (resting heart rate under 110)",
  "Strict rate control (resting under 80, and controlled with exercise)",
  "Composite of cardiovascular death, HF hospitalization, stroke, embolism, bleeding, and arrhythmic events (noninferiority)",
  "pos","Primary outcome 12.9% lenient vs 14.9% strict at 3 years, meeting noninferiority.",
  "For permanent AF with preserved function, a resting heart rate under 110 is acceptable and easier to reach.")

T("east-afnet4","EAST-AFNET 4","N Engl J Med",2020,"Early Rhythm-Control Therapy in Patients with Atrial Fibrillation","Cardiology",
  "2789 adults with atrial fibrillation diagnosed within 1 year and cardiovascular conditions",
  "Early rhythm control (antiarrhythmics or ablation)",
  "Usual care (rate control first, rhythm control for symptoms)",
  "Cardiovascular death, stroke, or hospitalization for HF or ACS",
  "pos","Primary outcome 3.9 vs 5.0 per 100 person-years (hazard ratio 0.79).",
  "Unlike AFFIRM, starting rhythm control early after diagnosis improved outcomes.")

T("cabana","CABANA","JAMA",2019,"Effect of Catheter Ablation vs Antiarrhythmic Drug Therapy on Mortality, Stroke, Bleeding, and Cardiac Arrest Among Patients With Atrial Fibrillation","Cardiology",
  "2204 adults with atrial fibrillation, 65 or older or with stroke risk factors",
  "Catheter ablation",
  "Rate or rhythm control drugs",
  "Death, disabling stroke, serious bleeding, or cardiac arrest",
  "neu","Primary outcome 8.0% ablation vs 9.2% drugs (hazard ratio 0.86, not significant). 27.5% of the drug group crossed over to ablation.",
  "In intention-to-treat, ablation did not reduce hard outcomes. It does reduce AF recurrence and improve symptoms.")

T("castle-af","CASTLE-AF","N Engl J Med",2018,"Catheter Ablation for Atrial Fibrillation with Heart Failure","Cardiology",
  "363 adults with AF, LVEF 35% or less, and an implanted defibrillator",
  "Catheter ablation",
  "Medical therapy (rate or rhythm control)",
  "Death or hospitalization for worsening heart failure",
  "pos","Primary outcome 28.5% ablation vs 44.6% medical therapy.",
  "In HFrEF with AF, ablation reduced death and HF admissions.")

T("re-ly","RE-LY","N Engl J Med",2009,"Dabigatran versus warfarin in patients with atrial fibrillation","Cardiology",
  "18113 adults with AF at risk of stroke",
  "Dabigatran 110 mg or 150 mg twice daily (blinded doses)",
  "Open-label warfarin",
  "Stroke or systemic embolism (noninferiority, then superiority)",
  "pos","Stroke or embolism 1.53% per year (110 mg) and 1.11% (150 mg) vs 1.69% with warfarin. 150 mg was superior.",
  "The first DOAC to beat warfarin. Watch renal function and GI bleeding with the higher dose.")

T("aristotle","ARISTOTLE","N Engl J Med",2011,"Apixaban versus warfarin in patients with atrial fibrillation","Cardiology",
  "18201 adults with AF and at least one stroke risk factor",
  "Apixaban 5 mg twice daily",
  "Warfarin (target INR 2 to 3)",
  "Stroke or systemic embolism",
  "pos","Stroke or embolism 1.27% vs 1.60% per year. Major bleeding 2.13% vs 3.09%. Death 3.52% vs 3.94%.",
  "Apixaban beat warfarin on stroke, bleeding, and death.")

T("averroes","AVERROES","N Engl J Med",2011,"Apixaban in patients with atrial fibrillation","Cardiology",
  "5599 adults with AF judged unsuitable for warfarin",
  "Apixaban 5 mg twice daily",
  "Aspirin 81 to 324 mg daily",
  "Stroke or systemic embolism",
  "pos","Stroke or embolism 1.6% vs 3.7% per year, with similar major bleeding. Stopped early for benefit.",
  "Aspirin is not a substitute for anticoagulation in AF. Apixaban worked better with similar bleeding.")

T("artesia","ARTESiA","N Engl J Med",2024,"Apixaban for Stroke Prevention in Subclinical Atrial Fibrillation","Cardiology",
  "4012 patients with device-detected subclinical AF lasting 6 minutes to 24 hours",
  "Apixaban",
  "Aspirin",
  "Stroke or systemic embolism",
  "pos","Stroke or embolism 0.78% vs 1.24% per patient-year. Major bleeding was higher with apixaban.",
  "Apixaban reduces stroke in device-detected AF, but the low baseline risk means weighing bleeding carefully.")

T("noah","NOAH-AFNET 6","N Engl J Med",2023,"Anticoagulation with Edoxaban in Patients with Atrial High-Rate Episodes","Cardiology",
  "2536 patients with device-detected atrial high-rate episodes (6 minutes or longer)",
  "Edoxaban",
  "Placebo (with aspirin if indicated)",
  "Cardiovascular death, stroke, or systemic embolism",
  "neu","Primary outcome 3.2% vs 4.0% per patient-year (not significant). Stopped early for futility, with more bleeding on edoxaban.",
  "For brief device-detected episodes, edoxaban did not clearly help and raised bleeding. Read with ARTESiA.")

T("pallas","PALLAS","N Engl J Med",2011,"Dronedarone in high-risk permanent atrial fibrillation","Cardiology",
  "3236 patients with permanent AF and cardiovascular risk factors",
  "Dronedarone",
  "Placebo",
  "Stroke, MI, systemic embolism, or cardiovascular death",
  "neg","Primary outcome hazard ratio 2.29 with dronedarone. More heart failure, stroke, and cardiovascular death. Stopped early.",
  "Dronedarone is contraindicated in permanent AF.")

T("bridge","BRIDGE","N Engl J Med",2015,"Perioperative Bridging Anticoagulation in Patients with Atrial Fibrillation","Cardiology",
  "1884 warfarin-treated AF patients needing elective surgery",
  "No bridging (placebo injections)",
  "Bridging with dalteparin",
  "Arterial thromboembolism (noninferiority) and major bleeding",
  "pos","Arterial thromboembolism 0.4% no bridging vs 0.3% bridging (noninferior). Major bleeding 1.3% vs 3.2%.",
  "Most AF patients stopping warfarin for surgery should not be bridged.")

T("dig","DIG","N Engl J Med",1997,"The effect of digoxin on mortality and morbidity in patients with heart failure","Cardiology",
  "6800 patients with heart failure, LVEF 45% or less, in sinus rhythm",
  "Digoxin",
  "Placebo",
  "All-cause mortality",
  "neu","Mortality 34.8% digoxin vs 35.1% placebo. HF hospitalizations fell.",
  "Digoxin relieves symptoms and reduces admissions but does not prolong life.")

T("rales","RALES","N Engl J Med",1999,"The effect of spironolactone on morbidity and mortality in patients with severe heart failure","Cardiology",
  "1663 patients with NYHA class III to IV heart failure and LVEF 35% or less",
  "Spironolactone 25 mg daily",
  "Placebo",
  "All-cause mortality",
  "pos","Mortality 35% spironolactone vs 46% placebo (relative risk 0.70). Stopped early for benefit.",
  "MRAs save lives in HFrEF. Monitor potassium and creatinine closely.")

T("topcat","TOPCAT","N Engl J Med",2014,"Spironolactone for heart failure with preserved ejection fraction","Cardiology",
  "3445 patients with symptomatic HF and LVEF 45% or more",
  "Spironolactone",
  "Placebo",
  "Cardiovascular death, aborted cardiac arrest, or HF hospitalization",
  "neu","Primary outcome 18.6% vs 20.4% (hazard ratio 0.89, not significant). HF hospitalizations fell.",
  "Neutral overall, with striking regional differences (Russia and Georgia vs the Americas) that raised doubts about enrollment.")

T("paradigm-hf","PARADIGM-HF","N Engl J Med",2014,"Angiotensin-neprilysin inhibition versus enalapril in heart failure","Cardiology",
  "8442 patients with NYHA class II to IV HF and LVEF 40% or less",
  "Sacubitril-valsartan",
  "Enalapril",
  "Cardiovascular death or HF hospitalization",
  "pos","Primary outcome 21.8% vs 26.5% (hazard ratio 0.80). Stopped early for benefit.",
  "An ARNI beats an ACE inhibitor in HFrEF.")

T("paragon-hf","PARAGON-HF","N Engl J Med",2019,"Angiotensin-Neprilysin Inhibition in Heart Failure with Preserved Ejection Fraction","Cardiology",
  "4822 patients with HF and LVEF 45% or more",
  "Sacubitril-valsartan",
  "Valsartan",
  "Total HF hospitalizations and cardiovascular death",
  "neu","Rate ratio 0.87 (95% CI 0.75 to 1.01, P=0.06).",
  "Just missed. Possible benefit at the lower end of the LVEF range and in women.")

T("dapa-hf","DAPA-HF","N Engl J Med",2019,"Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction","Cardiology",
  "4744 patients with HFrEF (LVEF 40% or less), with or without diabetes",
  "Dapagliflozin 10 mg daily",
  "Placebo",
  "Worsening HF or cardiovascular death",
  "pos","Primary outcome 16.3% vs 21.2% (hazard ratio 0.74). Benefit was the same with and without diabetes.",
  "SGLT2 inhibitors are a pillar of HFrEF therapy, diabetes or not.")

T("emperor-reduced","EMPEROR-Reduced","N Engl J Med",2020,"Cardiovascular and Renal Outcomes with Empagliflozin in Heart Failure","Cardiology",
  "3730 patients with HFrEF (LVEF 40% or less)",
  "Empagliflozin 10 mg daily",
  "Placebo",
  "Cardiovascular death or HF hospitalization",
  "pos","Primary outcome 19.4% vs 24.7% (hazard ratio 0.75).",
  "Confirmed DAPA-HF. SGLT2 inhibition works across HFrEF.")

T("emperor-preserved","EMPEROR-Preserved","N Engl J Med",2021,"Empagliflozin in Heart Failure with a Preserved Ejection Fraction","Cardiology",
  "5988 patients with HF and LVEF above 40%",
  "Empagliflozin 10 mg daily",
  "Placebo",
  "Cardiovascular death or HF hospitalization",
  "pos","Primary outcome 13.8% vs 17.1% (hazard ratio 0.79), driven by fewer HF hospitalizations.",
  "The first clearly positive drug trial in HFpEF.")

T("deliver","DELIVER","N Engl J Med",2022,"Dapagliflozin in Heart Failure with Mildly Reduced or Preserved Ejection Fraction","Cardiology",
  "6263 patients with HF and LVEF above 40%",
  "Dapagliflozin 10 mg daily",
  "Placebo",
  "Worsening HF or cardiovascular death",
  "pos","Primary outcome 16.4% vs 19.5% (hazard ratio 0.82).",
  "SGLT2 inhibitors help across the whole ejection fraction spectrum.")

T("strong-hf","STRONG-HF","Lancet",2022,"Safety, tolerability and efficacy of up-titration of guideline-directed medical therapies for acute heart failure (STRONG-HF)","Cardiology",
  "1078 patients hospitalized for acute HF, not yet on full-dose therapy",
  "High-intensity care: rapid up-titration of HF drugs to full doses within 2 weeks of discharge, with close follow-up",
  "Usual care",
  "180-day death or HF readmission",
  "pos","Primary outcome 15.2% vs 23.3%. Stopped early for benefit.",
  "Up-titrate guideline therapy quickly after an HF admission, with close lab and vital-sign checks.")

T("madit-2","MADIT-II","N Engl J Med",2002,"Prophylactic implantation of a defibrillator in patients with myocardial infarction and reduced ejection fraction","Cardiology",
  "1232 patients with prior MI and LVEF 30% or less",
  "Prophylactic ICD",
  "Conventional medical therapy",
  "All-cause mortality",
  "pos","Mortality 14.2% ICD vs 19.8% conventional therapy (hazard ratio 0.69).",
  "Primary-prevention ICDs save lives in ischemic cardiomyopathy.")

T("scd-heft","SCD-HeFT","N Engl J Med",2005,"Amiodarone or an implantable cardioverter-defibrillator for congestive heart failure","Cardiology",
  "2521 patients with NYHA class II to III HF and LVEF 35% or less",
  "Single-lead ICD (a third arm got amiodarone)",
  "Placebo",
  "All-cause mortality",
  "pos","ICD hazard ratio 0.77 vs placebo. Amiodarone hazard ratio 1.06 (no benefit).",
  "ICDs reduce death in HFrEF. Amiodarone does not.")

T("danish","DANISH","N Engl J Med",2016,"Defibrillator Implantation in Patients with Nonischemic Systolic Heart Failure","Cardiology",
  "1116 patients with nonischemic HF and LVEF 35% or less",
  "ICD",
  "Usual care",
  "All-cause mortality",
  "neu","Mortality 21.6% ICD vs 23.4% usual care (hazard ratio 0.87). Sudden death was halved. Younger patients may benefit.",
  "With modern therapy and CRT, ICDs did not lower total mortality in nonischemic cardiomyopathy.")

T("coapt","COAPT","N Engl J Med",2018,"Transcatheter Mitral-Valve Repair in Patients with Heart Failure","Cardiology",
  "614 patients with HF and moderate-to-severe or severe secondary mitral regurgitation despite maximal therapy",
  "Transcatheter edge-to-edge mitral repair (MitraClip) plus medical therapy",
  "Medical therapy alone",
  "All HF hospitalizations within 24 months",
  "pos","HF hospitalizations 35.8% vs 67.9% per patient-year. Death also fell.",
  "In carefully selected patients with MR out of proportion to LV size, MitraClip helps.")

T("mitra-fr","MITRA-FR","N Engl J Med",2018,"Percutaneous Repair or Medical Treatment for Secondary Mitral Regurgitation","Cardiology",
  "304 patients with severe secondary mitral regurgitation and LVEF 15 to 40%",
  "Percutaneous mitral repair plus medical therapy",
  "Medical therapy alone",
  "Death or unplanned HF hospitalization at 12 months",
  "neu","Primary outcome 54.6% repair vs 51.3% medical therapy.",
  "Opposite of COAPT. These patients had larger ventricles and less MR, so patient selection matters.")

T("dose","DOSE","N Engl J Med",2011,"Diuretic strategies in patients with acute decompensated heart failure","Cardiology",
  "308 patients with acute decompensated heart failure",
  "Continuous IV furosemide infusion, and high-dose (2.5 times the oral dose) in a factorial design",
  "IV boluses every 12 hours, and low-dose (equal to the oral dose)",
  "Patient global symptom assessment and change in creatinine over 72 hours",
  "neu","No significant differences between bolus and infusion or between high and low dose on either primary outcome. High dose gave more diuresis.",
  "Boluses work as well as drips. Don't be afraid to dose high.")

T("advor","ADVOR","N Engl J Med",2022,"Acetazolamide in Acute Decompensated Heart Failure with Volume Overload","Cardiology",
  "519 patients with acute decompensated HF and volume overload",
  "IV acetazolamide 500 mg daily added to loop diuretics",
  "Placebo plus loop diuretics",
  "Successful decongestion within 3 days",
  "pos","Successful decongestion 42.2% vs 30.5%.",
  "Adding acetazolamide boosts natriuresis and decongestion. It did not change death or readmission.")

T("transform-hf","TRANSFORM-HF","JAMA",2023,"Effect of Torsemide vs Furosemide After Discharge on All-Cause Mortality in Patients Hospitalized With Heart Failure","Cardiology",
  "2859 patients hospitalized with heart failure",
  "Torsemide at discharge",
  "Furosemide at discharge",
  "All-cause mortality",
  "neu","Mortality 26.1% torsemide vs 26.2% furosemide.",
  "Pick the loop diuretic that works and is affordable. Torsemide did not lower mortality.")

T("carress-hf","CARRESS-HF","N Engl J Med",2012,"Ultrafiltration in decompensated heart failure with cardiorenal syndrome","Cardiology",
  "188 patients with acute decompensated HF and worsening renal function",
  "Ultrafiltration",
  "Stepped pharmacologic therapy (titrated diuretics)",
  "Change in creatinine and weight at 96 hours",
  "neg","Creatinine rose with ultrafiltration (+0.23 mg/dL) but fell with diuretics (−0.04 mg/dL), with similar weight loss. More adverse events with ultrafiltration.",
  "Stepped diuretic therapy beat ultrafiltration in cardiorenal syndrome.")

T("fair-hf","FAIR-HF","N Engl J Med",2009,"Ferric carboxymaltose in patients with heart failure and iron deficiency","Cardiology",
  "459 patients with HFrEF and iron deficiency, with or without anemia",
  "IV ferric carboxymaltose",
  "Placebo",
  "Patient global assessment and NYHA class at week 24",
  "pos","Much or moderately improved 50% iron vs 28% placebo. NYHA class and walk distance also improved.",
  "Check iron studies in HFrEF. IV iron improves symptoms and function.")

T("shock","SHOCK","N Engl J Med",1999,"Early revascularization in acute myocardial infarction complicated by cardiogenic shock","Cardiology",
  "302 patients with MI complicated by cardiogenic shock",
  "Emergency revascularization (PCI or CABG)",
  "Initial medical stabilization",
  "30-day all-cause mortality",
  "neu","30-day mortality 46.7% revascularization vs 56.0% medical therapy (P=0.11). Six-month mortality was significantly lower (50.3% vs 63.1%).",
  "The primary endpoint missed, but survival diverged by 6 months. Emergency revascularization became the standard for MI with shock.")

T("iabp-shock-2","IABP-SHOCK II","N Engl J Med",2012,"Intraaortic balloon support for myocardial infarction with cardiogenic shock","Cardiology",
  "600 patients with MI and cardiogenic shock planned for early revascularization",
  "Intra-aortic balloon pump",
  "No IABP",
  "30-day all-cause mortality",
  "neu","30-day mortality 39.7% IABP vs 41.3% control.",
  "Routine IABP does not help in MI-related cardiogenic shock.")

T("culprit-shock","CULPRIT-SHOCK","N Engl J Med",2017,"PCI Strategies in Patients with Acute Myocardial Infarction and Cardiogenic Shock","Cardiology",
  "706 patients with multivessel disease, MI, and cardiogenic shock",
  "Culprit-lesion-only PCI (with possible staged revascularization)",
  "Immediate multivessel PCI",
  "Death or severe renal failure requiring renal replacement at 30 days",
  "pos","Primary outcome 45.9% culprit-only vs 55.4% multivessel.",
  "In shock, fix the culprit lesion only. Complete revascularization can wait.")

T("danger-shock","DanGer Shock","N Engl J Med",2024,"Microaxial Flow Pump or Standard Care in Infarct-Related Cardiogenic Shock","Cardiology",
  "360 patients with STEMI-related cardiogenic shock",
  "Microaxial flow pump (Impella CP) plus standard care",
  "Standard care",
  "All-cause death at 180 days",
  "pos","Death 45.8% pump vs 58.5% standard care (hazard ratio 0.74). More limb ischemia, bleeding, and renal replacement therapy.",
  "The first mechanical support device to lower death in selected STEMI shock (excluding comatose patients), at the cost of more complications.")

T("ecls-shock","ECLS-SHOCK","N Engl J Med",2023,"Extracorporeal Life Support in Infarct-Related Cardiogenic Shock","Cardiology",
  "420 patients with MI-related cardiogenic shock planned for early revascularization",
  "Early VA-ECMO plus usual care",
  "Usual medical therapy",
  "30-day all-cause death",
  "neu","30-day death 47.8% ECMO vs 49.0% control. More bleeding and vascular complications with ECMO.",
  "Routine early VA-ECMO did not improve survival in MI-related shock.")

T("courage","COURAGE","N Engl J Med",2007,"Optimal medical therapy with or without PCI for stable coronary disease","Cardiology",
  "2287 patients with stable coronary disease and objective ischemia",
  "PCI plus optimal medical therapy",
  "Optimal medical therapy alone",
  "Death or nonfatal MI",
  "neu","Primary outcome 19.0% PCI vs 18.5% medical therapy.",
  "In stable CAD, PCI relieves angina sooner but does not prevent death or MI.")

T("ischemia","ISCHEMIA","N Engl J Med",2020,"Initial Invasive or Conservative Strategy for Stable Coronary Disease","Cardiology",
  "5179 patients with stable CAD and moderate or severe ischemia on stress testing",
  "Initial invasive strategy (cath and revascularization when feasible)",
  "Initial conservative strategy (medical therapy, cath only if it fails)",
  "Cardiovascular death, MI, resuscitated arrest, or hospitalization for unstable angina or HF",
  "neu","No significant difference in the primary outcome over a median of 3.2 years. Angina improved with the invasive strategy.",
  "Even with moderate-to-severe ischemia, routine invasive care did not prevent events in stable CAD.")

T("orbita","ORBITA","Lancet",2018,"Percutaneous coronary intervention in stable angina (ORBITA): a double-blind, randomised controlled trial","Cardiology",
  "230 patients with stable angina and single-vessel stenosis of 70% or more",
  "PCI",
  "Sham procedure",
  "Change in exercise time",
  "neu","Exercise time difference 16.6 seconds (P=0.200).",
  "The first sham-controlled PCI trial. Much of the symptom benefit of PCI in stable angina may be placebo.")

T("orbita-2","ORBITA-2","N Engl J Med",2023,"A Placebo-Controlled Trial of Percutaneous Coronary Intervention for Stable Angina","Cardiology",
  "301 patients with stable angina and ischemia, off all antianginal drugs",
  "PCI",
  "Placebo (sham) procedure",
  "Daily angina symptom score",
  "pos","Lower angina symptom score with PCI (odds ratio 2.21).",
  "Off antianginal drugs, PCI did relieve angina better than a sham.")

T("revived","REVIVED-BCIS2","N Engl J Med",2022,"Percutaneous Revascularization for Ischemic Left Ventricular Dysfunction","Cardiology",
  "700 patients with LVEF 35% or less, extensive CAD, and viable myocardium",
  "PCI plus optimal medical therapy",
  "Optimal medical therapy alone",
  "Death or HF hospitalization",
  "neu","Primary outcome 37.2% PCI vs 38.0% medical therapy.",
  "PCI did not improve outcomes or LVEF in ischemic cardiomyopathy.")

T("stich","STICH","N Engl J Med",2011,"Coronary-artery bypass surgery in patients with left ventricular dysfunction","Cardiology",
  "1212 patients with LVEF 35% or less and CAD amenable to CABG",
  "CABG plus medical therapy",
  "Medical therapy alone",
  "All-cause mortality",
  "neu","Mortality 36% CABG vs 41% medical therapy (P=0.12). Cardiovascular death was lower with CABG.",
  "Neutral at 5 years. The 10-year extension (STICHES) did show lower mortality with CABG.")

T("freedom","FREEDOM","N Engl J Med",2012,"Strategies for multivessel revascularization in patients with diabetes","Cardiology",
  "1900 patients with diabetes and multivessel CAD",
  "CABG",
  "PCI with drug-eluting stents",
  "Death, nonfatal MI, or nonfatal stroke",
  "pos","5-year primary outcome 18.7% CABG vs 26.6% PCI. Stroke was higher with CABG.",
  "In diabetes with multivessel disease, CABG beats PCI.")

T("complete","COMPLETE","N Engl J Med",2019,"Complete Revascularization with Multivessel PCI for Myocardial Infarction","Cardiology",
  "4041 STEMI patients with multivessel disease after successful culprit PCI",
  "Staged complete revascularization of non-culprit lesions",
  "Culprit-lesion-only PCI",
  "Cardiovascular death or MI",
  "pos","Primary outcome 7.8% complete vs 10.5% culprit-only.",
  "In stable STEMI patients (not in shock), go back and fix significant non-culprit lesions.")

T("danami-2","DANAMI-2","N Engl J Med",2003,"A comparison of coronary angioplasty with fibrinolytic therapy in acute myocardial infarction","Cardiology",
  "1572 STEMI patients, including many at non-PCI hospitals",
  "Primary angioplasty, with transfer if needed (within 3 hours)",
  "On-site fibrinolysis with alteplase",
  "Death, reinfarction, or disabling stroke at 30 days",
  "pos","Primary outcome 8.5% vs 14.2% among patients randomized at referral hospitals (6.7% vs 12.3% at PCI centers), driven by less reinfarction.",
  "Transfer for primary PCI beats on-site lysis when transport is fast.")

T("plato","PLATO","N Engl J Med",2009,"Ticagrelor versus clopidogrel in patients with acute coronary syndromes","Cardiology",
  "18624 patients with ACS",
  "Ticagrelor plus aspirin",
  "Clopidogrel plus aspirin",
  "Vascular death, MI, or stroke at 12 months",
  "pos","Primary outcome 9.8% ticagrelor vs 11.7% clopidogrel. All-cause death also fell.",
  "Ticagrelor beats clopidogrel in ACS, with more dyspnea and non-CABG bleeding.")

T("triton","TRITON-TIMI 38","N Engl J Med",2007,"Prasugrel versus clopidogrel in patients with acute coronary syndromes","Cardiology",
  "13608 patients with ACS scheduled for PCI",
  "Prasugrel plus aspirin",
  "Clopidogrel plus aspirin",
  "Cardiovascular death, nonfatal MI, or nonfatal stroke",
  "pos","Primary outcome 9.9% prasugrel vs 12.1% clopidogrel. Major bleeding 2.4% vs 1.8%.",
  "Prasugrel is more potent but bleeds more. Avoid it with prior stroke or TIA.")

T("cure","CURE","N Engl J Med",2001,"Effects of clopidogrel in addition to aspirin in patients with acute coronary syndromes without ST-segment elevation","Cardiology",
  "12562 patients with NSTE-ACS",
  "Clopidogrel plus aspirin",
  "Placebo plus aspirin",
  "Cardiovascular death, nonfatal MI, or stroke",
  "pos","Primary outcome 9.3% clopidogrel vs 11.4% placebo. More major bleeding.",
  "Established dual antiplatelet therapy in ACS.")

T("isis-2","ISIS-2","Lancet",1988,"Randomised trial of intravenous streptokinase, oral aspirin, both, or neither among 17,187 cases of suspected acute myocardial infarction: ISIS-2","Cardiology",
  "17187 patients with suspected acute MI",
  "Streptokinase, aspirin, or both (factorial)",
  "Placebo",
  "5-week vascular mortality",
  "pos","Vascular death 9.2% vs 12.0% with streptokinase and 9.4% vs 11.8% with aspirin. Both together: 8.0% vs 13.2%.",
  "Aspirin for MI. A cheap pill that saves lives.")

T("deto2x","DETO2X-AMI","N Engl J Med",2017,"Oxygen Therapy in Suspected Acute Myocardial Infarction","Cardiology",
  "6629 patients with suspected MI and oxygen saturation 90% or more",
  "Oxygen 6 L/min by mask for 6 to 12 hours",
  "Ambient air",
  "1-year all-cause mortality",
  "neu","1-year death 5.0% oxygen vs 5.1% room air.",
  "Do not give oxygen to MI patients who are not hypoxemic.")

T("reduce-ami","REDUCE-AMI","N Engl J Med",2024,"Beta-Blockers after Myocardial Infarction and Preserved Ejection Fraction","Cardiology",
  "5020 patients after acute MI with LVEF 50% or more",
  "Long-term beta-blocker",
  "No beta-blocker",
  "Death or new MI",
  "neu","Primary outcome 7.9% beta-blocker vs 8.3% no beta-blocker.",
  "After MI with preserved ejection fraction, routine long-term beta-blockers did not reduce death or MI.")

T("adaptable","ADAPTABLE","N Engl J Med",2021,"Comparative Effectiveness of Aspirin Dosing in Cardiovascular Disease","Cardiology",
  "15076 patients with established atherosclerotic disease",
  "Aspirin 325 mg daily",
  "Aspirin 81 mg daily",
  "Death, MI, or stroke hospitalization",
  "neu","Primary outcome 7.28% (81 mg) vs 7.51% (325 mg). More people switched off 325 mg.",
  "81 mg is enough.")

T("4s","4S","Lancet",1994,"Randomised trial of cholesterol lowering in 4444 patients with coronary heart disease: the Scandinavian Simvastatin Survival Study (4S)","Cardiology",
  "4444 patients with coronary disease and high cholesterol",
  "Simvastatin",
  "Placebo",
  "All-cause mortality",
  "pos","Mortality 8% simvastatin vs 12% placebo (relative risk 0.70).",
  "The first trial to show a statin lowers total mortality in coronary disease.")

T("jupiter","JUPITER","N Engl J Med",2008,"Rosuvastatin to prevent vascular events in men and women with elevated C-reactive protein","Cardiology",
  "17802 healthy adults with LDL under 130 mg/dL and hsCRP 2 mg/L or more",
  "Rosuvastatin 20 mg daily",
  "Placebo",
  "MI, stroke, revascularization, unstable angina, or cardiovascular death",
  "pos","Hazard ratio 0.56. Stopped early for benefit. Physician-reported diabetes rose.",
  "Statins help in primary prevention even with normal LDL when inflammation is high.")

T("improve-it","IMPROVE-IT","N Engl J Med",2015,"Ezetimibe Added to Statin Therapy after Acute Coronary Syndromes","Cardiology",
  "18144 patients after ACS",
  "Simvastatin plus ezetimibe",
  "Simvastatin plus placebo",
  "Cardiovascular death, major coronary event, or stroke at 7 years",
  "pos","Primary outcome 32.7% vs 34.7%.",
  "Lowering LDL further with a non-statin helps. Lower is better.")

T("fourier","FOURIER","N Engl J Med",2017,"Evolocumab and Clinical Outcomes in Patients with Cardiovascular Disease","Cardiology",
  "27564 patients with atherosclerotic disease and LDL 70 mg/dL or more on a statin",
  "Evolocumab (PCSK9 inhibitor)",
  "Placebo",
  "Cardiovascular death, MI, stroke, unstable angina hospitalization, or coronary revascularization",
  "pos","Primary outcome 9.8% vs 11.3% (hazard ratio 0.85). Median LDL fell to 30 mg/dL.",
  "PCSK9 inhibitors cut events with no safety signal at very low LDL.")

T("odyssey","ODYSSEY OUTCOMES","N Engl J Med",2018,"Alirocumab and Cardiovascular Outcomes after Acute Coronary Syndrome","Cardiology",
  "18924 patients 1 to 12 months after ACS with elevated atherogenic lipids on high-intensity statins",
  "Alirocumab (PCSK9 inhibitor)",
  "Placebo",
  "Coronary heart disease death, MI, ischemic stroke, or unstable angina hospitalization",
  "pos","Primary outcome 9.5% vs 11.1% (hazard ratio 0.85).",
  "Confirmed PCSK9 benefit after ACS.")

T("reduce-it","REDUCE-IT","N Engl J Med",2019,"Cardiovascular Risk Reduction with Icosapent Ethyl for Hypertriglyceridemia","Cardiology",
  "8179 statin-treated patients with elevated triglycerides and CVD or diabetes",
  "Icosapent ethyl 2 g twice daily",
  "Mineral oil placebo",
  "Cardiovascular death, MI, stroke, revascularization, or unstable angina",
  "pos","Primary outcome 17.2% vs 22.0% (hazard ratio 0.75). More atrial fibrillation.",
  "Positive, but the mineral oil placebo raised LDL and CRP, which may have exaggerated the benefit.")

T("strength","STRENGTH","JAMA",2020,"Effect of High-Dose Omega-3 Fatty Acids vs Corn Oil on Major Adverse Cardiovascular Events in Patients at High Cardiovascular Risk","Cardiology",
  "13078 statin-treated high-risk patients with high triglycerides and low HDL",
  "Omega-3 carboxylic acid (EPA plus DHA) 4 g daily",
  "Corn oil",
  "Cardiovascular death, MI, stroke, revascularization, or unstable angina",
  "neu","Primary outcome 12.0% vs 12.2%. Stopped for futility.",
  "With a neutral comparator, high-dose omega-3s did not help. This fuels doubts about REDUCE-IT's placebo.")

T("aim-high","AIM-HIGH","N Engl J Med",2011,"Niacin in patients with low HDL cholesterol levels receiving intensive statin therapy","Cardiology",
  "3414 patients with CVD and low HDL on statins",
  "Extended-release niacin",
  "Placebo",
  "Coronary death, MI, stroke, ACS hospitalization, or revascularization",
  "neu","Primary outcome 16.4% niacin vs 16.2% placebo. Stopped for futility.",
  "Raising HDL with niacin on top of a statin does not prevent events.")

T("hps2-thrive","HPS2-THRIVE","N Engl J Med",2014,"Effects of extended-release niacin with laropiprant in high-risk patients","Cardiology",
  "25673 patients with vascular disease on statin therapy",
  "Extended-release niacin with laropiprant",
  "Placebo",
  "Major vascular events",
  "neu","Major vascular events 13.2% vs 13.7%. More serious adverse events, including bleeding, infection, and new diabetes.",
  "Niacin adds side effects without benefit. Raising HDL is not the goal.")

T("illuminate","ILLUMINATE","N Engl J Med",2007,"Effects of torcetrapib in patients at high risk for coronary events","Cardiology",
  "15067 high-risk patients on atorvastatin",
  "Torcetrapib (CETP inhibitor) plus atorvastatin",
  "Atorvastatin alone",
  "Major cardiovascular events",
  "neg","HDL rose 72%, but cardiovascular events increased (hazard ratio 1.25) and deaths rose (hazard ratio 1.58). Stopped early.",
  "Raising HDL with torcetrapib killed people, partly from off-target blood pressure and aldosterone effects.")

T("clear-outcomes","CLEAR Outcomes","N Engl J Med",2023,"Bempedoic Acid and Cardiovascular Outcomes in Statin-Intolerant Patients","Cardiology",
  "13970 statin-intolerant patients at high cardiovascular risk",
  "Bempedoic acid 180 mg daily",
  "Placebo",
  "Cardiovascular death, MI, stroke, or coronary revascularization",
  "pos","Primary outcome 11.7% vs 13.3% (hazard ratio 0.87). More gout and gallstones.",
  "A real option for statin-intolerant patients.")

T("cantos","CANTOS","N Engl J Med",2017,"Antiinflammatory Therapy with Canakinumab for Atherosclerotic Disease","Cardiology",
  "10061 patients with prior MI and hsCRP 2 mg/L or more",
  "Canakinumab (IL-1 beta antibody) at 50, 150, or 300 mg every 3 months",
  "Placebo",
  "Nonfatal MI, nonfatal stroke, or cardiovascular death",
  "pos","Hazard ratio 0.85 at the 150 mg dose, without lowering LDL. More fatal infections.",
  "Proof that inflammation drives atherosclerosis. The drug was not approved for this use.")

T("colcot","COLCOT","N Engl J Med",2019,"Efficacy and Safety of Low-Dose Colchicine after Myocardial Infarction","Cardiology",
  "4745 patients within 30 days after MI",
  "Colchicine 0.5 mg daily",
  "Placebo",
  "Cardiovascular death, resuscitated arrest, MI, stroke, or urgent hospitalization for angina needing revascularization",
  "pos","Primary outcome 5.5% vs 7.1% (hazard ratio 0.77). More pneumonia.",
  "Low-dose colchicine reduced ischemic events after MI.")

T("allhat","ALLHAT","JAMA",2002,"Major outcomes in high-risk hypertensive patients randomized to angiotensin-converting enzyme inhibitor or calcium channel blocker vs diuretic","Cardiology",
  "33357 adults 55 or older with hypertension and another cardiovascular risk factor",
  "Amlodipine or lisinopril",
  "Chlorthalidone",
  "Fatal coronary heart disease or nonfatal MI",
  "neu","No difference in the primary outcome. Chlorthalidone prevented more heart failure than amlodipine or lisinopril.",
  "A cheap thiazide-type diuretic is as good or better than newer agents as first-line therapy.")

T("hope","HOPE","N Engl J Med",2000,"Effects of an angiotensin-converting-enzyme inhibitor, ramipril, on cardiovascular events in high-risk patients","Cardiology",
  "9297 high-risk patients with vascular disease or diabetes, without HF or low EF",
  "Ramipril 10 mg daily",
  "Placebo",
  "MI, stroke, or cardiovascular death",
  "pos","Primary outcome 14.0% vs 17.8%.",
  "ACE inhibitors protect high-risk vascular patients beyond blood pressure lowering.")

T("compass","COMPASS","N Engl J Med",2017,"Rivaroxaban with or without Aspirin in Stable Cardiovascular Disease","Cardiology",
  "27395 patients with stable atherosclerotic disease",
  "Rivaroxaban 2.5 mg twice daily plus aspirin",
  "Aspirin alone",
  "Cardiovascular death, stroke, or MI",
  "pos","Primary outcome 4.1% vs 5.4%. Major bleeding was higher.",
  "Low-dose rivaroxaban plus aspirin lowers events in stable vascular disease, at a bleeding cost.")

T("icap","ICAP","N Engl J Med",2013,"A randomized trial of colchicine for acute pericarditis","Cardiology",
  "240 adults with a first episode of acute pericarditis",
  "Colchicine for 3 months plus aspirin or ibuprofen",
  "Placebo plus aspirin or ibuprofen",
  "Incessant or recurrent pericarditis",
  "pos","Incessant or recurrent pericarditis 16.7% vs 37.5%.",
  "Add colchicine to NSAIDs for every first episode of pericarditis.")

T("partner","PARTNER (cohort B)","N Engl J Med",2010,"Transcatheter aortic-valve implantation for aortic stenosis in patients who cannot undergo surgery","Cardiology",
  "358 patients with severe aortic stenosis deemed inoperable",
  "TAVR",
  "Standard therapy (often balloon valvuloplasty)",
  "All-cause mortality at 1 year",
  "pos","1-year mortality 30.7% TAVR vs 50.7% standard therapy. More strokes and vascular complications.",
  "TAVR transformed care for inoperable aortic stenosis.")

T("secure","SECURE","N Engl J Med",2022,"Polypill Strategy in Secondary Cardiovascular Prevention","Cardiology",
  "2499 patients within 6 months after MI, 65 or older",
  "Polypill (aspirin, ramipril, atorvastatin)",
  "Usual care",
  "Cardiovascular death, MI, stroke, or urgent revascularization",
  "pos","Primary outcome 9.5% vs 12.7% (hazard ratio 0.76).",
  "One pill improves adherence and cuts events after MI.")

T("everest","EVEREST Outcome","JAMA",2007,"Effects of oral tolvaptan in patients hospitalized for worsening heart failure: the EVEREST Outcome Trial","Cardiology",
  "4133 patients hospitalized with worsening HFrEF",
  "Tolvaptan 30 mg daily",
  "Placebo",
  "All-cause mortality, and cardiovascular death or HF hospitalization",
  "neu","No difference in mortality or the composite outcome over a median of 9.9 months.",
  "Vasopressin antagonism improves weight and sodium but not outcomes in heart failure.")

T("mint","MINT","N Engl J Med",2023,"Restrictive or Liberal Transfusion Strategy in Myocardial Infarction and Anemia","Cardiology",
  "3504 patients with acute MI and hemoglobin under 10 g/dL",
  "Restrictive transfusion (threshold 7 to 8 g/dL)",
  "Liberal transfusion (threshold 10 g/dL)",
  "Death or recurrent MI at 30 days",
  "neu","Primary outcome 16.9% restrictive vs 14.5% liberal (relative risk 1.15, P=0.07).",
  "Not significant, but the trend favored liberal transfusion. Many now use a higher threshold in acute MI.")
