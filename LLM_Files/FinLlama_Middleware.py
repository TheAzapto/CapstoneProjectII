import spacy
from ollama import Client, GenerateResponse
import pandas as pd
import json

# def fuzzy_match(LLM_json_output: str) -> dict|None: 

#     name = LLM_json_output['company']
#     impact_score = LLM_json_output['impact_score']


#     with open('backend\StockNames.csv', 'r') as f:
#         reader = pd.read_csv(f)
#         company_list = reader['Names'].tolist()

#         print(company_list[0])



#     for company in company_list:
#         ratio_partial = fuzz.partial_ratio(name, company)
#         if ratio_partial > 92:
#             print(ratio_partial)
#             return {"company": company, "impact_score": impact_score}

            
        
#         ratio_full = fuzz.ratio(name, company)
#         if ratio_full > 92:
#             print(ratio_full)
#             return {"company": company, "impact_score": impact_score}

#         ratio_token = fuzz.token_sort_ratio(name, company)
#         if ratio_token > 92:
#             print(ratio_token)
#             return {"company": company, "impact_score": impact_score}
        
#     return None

client_local = Client(host='http://localhost:11434')
client_host = Client(host='http://103.157.22.12:11434')

def Summarize(msg:str) -> str:
    prompt=f"""You are a financial text analysis expert. Your task is to analyze the provided article and generate a single summary sentence for sentiment analysis.

    **Instructions:**
    1. Read and understand the article thoroughly
    2. Identify the main financial topics, entities, and events discussed
    3. Generate ONE simple, clear sentence (25-50 words) that summarizes the article's core message
    4. Output ONLY the sentence - no labels, no explanations, no additional text

    **Article:**
    {msg}

    **Guidelines:**
    - Focus on financial terminology, company names, market movements, and economic indicators
    - The sentence must be grammatically correct and self-contained
    - Include clear sentiment indicators (positive, negative, or neutral words)
    - Avoid jargon; keep it accessible
    - Be objective and accurate to the source material

    **CRITICAL: Return ONLY the summary sentence. Do not include "Summary Sentence:" or any other labels or formatting.**"""

    response: GenerateResponse = client_host.generate(model="mistral:latest",
    prompt=prompt,
    options={
        'temperature': 0.2,
        'top_p': 0.85,
        'top_k': 30,
        'num_predict': 60,
        'repeat_penalty': 1.1,
        'num_ctx': 4096,
        'num_thread': 16,
    })

    return response.response

def keyword_extractor(sentence: str) -> str:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
 
    seen: set[str] = set()
    keywords: list[dict] = []

    target_pos = {"ADJ"}
    for token in doc:
        if (
            token.pos_ in target_pos
            and not token.is_stop
            and not token.is_punct
            and token.text.lower() not in seen
            and len(token.text) > 1
        ):
            seen.add(token.text.lower())
            keywords.append(token.text) # type: ignore
 
    res = ''
    for word in keywords:
        res+=f'-{word}  '
    
    return res

