# Multimodal Prehabilitation in Cancer Care: Development of Evidence-Based Nutritional Pathways and Educational Resources

## Background and Context

Cancer surgery places significant physiological demand on patients, and poor nutritional or functional status before treatment may be associated with poorer clinical outcomes. Prehabilitation involves optimising a patient's physical and nutritional condition before treatment begins and has emerging evidence as a way to improve these outcomes. However, translating that evidence into accessible, practical guidance for patients and clinicians remains limited.

This repository documents a professional placement project undertaken as part of the MSc Health Data Science programme at University of Aberdeen in collaboration with Dr Monika Gostic Nutrition Ltd. The project focused on systematically identifying and synthesising evidence on multimodal prehabilitation before major cancer surgery and translating the findings into practical nutritional pathways and educational resources.

## Aims and Objectives

To develop evidence-based nutritional support pathways and educational resources for individuals before cancer treatment through the systematic identification, appraisal, synthesis, and communication of evidence from multimodal prehabilitation interventions.

The objectives were to:
* Conduct a systematic review on multimodal prehabilitation for patients undergoing cancer surgery
* Narratively synthesise evidence and visually communicate the available evidence
* Translate the findings into practical resources 
* Support the host organisation’s development of evidence-based cancer nutrition services and educational resources

## Methods 

The project involved:
* Developing the review question and eligibility criteria
* Conducting structured literature searches to identify relevant randomised controlled trials
* Screening studies against predefined criteria
* Extracting study, participant, intervention and outcome data into evidence table
* Assessing risk of bias using the Cochrane Risk of Bias 2 tool
* Conducting a narrative synthesis of the evidence
* Developing evidence map and other data visualisations
* Interpreting findings for clinical and organisational use
* Translating the evidence into patient and clinician facing resources
* Developing evidence-informed knowledge base for AI cancer nutrition assistant

Microsoft Excel was used for evidence extraction and data management. Python, including pandas, Matplotlib and regular expressions, was used to clean, organise, analyse and visualise the extracted data.

## Main Findings 

The included interventions combined nutritional and exercise support, with some programmes also incorporating psychological support. The findings suggest that prehabilitation should begin as early as possible after the treatment decision. Although around four weeks was commonly used, shorter programmes may still be beneficial when surgery cannot be delayed. Support should be personalised according to nutritional risk, functional capacity and the available preoperative window.

Nutritional support commonly involved dietitian-led assessment and counselling, optimisation of energy and protein intake, and oral nutritional supplements or protein supplementation where appropriate. Exercise programmes commonly included aerobic activity, resistance training and, in some cases, respiratory muscle training. Delivery varied between supervised, home-based programmes and blended approaches. 

Functional capacity was the most consistently measured outcome and generally improved following prehabilitation. Findings for postoperative complications, length of hospital stay, nutritional status, body composition and quality of life were more variable.

## Project Outputs

The placement produced:
* A completed systematic review manuscript
* A structured evidence table
* Risk-of-bias assessment for the included studies
* An evidence map
* Descriptive data visualisations
* Evidence-based resources including prehabilitation guide and brochure for patients 
* Multiple patient education guides covering protein intake, energy intake and meal planning
* A Frequently Asked Questions document on nutritional prehabilitation
* A clinician checklist for delivering multimodal prehabilitation
* Clinical knowledge base for a cancer nutrition virtual assistant

Final host-specific resources and manuscript materials are not included in this public repository because of confidentiality and organisational requirements.
These deliverables (final manuscript, full patient/clinician resources, AI assistant knowledge base) are maintained in a companion private repository, access to which has been shared with the course coordinator.

## Implications for the Host Organisation

The project provided Dr Monika Gostic Nutrition Ltd. with an organised evidence base that the organisation can cite and build services around. 

It also provided ready-to-use patient and clinician resources that translate that evidence into a form usable in day-to-day practice and a foundation knowledge base for the host's AI-assisted nutrition tool.

The project also has a reproducible methodology that the host organisation or future placement students could extend as new evidence emerges.

The findings from the project informed:
* Evidence-based nutritional guidance for patients preparing for cancer treatment
* Content for a cancer nutrition website and digital resource library
* Development of educational resources and clinical knowledge base for a virtual nutrition assistant
* Future development of personalised prehabilitation support pathways

## Repository Structure 

systematic-review/

    Contains the review documentation, including the PICOS framework, search strategy and study protocol
    
data/

    Contains the extracted evidence table (Evidence_Table.xlsx), a cleaned CSV dataset used for analysis (cleaned_evidence_table.csv), and the RoB 2 risk-of-bias assessment (risk_of_bias_rob2.xlsx)

scripts/

    Contains the Python scripts used to load and clean the extracted data and generate the figures. This includes scripts for the evidence map and other visualisations

figures/

    Contains the final visual outputs generated from the evidence synthesis, including the PRISMA flow diagram, RoB 2 traffic-light-plot, intervention-duration chart, evidence maps, intervention-frequency chart, outcome-effects chart and sample-size/dropout chart

weekly-progress/

    Contains weekly placement records documenting the activities completed, development of the review and progression of the wider project.

## How to Navigate This Repository

For an overview of the project, begin with this README.

1. Start with systematic-review/ to understand the review question, eligibility criteria and methods.
2. Review data/ to examine the extracted evidence table, cleaned dataset and RoB 2 risk-of-bias assessment.
3. Open scripts/ to view the Python code used to load and clean the data and generate the evidence maps and other visualisations.
4. View figures/ to see the visual outputs from the evidence synthesis, including the PRISMA flow diagram, RoB 2 traffic-light plot, intervention characteristics and outcome figures.
5. Check weekly-progress/ for a chronological record of the placement activities and completed work across the placement period.

## License

This repository is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) License. See the LICENSE file for details.
