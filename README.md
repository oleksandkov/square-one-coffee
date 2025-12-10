# Square One Coffee Research Partnership

> *"At Square 1, we foster belonging by creating community. We own our presence in the community by acting with integrity and generosity."* — Square One Coffee

**Learning partnership** between [RG-FIDES](https://github.com/RG-FIDES) and [Square One Coffee](https://www.square1coffee.ca/), a family-owned specialty coffee chain in Edmonton, Alberta. We're researchers who consult by helping you learn—delivering insights while teaching the methods behind them.

## 🎯 Project Overview

**Partner**: Square One Coffee (est. 2015, Jonathon & Brandy Brozny)  
**Locations**: 6 active + 1 coming soon (Edmonton metro)  
**Research Team**: RG-FIDES (Framework for Interpretive Dialogue and Epistemic Symbiosis)  

### What We Do
- **Answer business questions** using rigorous research methods
- **Systematize knowledge** from open and internal data sources  
- **Build analytical capacity** so SOC can explore future questions independently
- **Test hypotheses** collaboratively with academic-quality methods

### Why We're Different
**Traditional consultants** deliver reports and leave.  
**Researchers** deliver insights + teach you how to generate more.  

We consult by helping you learn. Every analysis becomes a template. Every question answered builds capacity for the next one.

### Core Services
1. **Market Intelligence** — Competitive landscape, customer insights, growth opportunities
2. **Operational Analytics** — Staffing optimization, inventory management, performance benchmarking
3. **Hypothesis Testing** — Rigorous analysis of strategic questions SOC leadership poses
4. **Data Strategy** — Open data collection systems and internal data organization

### Related SOC Businesses
- **Anecdote Coffee Roasters** (2022) — In-house roasting operation
- **Doorstep Barista** — Craft coffee subscription service
- **Stone & Wheel Pizzeria** — Restaurant expansion

---

## 📁 Repository Structure

```
├── ai/                    # AI support system (personas, memory, context)
│   ├── project/           # Mission, methodology, glossary
│   └── memory/            # Decision logs and AI notes
├── analysis/              # Research analyses and reports
├── data-public/           # Non-sensitive data and profiles
│   └── derived/           # Generated documents (e.g., business profiles)
├── data-private/          # SOC operational data (when available)
├── guides/                # Project documentation
└── philosophy/            # Research frameworks (FIDES, validity)
```

---


## 🎭 AI Persona System

This project template includes 9 specialized AI personas, each optimized for different research tasks:

### **Core Personas**
- **🔧 Developer** - Technical infrastructure and reproducible code
- **📊 Project Manager** - Strategic oversight and coordination
- **🔬 Research Scientist** - Statistical analysis and methodology

### **Specialized Personas**  
- **💡 Prompt Engineer** - AI optimization and prompt design
- **⚡ Data Engineer** - Data pipelines and quality assurance
- **📈 Grapher** - Data visualization and display of informatioin
- **📝 Reporter** - Analysis communication and storytelling
- **🚀 DevOps Engineer** - Deployment and operational excellence
- **🎨 Frontend Architect** - User interfaces and visualization

You can switch between personas in VSCode:
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Activate [Persona Name] Persona"  
- Instruct the chat agent to switch to the specific persona you name  

You can define persona's default context in `get_persona_configs()` function of `ai/scripts/dynamic-context-builder.R`:

```r
"project-manager" = list(
  file = "./ai/personas/project-manager.md",
  default_context = c("project/mission", "project/method", "project/glossary")
)
```

You can define what context files get a shortcut alias, so they can be integrated into the chat calls easily. See `get_file_map()` function in `ai/scripts/dynamic-context-builder.R`.



## 🧠 Memory System

The template includes an intelligent memory system that maintains project continuity:

- **`ai/memory/memory-human.md`** - Your decisions and reasoning, only humans can edit
- **`ai/memory/memory-ai.md`** - AI-maintained technical status, only AI can edit
- **`ai/memory/log/YYYY-MM-DD.md** - dedicated folder in which one file = one log entry. Helps to isolate large changes to a single file for easier tracking.

# 🚀 Quick Start Guide

## Step 1: Standard Setup

1. **Install Prerequisites**
   - [R (4.0+)](https://cran.r-project.org/)
   - [RStudio](https://rstudio.com/products/rstudio/) or [VS Code](https://code.visualstudio.com/)
   - [Git](https://git-scm.com/)
   - [Quarto](https://quarto.org/) (for reports)

2. **Clone and Open Project**
   ```bash
   git clone [your-repo-url]
   cd quick-start-template
   ```
   - Open `quick-start-template.Rproj` in RStudio, or
   - Open folder in VS Code

3. **Install R Dependencies** 
   
   **Choose your preferred approach** (see `docs/environment-management.md` for detailed comparison):

   **Option A: Enhanced CSV System (Default - Flexible)**
   ```r
   # Enhanced system with version constraints
   Rscript utility/enhanced-install-packages.R
   
   # Or original system (backward compatible)
   Rscript utility/install-packages.R
   ```
   
   **Option B: renv (Strict Reproducibility)**
   ```r
   # For exact reproducibility (research publication)
   Rscript utility/init-renv.R
   ```
   
   **Option C: Conda (Cross-Language Projects)**
   ```bash
   # For R + Python workflows
   conda env create -f environment.yml
   conda activate quick-start-template
   ```

## Step 2: AI Support System Setup

4. **Initialize AI System**
   - **In VS Code**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Show AI Context Status"

5. **Assign the active persona**
   - In VS Code: `Ctrl+Shift+P` → "Tasks: Run Task" → "Activate [default] Persona"

5. **Customize Your Project**

Each personal could be customized by adding specific documents to the dynamic part of the copilot-instructions.md (Section 3). Some personas may have some documents loaded by default (e.g. Project Manager and Grapher load mission, method, and glossary). 

   - Edit `ai/mission.md` - What you wan to do: goals and deliverables
   - Edit `ai/method.md` - How you want to do it: tecniques and processes 
   - Edit `ai/glossary.md` - Encyclopedia of domain-specific terms
   - Update `config.yml` - To set project-specific configurations