def Evaluate(input:str) -> str:

    summary = Summarize(input)
    keywords = keyword_extractor(input) 

    sen = f"summary:{summary}\nkeywords:{str(keywords)}"
    
    system_prompt=f"""You are a financial sentiment analysis expert. Your task is to evaluate the provided article and assign precise impact scores.

    **Instructions:**
    1. Analyze the sentiment and financial implications of the Article
    2. Identify ALL companies or entities mentioned in the article
    3. For EACH company, assign an impact score between -1.0 and 1.0 where:
       - -1.0 = extremely negative impact
       - -0.5 = moderately negative impact
       - 0.0 = neutral or no clear impact
       - 0.5 = moderately positive impact
       - 1.0 = extremely positive impact
    4. Consider market impact, investor sentiment, and economic implications for each company
    5. Use decimal precision (e.g., -0.73, 0.42, 0.15)

    **Article to Analyze:**
    {sen}

    **Scoring Guidelines:**
    - Strong negative words (crash, plunge, collapse, crisis) → -0.7 to -1.0
    - Moderate negative words (decline, fall, weak, concern) → -0.3 to -0.6
    - Neutral words (stable, unchanged, maintained) → -0.2 to 0.2
    - Moderate positive words (rise, growth, improvement, gain) → 0.3 to 0.6
    - Strong positive words (surge, soar, breakthrough, boom) → 0.7 to 1.0

    **Output Format:**
    Return ONLY a single float number between -1.0 and 1.0
    
    **Examples of valid outputs:**
    0.75
    -0.42
    -0.88
    0.33

    **CRITICAL RULES:**
    - Output must be a valid float number with up to 2 decimal places
    - No explanations, no text, no labels, no markdown
    - No words like "score:", "impact:", or any prefixes
    - Just the number itself (e.g., 0.65).
    - Avoid 0.0, as all news has some change
    - Do not format wrap it in json. Return just the numeric value
    - Refer the Word Influence Table below for scoring help.
    
    **Word Influence**
    | Word | Score | Influence |
    |------|-------|-----------|
    | record high | 0.95 | positive |
    | all-time high | 0.95 | positive |
    |surge|0.9|positive|
    |soar|0.9|positive|
    |boom|0.85|positive|
    |rally|0.8|positive|
    |breakout|0.8|positive|
    |record high|0.95|positive|
    |all-time high|0.95|positive|
    |outperform|0.8|positive|
    |beat expectations|0.85|positive|
    |exceed|0.75|positive|
    |profit|0.75|positive|
    |revenue growth|0.8|positive|
    |earnings beat|0.85|positive|
    |upgrade|0.8|positive|
    |bull market|0.85|positive|
    |bullish|0.8|positive|
    |strong|0.7|positive|
    |robust|0.7|positive|
    |record profit|0.9|positive|
    |dividend increase|0.8|positive|
    |buyback|0.65|positive|
    |acquisition|0.55|positive|
    |market cap growth|0.75|positive|
    |recovery|0.7|positive|
    |rebound|0.7|positive|
    |gain|0.65|positive|
    |rise|0.6|positive|
    |increase|0.55|positive|
    |growth|0.65|positive|
    |expansion|0.65|positive|
    |improvement|0.6|positive|
    |advance|0.6|positive|
    |positive|0.55|positive|
    |optimism|0.7|positive|
    |opportunity|0.6|positive|
    |momentum|0.6|positive|
    |solid|0.55|positive|
    |confidence|0.65|positive|
    |upside|0.65|positive|
    |upward|0.55|positive|
    |deliver|0.5|positive|
    |innovate|0.6|positive|
    |milestone|0.65|positive|
    |sustainability|0.55|positive|
    |resilient|0.65|positive|
    |efficiency|0.55|positive|
    |partnership|0.5|positive|
    |launch|0.5|positive|
    |breakthrough|0.75|positive|
    |accelerate|0.6|positive|
    |crash|-0.95|negative|
    |collapse|-0.9|negative|
    |plunge|-0.9|negative|
    |bankruptcy|-0.95|negative|
    |default|-0.9|negative|
    |recession|-0.85|negative|
    |crisis|-0.85|negative|
    |loss|-0.75|negative|
    |debt|-0.6|negative|
    |deficit|-0.65|negative|
    |fraud|-0.95|negative|
    |scandal|-0.85|negative|
    |miss expectations|-0.8|negative|
    |earnings miss|-0.8|negative|
    |downgrade|-0.8|negative|
    |layoffs|-0.75|negative|
    |downturn|-0.75|negative|
    |bear market|-0.85|negative|
    |bearish|-0.75|negative|
    |sell-off|-0.75|negative|
    |decline|-0.65|negative|
    |drop|-0.6|negative|
    |fall|-0.55|negative|
    |weak|-0.6|negative|
    |slump|-0.7|negative|
    |concern|-0.5|negative|
    |risk|-0.5|negative|
    |warning|-0.65|negative|
    |uncertainty|-0.55|negative|
    |volatility|-0.5|negative|
    |headwind|-0.6|negative|
    |tariff|-0.55|negative|
    |inflation|-0.6|negative|
    |stagflation|-0.8|negative|
    |hyperinflation|-0.9|negative|
    |writedown|-0.75|negative|
    |impairment|-0.7|negative|
    |restructuring|-0.55|negative|
    |liquidation|-0.85|negative|
    |fine|-0.6|negative|
    |penalty|-0.65|negative|
    |lawsuit|-0.65|negative|
    |overvalued|-0.6|negative|
    |bubble|-0.7|negative|
    |shortfall|-0.65|negative|
    |insolvency|-0.9|negative|
    |devaluation|-0.75|negative|
    |downside|-0.6|negative|
    |pressure|-0.5|negative|
    |contraction|-0.7|negative|
    |merger|0.0|neutral|
    |report|0.0|neutral|
    |quarter|0.0|neutral|
    |forecast|0.0|neutral|
    |guidance|0.0|neutral|
    |analyst|0.0|neutral|
    |market|0.0|neutral|
    |shares|0.0|neutral|
    |equity|0.0|neutral|
    |bond|0.0|neutral|
    |yield|0.05|neutral|
    |interest rate|0.0|neutral|
    |Federal Reserve|0.0|neutral|
    |central bank|0.0|neutral|
    |IPO|0.1|neutral|
    |trade|0.0|neutral|
    |index|0.0|neutral|
    |portfolio|0.0|neutral|
    |stake|0.0|neutral|
    |sector|0.0|neutral|
    |regulatory|-0.05|neutral|
    |filing|0.0|neutral|
    |earnings|0.05|neutral|
    |revenue|0.05|neutral|
    |output|0.0|neutral|
    |supply chain|0.0|neutral|
    |inventory|0.0|neutral|
    |liquidity|0.1|neutral|
    |capital|0.0|neutral|
    |dividend|0.1|neutral|
    |spread|0.0|neutral|
    |hedge|0.05|neutral|
    |derivative|0.0|neutral|
    |futures|0.0|neutral|
    |commodity|0.0|neutral|
    |valuation|0.0|neutral|
    |benchmark|0.0|neutral|
    |leverage|-0.05|neutral|
    |compliance|0.05|neutral|
    |audit|0.0|neutral|
    |fiscal|0.0|neutral|
    |monetary|0.0|neutral|
    |balance sheet|0.05|neutral|
    |cash flow|0.1|neutral|
    |operating margin|0.05|neutral|
    |divestiture|-0.05|neutral|
    |spinoff|0.05|neutral|
    |SEC|0.0|neutral|
    |disclosure|0.0|neutral|
    |analyst rating|0.0|neutral|

    """


    response = client_local.generate(model="hf.co/us4/fin-llama3.1-8b:Q5_K_M", 
    prompt=system_prompt,
    options={
    'temperature': 0.1,
    'top_p': 0.9,
    'top_k': 40,
    'num_predict': 300,
    'repeat_penalty': 1.0,
    'num_ctx': 2048,
    'num_thread': 16,
    })

    return response.response