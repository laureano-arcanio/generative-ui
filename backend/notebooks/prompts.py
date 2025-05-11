describe_business_prompt = """
Rewrite this business description into a more detailed, prompt-ready version. 
Ensure clarity, conciseness, and focus. 
Enhance specificity without adding unnecessary details or filler.
Refine precision without changing its verbal tone, mood, or writing personality.
Dont add any questions or calls to action.
"""

business_overview_questions_prompt = """
Use the business description to answer the following questions to provide a comprehensive overview of the business. 
If there is not enough information to extract the question, leave it blank.
Format the response as a list of questions and answers, with each question followed by its corresponding answerin a new line.
Each question should be answered in a single sentence or a short paragraph.
Each question / answer pair should be separated by a new line.
Each answer should have an axterisk followed by a white space and the answer.

The questions to answer are:
- What is the name of the business?
- What products or services does the business offer?
- How are these products/services sold?
- Briefly describe the target audience.
- What makes this business unique or different from competitors?
- What problem(s) does the business solve for customers?
- What is the price range or pricing strategy?
- Where does the business operate (geographical scope)?
- What sales channels are used?
- How does the business acquire customers?
- What is the brand tone or personality?
- What are the core values or mission statement?
- Who are the main competitors?
- Are there flagship products or bestsellers?
- How does the business handle fulfillment and logistics?
- How does the business engage with customers?
- What kind of post-sale support is offered?
- What are the business's short-term goals?
- What are the business's long-term goals?
- Are there notable partnerships or collaborations?
- What’s the business model?
- What KPIs or success metrics are most important?
"""

analyse_business_overview_questions_prompt = """
Analyze the following list of questions and answers.
Evaluate how well the business is described by assessing the completeness and level of detail provided in the answers. 
Write a short summary highlighting which key aspects or information are missing or incomplete.
Rank the overall description based on completeness, using a score from 0 to 100.
0 = Not at all complete
100 = Fully complete
The analysis should be concise and focused on the quality of the information provided in the answers.
Do not rewrite or summarize the answers themselves; only evaluate the completeness and detail of the information provided.
The analysis should be structured as follows:
- Completeness Score: [0-100]
- Missing Information: [List of key aspects or information that are missing or incomplete]
- Summary: [A short summary of the analysis]
"""

business_categories_prompt = """
List 20 broad business categories with a short description.

Analyze the business description and identify all applicable business categories it belongs to. List only the matching categories from the provided list. Do not include explanations, additional details, or unrelated information.

Categories:
- Retail & E-commerce - Selling physical or digital products directly to consumers through online platforms or physical stores.
- Food & Beverage - Businesses that produce, distribute, or sell food and drinks, including restaurants, cafes, and packaged goods.
- Technology & Software - Companies that develop software, apps, or provide technology solutions and services.
- Health & Wellness - Businesses focused on healthcare, fitness, nutrition, and mental well-being.
- Finance & Insurance - Organizations offering banking, investments, financial planning, or insurance products.
- Education & Training - Institutions or services providing academic, vocational, or corporate learning.
- Creative & Media - Businesses involved in content creation, marketing, advertising, publishing, and entertainment media.
- Hospitality & Tourism - Hotels, travel agencies, tour operators, and other businesses serving travelers and guests.
- Real Estate & Construction - Companies engaged in property development, sales, leasing, and construction services.
- Professional Services - Firms offering specialized knowledge-based services such as consulting, legal, or accounting.
- Manufacturing & Industrial - Businesses that produce goods at scale for B2B or B2C markets.
- Logistics & Transportation - Companies handling the movement, storage, and delivery of goods.
- Energy & Utilities - Providers of electricity, gas, renewable energy, and essential infrastructure.
- Entertainment & Gaming - Businesses creating movies, music, games, or live entertainment experiences.
- Agriculture & Farming - Enterprises involved in cultivating crops, raising livestock, or related food production.
- Beauty & Personal Care - Companies selling cosmetics, skincare, haircare, and wellness products or services.
- Sports & Recreation - Businesses providing sports equipment, fitness facilities, or recreational activities.
- Nonprofit & Social Enterprises - Organizations focused on social causes, advocacy, or charitable services.
- Automotive - Businesses related to vehicle manufacturing, sales, repair, and automotive services.
- Telecommunications - Companies providing internet, phone, and communication technology infrastructure.
"""

business_owner_characteristics_prompt = """
Analyze the following business description and extract characteristics of the business owner or founder that can be inferred from the writing. Focus only on what is implied by the language, priorities, and focus of the description.

Organize your response under the following categories, using brief descriptive phrases for each:

- Communication Style - How does the owner communicate (e.g., formal, casual, technical, conversational)?
- Personality Traits - What personality traits are implied (e.g., ambitious, detail-oriented, creative, pragmatic)?
- Value Priorities - What values seem most important to the owner (e.g., innovation, speed, sustainability, quality)?
- Business Mindset/Approach - What strategic approach is reflected (e.g., growth-focused, niche, scalable, experimental)?
- Risk Appetite - What level of risk tolerance is suggested (e.g., risk-taking, conservative, disruptive)?
- Customer Orientation - How focused is the owner on customer needs (e.g., customer-centric, product-centric)?
- Motivation Indicators - What motivates the owner (e.g., solving problems, disrupting industries, creating beauty)?
- Strategic Focus - Where does the owner seem to place strategic emphasis (e.g., marketing, operations, branding)?
- Cultural or Social Inclinations - Are there indications of ethical, sustainability, inclusivity, or social values?
- Business Maturity - Does the writing suggest an early-stage startup mindset or a seasoned business owner perspective?

Do not rewrite or summarize the description itself; only infer characteristics based on what is implied by the content, tone, and focus of the writing.
"""
