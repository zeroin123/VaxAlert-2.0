---
title: "(PDF) Yellow Fever Vaccine Demand Forecasting with ARIMA, SARIMA, Linear Regression and XGBoost"
source: "https://www.researchgate.net/publication/387102702_Yellow_Fever_Vaccine_Demand_Forecasting_with_ARIMA_SARIMA_Linear_Regression_and_XGBoost"
author:
  - "[[N. Sen]]"
  - "[[Lütfiye Özge Temur]]"
  - "[[D. C. Atilla]]"
published: 2024-01-01
created: 2026-05-14
description: "PDF | The demand for vaccines is significantly increasing in various countries due to heightened population mobility and the prevalence of epidemics.... | Find, read and cite all the research you need on ResearchGate"
tags:
  - "clippings"
---
Article

## Yellow Fever Vaccine Demand Forecasting with ARIMA, SARIMA, Linear Regression and XGBoost

Authors:

[N. Sen](https://www.researchgate.net/scientific-contributions/N-Sen-2300370921)

[N. Sen](https://www.researchgate.net/scientific-contributions/N-Sen-2300370921)

- This person is not on ResearchGate, or hasn't claimed this research yet.

[L. O. Temur](https://www.researchgate.net/scientific-contributions/Luetfiye-Oezge-Temur-2307244230)

- This person is not on ResearchGate, or hasn't claimed this research yet.

[D. C. Atilla](https://www.researchgate.net/scientific-contributions/D-C-Atilla-2300344626)

- This person is not on ResearchGate, or hasn't claimed this research yet.

## Abstract and Figures

The demand for vaccines is significantly increasing in various countries due to heightened population mobility and the prevalence of epidemics. This study employed machine learning methods to predict optimal vaccine stock levels, aiming to prevent both shortages and oversupply, and to compare the effectiveness of these predictions. The data utilized in the prediction models were sourced from the General Directorate of Border and Coastal Health. This study analyzed a 21-year retrospective dataset collected between 2003 and 2023, which contains monthly vaccination coverage data. Four different methods commonly used in the literature were applied to estimate annual vaccine demand. Among these, the most widely utilized method was the Autoregressive Integrated Moving Average (ARIMA). Additionally, Seasonal Autoregressive Integrated Moving Average (SARIMA), Linear Regression, and XGBoost models are employed. Certain events, such as the COVID-19 pandemic, disrupt patterns within the dataset. In pruning tests, variations in data frequency within the raw dataset are analyzed. The models are evaluated using Root Mean Square Error (RMSE) and Mean Absolute Error (MAE). The entire dataset is then transformed to achieve stationarity. The models are re-evaluated after removing seasonality and white noise. Cross-validation is applied to the models that yield the most accurate predictions. The forecast results obtained from the optimized model serve as input for the Value at Risk (VaR) model. Actual, projected, and average vaccination numbers are presented with 95% and 99% confidence intervals (critical stock range) based on SARIMA, Linear Regresion and XGBoost estimates. Due to the vaccine forecast range balance, XGBoost’s outputs are input into the Value at Risk (VaR) model and the cost risk related to the safe vaccine stock that may arise in the coming days is evaluated. Throughout the study, the conditions under which models can continue to learn effectively, as well as the rationale for selecting these models, can be monitored.

![](https://www.researchgate.net/images/icons/svgicons/researchgate-logo-white.svg)

**Discover the world's research**

- 25+ million members
- 160+ million publication pages
- 2.3+ billion citations

Available via license: [CC BY 4.0](https://www.researchgate.net/deref/https%3A%2F%2Fcreativecommons.org%2Flicenses%2Fby%2F4.0%2F)

... Traditional time series models-such as autoregressive (AR) and autoregressive integrated moving average (ARIMA)-have been widely applied to capture demand trends \[4\], \[5\]. However, these linear models often struggle to accommodate complex seasonality and abrupt demand surges triggered by localized outbreaks ==\[6\]==. As recent studies suggest, their limited adaptability to external shocks underscores the need for more flexible, data-driven forecasting frameworks capable of rapid recalibration \[7\], \[8\]....

... Similarly, Zhou and Li \[5\] introduced a stacked ensemble method combining ARIMA with web-derived indicators using machine learning techniques such as LASSO and support vector machines, resulting in more accurate forecasts of COVID-19 vaccine uptake. In a study focused on yellow fever vaccines, Sen et al. ==\[6\]== compared ARIMA, SARIMA, linear regression, and XGBoost models, demonstrating that ensemble-based ML models can more effectively account for disruptions and complex seasonality in vaccine stock planning....

[A Data-Driven Framework for Vaccine Demand Forecasting and Inventory Simulation in a Hospital Travel Clinic](https://www.researchgate.net/publication/404053801_A_Data-Driven_Framework_for_Vaccine_Demand_Forecasting_and_Inventory_Simulation_in_a_Hospital_Travel_Clinic)

Article

Full-text available

- Jan 2026

Forecasting vaccine demand and determining inventory policies are critical challenges in healthcare supply chains, where uncertainty poses significant operational risks. This study proposes a two-step data-driven framework to support vaccine planning under uncertainty. The first step leverages machine learning models—XGBoost and LightGBM—for daily demand forecasting using a recursive multi-day strategy, with model deviations generated via bootstrapping to characterize uncertainty. Forecast accuracy is evaluated using a sliding-window Mean Cumulative Absolute Percentage Error to capture cumulative deviations relevant to operational planning. The second step employs a stochastic Monte Carlo simulation and a custom performance-based heuristic to determine proper policy parameters. A key feature is the implementation of dynamic reorder points and order quantities that adapt to forecasted demand and volatility to ensure responsiveness. By incorporating data-driven forecast distributions, the simulation evaluates tradeoffs between stock-out risk and inventory efficiency using Value-at-Risk metrics. A case study examining vaccines in a hospital travel clinic confirms the framework’s real-world applicability and the effectiveness of this hybrid approach. Results reveal that XGBoost performs better for seasonal or volatile demand, while LightGBM excels with smoother profiles. Notably, both algorithms outperform benchmark algorithms including CatBoost, LSTM, and Prophet. Furthermore, the proposed heuristic identifies effective policy parameters for each vaccine within a computationally efficient timeframe. Inventory results show that the proposed method maintains inventory days within hospital targets to maintain vaccine potency while simultaneously minimizing the risk of stockout. This is particularly advantageous for travel clinics that manage diverse vaccine portfolios with unpredictable demand and strict shelf-life constraints.

... Conventional approaches to demand forecasting, including time series analysis \[5\], linear regression ==\[6\]==, and moving averages \[7\], have been widely used to model demand patterns over time. Although effective in some applications, these methods often fail to capture the intricate, nonlinear interactions among factors such as website traffic, promotional activities, and seasonal patterns, and their impact on resulting demand \[8\]....

... Multi-Stage Search Strategy of PAS Input: Population size N, maximum iterations M, parameters ω, c 1, c 2, c 3 Output: Global best solution g 1 Initialize particle positions {x 0 i } N i=1 using optimal-point set strategy; 2 Initialize velocities {v 0 i } N i=1; 3 Evaluate fitness and initialize p i and g; 4 for i = 1 to M do 5 Compute adaptive coefficient K(i); ==6== Select search stage S(i) according to Equation (10); 7 Update velocities v t+1 i using stage-specific operator; 8 Update positions x t+1...

[PAS: A Novel Attention-Enhanced Particle Swarm Optimization Model for Demand Forecasting in Cross-Border E-Commerce](https://www.researchgate.net/publication/403339495_PAS_A_Novel_Attention-Enhanced_Particle_Swarm_Optimization_Model_for_Demand_Forecasting_in_Cross-Border_E-Commerce)

Article

Full-text available

- Mar 2026

Demand forecasting is crucial for optimizing cross-border e-commerce operations, yet traditional methods often struggle to capture complex input–output relationships and nonlinear patterns. This paper proposes an enhanced model, Particle Swarm Optimization with Attention and Strategy (PAS), to address the low search accuracy and slow convergence of conventional PSO. An optimal-point set strategy is introduced to improve population initialization and global search efficiency, enabling more effective global and local exploration. Moreover, an improved Transformer model is adapted for demand forecasting by separately modeling input and output features and fusing them through the decoder, allowing the model to better capture complex relationships between e-commerce variables. A multi-stage search and learning mechanism is further designed, in which PSO first explores the global demand space, followed by localized learning using attention mechanisms. This staged process accelerates convergence and reduces the risk of falling into local optima. Furthermore, we also conducted comparative experiments on the proposed PSO algorithm with two classical optimization algorithms, including the genetic algorithm (GA) and simulated annealing (SA), to demonstrate the rationality of the proposed method. Evaluation on real-world datasets shows that the proposed model markedly surpasses conventional approaches, achieving an average MAPE of 8.7%, which is 23% lower than the Transformer model and 30% lower than the LSTM model. This has certain significance for the reliability and stability of demand forecasting in e-commerce.

... Ten studies (Table 3) investigated AI/ML for logistics and distribution, highlighting predictive, adaptive approaches for transport, inventory, and cold-chain management. Across studies, ML time-series models and regression-based algorithms were commonly applied for demand forecasting, while Artificial Intelligence of things (AIoT)enabled robotics and blockchain integration enhanced operational reliability and real-time monitoring (Davahli et al., 2021;Meghla et al., 2021;Chabel and Ar-Reyouchi, 2024;==Sen et al., 2024)==. Comparative trends suggest that LSTM-based models performed best in forecasting demand spikes during COVID-19 vaccination campaigns, while multilayered GIS-integrated ML frameworks enabled precise route optimization for equitable delivery (Davahli et al., 2021;Mengüç et al., 2025)....

... Entre las variables de entrada más comunes se puede destacar temperatura exterior, presión, humedad relativa, irradiación solar, ocupación del edificio, números de trabajadores, etc., Para comprobar la bondad del modelo se utilizan métricas estadísticas. La más común el coeficiente de determinación R2 ==(Sen et al., 2024)==. Cuando se hace uso de MLR se aplica la estimación de mínimos cuadrados para obtener los coeficientes de regresión que permiten modelar el consumo en función de las variables seleccionadas (Urošević & M. Savić, 2025)....

[Métodos de análisis para la predicción del consumo energético en edificios sanitarios: revisiónMethods analysis for energy consumption forecasting in healthcare buildings: a reviewMétodos de análise para a previsão do consumo de energia em edifícios de cuidados de saúde: uma revisão](https://www.researchgate.net/publication/399583267_Metodos_de_analisis_para_la_prediccion_del_consumo_energetico_en_edificios_sanitarios_revisionMethods_analysis_for_energy_consumption_forecasting_in_healthcare_buildings_a_reviewMetodos_de_analise_par)

Article

Full-text available

- Jan 2026

Los edificios sanitarios son unos de los principales consumidores de energía a nivel mundial debido a las particularidades de los procedimientos sanitarios. Por lo cual es necesario optimizar sus recursos energéticos mediante planes de operación y mantenimiento. Ello puede provocar un debate sobre el impacto que puede provocar cada medida de ahorro energético. En este aspecto, el despliegue de distintos modelos predictivos se ha hecho notable en los últimos años. Su ventaja de aplicación reside en el empleo de una base de datos con la que modelar el consumo energético de los edificios sanitarios. Sin embargo, existe un debate asentado relacionado con la naturaleza del modelo predictivo a aplicar. Por tanto, esta investigación se centra en comparar la viabilidad de aplicación de los modelos predictivos para predecir la energía consumida en edificios sanitarios. Los resultados de esta investigación revelaron que existen en la bibliografía científica cuatro tipos de modelos predictivos. A pesar de esta variabilidad de opciones, las últimas investigaciones aportaron que los modelos de Inteligencia Artificial son los que ofertan capacidades mayores para las predicciones de variables de un sistema complejo como lo es un edificio sanitario.

... Where Yt is the observed concentration of gases and particles, Ai and Ck are the non-seasonal and seasonal autoregressive coefficients, Bj and Em are the non-seasonal and seasonal moving average coefficients, s=12 represents the seasonal period (monthly data) and Dt is white noise ==(Sen et al., 2024)==....

[Machine learning in drug supply chain management during disease outbreaks: a systematic review](https://www.researchgate.net/publication/371808323_Machine_learning_in_drug_supply_chain_management_during_disease_outbreaks_a_systematic_review)

Article

Full-text available

- Oct 2023
- IJECE

The drug supply chain is inherently complex. The challenge is not only the number of stakeholders and the supply chain from producers to users but also production and demand gaps. Downstream, drug demand is related to the type of disease outbreak. This study identifies the correlation between drug supply chain management and the use of predictive parameters in research on the spread of disease, especially with machine learning methods in the last five years. Using the Publish or Perish 8 application, there are 71 articles that meet the inclusion criteria and keyword search requirements according to Kitchenham's systematic review methodology. The findings can be grouped into three broad groupings of disease outbreaks, each of which uses machine learning algorithms to predict the spread of disease outbreaks. The use of parameters for prediction with machine learning has a correlation with drug supply management in the coronavirus disease case. The area of drug supply risk management has not been heavily involved in the prediction of disease outbreaks.

[Vaccine Supply Forecasting and Optimization using Deterministic and Probabilistic Approaches](https://www.researchgate.net/publication/370146287_Vaccine_Supply_Forecasting_and_Optimization_using_Deterministic_and_Probabilistic_Approaches)

Conference Paper

Full-text available

- Mar 2023

[The impact of correlation on (Range) Value-at-Risk](https://www.researchgate.net/publication/365211490_The_impact_of_correlation_on_Range_Value-at-Risk)

Article

Full-text available

- Nov 2022

The assessment of portfolio risk is often explicitly (e.g. the Basel III square root formula) or implicitly (e.g. credit risk models) driven by the marginal distributions of the risky components and their correlations. We assess the extent by which such practice is prone to model error. In the case of n = 2 risks, we investigate under which conditions the unconstrained Value-at-Risk (VaR) bounds (which are the maximum and minimum VaR for S=∑i=1nXi when only the marginal distributions of the Xi are known) coincide with the (constrained) VaR bounds when in addition one has information on some measure of dependence (e.g. Pearson correlation or Spearman's rho). We find that both bounds coincide if the measure of dependence takes value in an interval that we explicitly determine. For probability levels used in risk management practice, we show that using correlation information has typically no effect on the highest possible VaR whereas it can affect the lowest possible VaR. In the case of a general sum of n⩾2 risks, we derive Range Value-at-Risk (RVaR) bounds under an average correlation constraint and we show they are best-possible in the case of a sum of n⩾3 standard uniformly distributed risks.

[The max–min newsvendor pricing problem under conditional value-at-risk criterion](https://www.researchgate.net/publication/365129516_The_max-min_newsvendor_pricing_problem_under_conditional_value-at-risk_criterion)

Article

Full-text available

- Nov 2022

This paper studies a risk-averse newsvendor pricing model with limited demand information under the conditional value-at-risk (CVaR) criterion. The paper uses a max–min approach and the objective is to maximize the lower bound on the CVaR of the loss, i.e., the negative of profit in the worst possible distribution case. The paper analyzes the optimal ordering and pricing decisions under both multiplicative and additive demand models, identifies the optimality conditions of the lower bound on the CVaR of loss, and obtains the implicit solutions for the optimal price and order quantity. Furthermore, the paper analyzes the sensitivity of optimal solutions with respect to the degree of risk aversion.

[Forecasting the Anti-Rabies Vaccine Demand at Jawaharlal Medical College and Hospital, Ajmer, Rajasthan: A Comparative Analysis based on Time Series Model](https://www.researchgate.net/publication/357279465_Forecasting_the_Anti-Rabies_Vaccine_Demand_at_Jawaharlal_Medical_College_and_Hospital_Ajmer_Rajasthan_A_Comparative_Analysis_based_on_Time_Series_Model)

Article

Full-text available

- Sep 2021

Background: In India, high mortality and morbidity rates of human rabies is observed. Hence, a structured surveillance system is yet to be put in place for public health discussion. At the tertiary care hospital and all public health centres, requirement of anti-rabies vaccine is needed in advance to predict the upcoming months coverage so that wastage of vaccine is minimum. Objective: To find a suitable model for forecasting the appropriate stock of anti-rabies vaccines to avoid shortage and over-supply at anti rabies clinic. Methods and Material: This was a record based cross sectional study, conducted at anti rabies clinic of Jawaharlal Nehru Medical College and Hospital, Ajmer. Data of used anti rabies vaccine was taken from immunization inventory during the period from 2017 to 2020. Time series analysis based on Holt-Winter and Box-Jenkins methods were carried out to predict the need of vaccine. Results: Study series was not stationary and stationarity was observed by taken difference in the observation between two consequent months. Residuals of the series were normally distributed and independent to each other. ARIMA(0, 1, 1) was the best model in comparison to Holt-Winter model for prediction because of low value of model selection criterion. The forecasted value for anti-rabies vaccine was done for the year 2021. Conclusions: The following study concluded that time series can be used as a tool to forecast anti-rabies vaccine coverage and will help the policy makers to formulate appropriate plans and strategies and improve the management of vaccination resources and inventory.

[Advancing Deep Learning for Supply Chain Optimization of COVID-19 Vaccination in Rural Communities](https://www.researchgate.net/publication/353855095_Advancing_Deep_Learning_for_Supply_Chain_Optimization_of_COVID-19_Vaccination_in_Rural_Communities)

Conference Paper

Full-text available

- Jun 2021

[Modeling a closed-loop vaccine supply chain with transshipments to minimize wastage and threats to the public: a system dynamics approach](https://www.researchgate.net/publication/370101821_Modeling_a_closed-loop_vaccine_supply_chain_with_transshipments_to_minimize_wastage_and_threats_to_the_public_a_system_dynamics_approach)

Article

- Feb 2023

Purpose This study aims to focus on building a conceptual closed-loop vaccine supply chain (CLVSC) to decrease vaccine wastage and counterfeit/fake vaccines. Design/methodology/approach Through a focused literature review, the framework for the CLVSC is described, and the system dynamics (SD) research methodology is used to build a causal loop diagram (CLD) of the proposed model. Findings In the battle against COVID-19, waste management systems have become overwhelmed, which has created negative environmental and extremely hazardous societal impacts. A key contributing factor is unused vaccine doses, shown as a source for counterfeit/fake vaccines. The findings identify a CLVSC design and transshipment operations to decrease vaccine wastage and the potential for vaccine theft. Research limitations/implications This study contributes to establishing a pandemic-specific VSC structure. The proposed model informs the current COVID-19 pandemic as well as potential future pandemics. Social implications A large part of the negative impact of counterfeit/fake vaccines is on human well-being, and this can be avoided with proper CLVSC. Originality/value This study develops a novel overarching SD CLD by integrating the epidemic model of disease transmission, VSC and closed-loop structure. This study enhances the policymakers’ understanding of the importance of vaccine waste collection, proper handling and threats to the public, which are born through illicit activities that rely on stolen vaccine doses.

[Leveraging Data and AI to Deliver on the Promise of Digital Health](https://www.researchgate.net/publication/350863209_Leveraging_Data_and_AI_to_Deliver_on_the_Promise_of_Digital_Health)

Article

- Apr 2021
- INT J MED INFORM

Rising rates of NCDs threaten fragile healthcare systems in low- and middle-income countries. Fortunately, new digital technology provides tools to more effectively address the growing dual burden of disease. Two-thirds of the world’s population subscribed to mobile services by the end of 2018, while the falling price of connectivity and the 5 G networks rollout promise to accelerate the use of digital technology. Properly leveraged, we can employ digital solutions and applications to transform health systems from reactive to proactive and even preventive, helping people stay healthy. With artificial intelligence (AI), health systems can be made more predictive by detecting risk factors and helping health professionals respond faster to prevent disease. Yet this rapid pace of growth has also complicated the digital health landscape. Myriad digital health apps compete and overlap in the public and private sectors, and significant gaps in the collection and analysis of digital data threaten to leave some behind. Established in 2010, the Broadband Commission for Sustainable Development is led by ITU and UNESCO and advocates for the transformational impact of broadband technologies for development. Its working group on digital health, co-chaired by the Novartis Foundation and at different times Nokia, Intel and now Microsoft, identifies best practices for countries to realize the potential of digital technology in health and care. Interviewing more than 100 key stakeholders and reviewing over 200 documents, the Working Group set out to identify common challenges that countries face in implementing digital health solutions, and to develop a framework that countries can use to build systems for supporting digital health solutions. Common challenges include a lack of coordination leading to fragmented digital health solutions; lack of systems and workforce capacity to manage data and digital technology, and inadequate financing to support digital health. The working group proposes six building blocks for building digital health systems: formulate and execute a national digital health strategy; create policy and regulatory frameworks that support innovation while protecting security and privacy; ensure access to digital infrastructure; ensure interoperability of digital health system components; establish effective partnerships; and sustain adequate financing.