## An Effort-Reward Model Instrument parser and calculator

Siegert's Effort-Reward Imbalance (ERI) model proposes that when an 
imbalance between work effort and reward exists (particularly with effort being 
greater than the reward), work stress results. This can lead to a variety of 
adverse health outcomes. The model also suggests that over-commitment, or a 
personal motivation to work excessively, can increase the risk of these adverse 
health outcomes. ERI is measured through a questionnaire that includes items 
concerning Effort, Reward, and Over-Commitment. 

The ERI questionnaire is a standardized, self-report measure of ERI. The long 
version has 16 items: 10 measuring reward, six measuring effort, and six 
measuring over-commitment. The short version uses a battery of five questions 
for Effort. Results from the ERI battery are coded to allow calculation of an 
Effort-Reward Index based on the formula: ER = k(E/R) (where E and R are the 
effort and reward scores, and k is a correction factor (k = 7/3 for the short 
version, and k = 10/6 for the long version)). ERI is present when ER ≠ 1, with 
ER <1 indicating an imbalance in favor of rewards and 
ER >1 indicating an imbalance in favor of effort.

The code in this project will parse the results of a Survey Monkey administered 
questionnaire based on the 5 point scale version of the ERI instrument. 4 point
ERI coding and analysis will be implemented later.

Responses will be opened with file_handler.py, recoded with 
answer_recoder.py, and the ERI calculated with index_calculator.py.

In addition, freetext answers will be read by a GPT as instructed by 
sentiment_analysis.py. Relevant quotes will be found by GPT as instructed by
quote_finder.py; which work will be double-checked by a different GPT instance
as instructed by hallucination_checker.py
