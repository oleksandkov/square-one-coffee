# Methodology: Square One Coffee Research

**Approach**: Learning partnership model emphasizing systematic knowledge organization, open data utilization, and capacity building for question-driven inquiry. Grounded in the FIDES framework for human-AI collaboration.

## Core Principles

1. **Open Data First** — Maximize free, publicly available information before requesting internal data
2. **Question-Driven** — Research follows SOC's questions, not predetermined analyses
3. **Co-Learning** — Joint interpretation of findings; we teach analytical thinking while delivering insights
4. **Capacity Building** — Transfer skills and methods alongside delivering analyses
5. **Rigorous Methods** — Academic-quality research applied to business questions
6. **Iterative** — Start simple, deepen based on what's learned and what new questions emerge

## Data Collection Strategy

### Tier 1: Free Open Sources (Priority)
**Objective**: Build comprehensive business knowledge without cost or burden to SOC

**Sources**: Web scraping, social media, online reviews, public demographic data, competitor websites

1. **SOC Business Systematization**
   - Document all public information about SOC (locations, hours, products, history)
   - Map the SOC ecosystem (Anecdote, Doorstep Barista, Stone & Wheel)
   - Archive website content and social media presence (baseline)
   - Create queryable business profile document

2. **Competitive Intelligence**
   - Identify Edmonton specialty coffee competitors
   - Scrape public information (locations, prices, menus, hours)
   - Analyze social media presence and engagement patterns
   - Map geographic distribution and market coverage gaps

3. **Customer Voice Analysis**
   - Aggregate online reviews (Google, Yelp, Facebook) for SOC and competitors
   - Sentiment analysis and topic extraction
   - Identify recurring themes in customer feedback
   - Track sentiment over time

4. **Demographic Context**
   - Population, income, age distribution around each SOC location
   - Commuting patterns and foot traffic potential (open data)
   - Neighborhood characteristics and coffee culture indicators

### Tier 2: Low-Burden Internal Data (When Ready)
**Objective**: Answer SOC's specific questions using operational data, with minimal burden on staff

**Approach**: Start with data SOC already collects (POS, scheduling software exports). No new systems required.

1. **Question Formulation Workshops**
   - Work with SOC leadership to articulate key business questions
   - Translate questions into data requirements
   - Assess what data is available vs. what would need to be collected
   - Prioritize questions by importance and data availability

2. **Data Assessment & Preparation**
   - Inventory existing data sources (POS system, scheduling, inventory)
   - Evaluate data quality and completeness
   - Design simple data export protocols
   - Create data documentation (what each field means)

3. **Collaborative Analysis Sessions**
   - Joint interpretation of findings (never just send a report)
   - Teach analytical thinking through example
   - Surface new questions based on what's discovered
   - Document insights and next inquiry directions

4. **Skill Transfer Activities**
   - Show SOC team how analyses were conducted
   - Create templates for repeated analyses
   - Build simple dashboards SOC can maintain
   - Encourage independent exploration

### Tier 3: Deliberate Data Collection (Only When Needed)
**Objective**: Fill critical knowledge gaps when open and operational data insufficient

**Principle**: Only collect new data when a specific question cannot be answered otherwise.

1. **Gap Identification**
   - What questions remain after Tier 1 & 2 analyses?
   - What information is needed but not available?
   - Is the question important enough to justify collection effort?

2. **Method Design (Low-Cost Priority)**
   - **Observational studies** — Count foot traffic, observe patterns (free, time-intensive)
   - **Customer surveys** — Keep short, incentivize with discounts (low cost)
   - **Staff interviews** — Capture institutional knowledge (free, high value)
   - **Digital tracking** — Only if passive and privacy-respecting

3. **Ethical Review**
   - Does this respect customer/staff privacy?
   - Is informed consent obtained when required?
   - How is data secured and who has access?
   - What's the benefit-to-burden ratio?

4. **Execution & Integration**
   - Pilot on small scale first
   - Train SOC staff to collect if ongoing
   - Integrate findings into knowledge base
   - Evaluate: Was the juice worth the squeeze?

## FIDES Framework Application

This project applies the Framework for Interpretive Dialogue and Epistemic Symbiosis:

- **Human-Centered**: SOC's questions drive the inquiry; AI assists analysis, doesn't prescribe answers
- **Transparency**: Methods, data sources, and limitations clearly explained and reproducible
- **Accountability**: Research team delivers quality analysis AND teaches the process
- **Iterative**: Continuous dialogue; each finding generates new questions and deeper partnership
- **Ethical**: Privacy protection, honest uncertainty, no extractive data practices
- **Capacity Building**: Success = SOC gains both immediate insights and long-term analytical capability

## Reproducibility Standards

- All analyses version-controlled in this repository
- Random seeds documented for any stochastic processes
- Data transformations scripted and auditable
- External data sources cited with access dates
- Methodology decisions logged in `ai/memory/memory-human.md`

## Documentation & Knowledge Management

- **Living Business Profile**: Continuously updated document in `data-public/derived/`
- **Analysis Notebooks**: Quarto documents showing methods + findings (for learning)
- **Question Log**: Track questions asked, answers found, new questions emerged
- **Method Documentation**: How-to guides SOC can reference independently
- **Decision Memory**: Why we chose certain approaches, what we learned
- **Data Source Inventory**: Where information comes from, how to update it