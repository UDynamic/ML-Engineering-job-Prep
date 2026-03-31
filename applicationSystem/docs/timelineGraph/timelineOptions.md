# Career Progression Diagram Options

Below are multiple diagram styles based on `applicationSystem/PYDEV.md`, so you can choose the one that best represents your story.

## Option 1 — Clean chronological timeline

```mermaid
timeline
    title Mahriar Gharaghani — Education, Career, Certifications, and Projects
    2017 : Began B.Sc. in Industrial Engineering
         : Isfahan University of Technology
    2019 : Project Control Specialist
         : Jahanpars Group
         : Built reporting discipline, schedule tracking, and management analysis
    2020 : Continued project controls and coordination work
    2021 : Expanded practical software foundations through self-driven development
    2022 : Completed multiple freeCodeCamp certifications
         : Responsive Web Design
         : JavaScript Algorithms and Data Structures
         : Front End Development Libraries
         : Data Visualization
         : Relational Database
         : Back End Development and APIs
    2023 : Completed B.Sc. in Industrial Engineering
         : Started M.Sc. in Engineering Management
         : Joined IEIC as Project Management Officer
         : Led planning and coordination team
    2023 : Built Logistics Marketplace Heatmap Decision Support Tool
         : Combined analytics, automation, and business insight
    2024 : Deepened Python, backend, automation, and AI application skills
         : Built RAG4Konkur local LLM study assistant
         : Explored algorithmic trading systems
    2024 : Worked on Autonomous Assembling Robotic Arm simulation
         : Applied deep reinforcement learning to robotics control
    2025 : Developed Autonomous Budgeting AI Agent thesis project
         : Reinforcement learning for budgeting under uncertainty
    2026 : Expected completion of M.Sc. in Engineering Management
```

## Option 1.1 — Split timeline with education above

```mermaid
flowchart TB
    subgraph TOP[Education]
        direction LR
        E2017[2017<br/>Begin B.Sc. in Industrial Engineering<br/>Isfahan University of Technology]
        E2023[2023<br/>Start M.Sc. in Engineering Management<br/>Iran University of Science and Technology]
        E2026[2026<br/>Expected M.Sc. completion]
    end

    subgraph MID[Years]
        direction LR
        Y2017((2017)) --> Y2019((2019)) --> Y2020((2020)) --> Y2021((2021)) --> Y2022((2022)) --> Y2023((2023)) --> Y2024((2024)) --> Y2025((2025)) --> Y2026((2026))
    end

    subgraph BOTTOM[Career and Projects]
        direction LR
        C2019[Project Control Specialist<br/>Jahanpars Group<br/>Reporting, schedules, management analysis]
        C2020[Continued project controls<br/>and coordination work]
        C2021[Expanded software foundations<br/>through self-driven development]
        C2022[Completed freeCodeCamp certifications<br/>Web, JavaScript, Data Viz, DB, APIs]
        C2023A[Project Management Officer<br/>IEIC<br/>Led planning and coordination team]
        C2023B[Built Logistics Marketplace<br/>Heatmap Decision Support Tool]
        C2024A[Deepened Python, backend,<br/>automation, and AI application skills]
        C2024B[Built RAG4Konkur and explored<br/>algorithmic trading systems]
        C2024C[Worked on Autonomous Assembling<br/>Robotic Arm RL simulation]
        C2025[Developed Autonomous Budgeting<br/>AI Agent thesis project]
    end

    E2017 --- Y2017
    E2023 --- Y2023
    E2026 --- Y2026

    Y2019 --- C2019
    Y2020 --- C2020
    Y2021 --- C2021
    Y2022 --- C2022
    Y2023 --- C2023A
    Y2023 --- C2023B
    Y2024 --- C2024A
    Y2024 --- C2024B
    Y2024 --- C2024C
    Y2025 --- C2025
```

## Option 1.2 — Timeline with grouped story lanes

```mermaid
timeline
    title Mahriar Gharaghani — Grouped Timeline View
    2017 : EDUCATION — Began B.Sc. in Industrial Engineering
         : Isfahan University of Technology
    2019 : JOBS — Project Control Specialist
         : Jahanpars Group
         : Reporting, schedule tracking, and management analysis
    2020 : JOBS — Continued project controls and coordination work
    2021 : PROJECTS — Expanded practical software foundations through self-driven development
    2022 : PROJECTS — Completed freeCodeCamp certifications
         : Responsive Web Design, JavaScript Algorithms and Data Structures
         : Front End Development Libraries, Data Visualization
         : Relational Database, Back End Development and APIs
    2023 : EDUCATION — Completed B.Sc. in Industrial Engineering
         : Started M.Sc. in Engineering Management
         : Iran University of Science and Technology
    2023 : JOBS — Project Management Officer
         : IEIC
         : Led planning and coordination team
    2023 : PROJECTS — Built Logistics Marketplace Heatmap Decision Support Tool
         : Combined analytics, automation, and business insight
    2024 : PROJECTS — Built RAG4Konkur local LLM study assistant
         : Explored algorithmic trading systems
         : Deepened Python, backend, automation, and AI application skills
    2024 : PROJECTS — Worked on Autonomous Assembling Robotic Arm simulation
         : Applied deep reinforcement learning to robotics control
    2025 : PROJECTS — Developed Autonomous Budgeting AI Agent thesis project
         : Reinforcement learning for budgeting under uncertainty
    2026 : EDUCATION — Expected completion of M.Sc. in Engineering Management
```

## Option 1.3 — Timeline with emoji-grouped story lanes

```mermaid
timeline
    title Mahriar Gharaghani — Grouped Timeline View with Emojis
    2017 : 🎓 Began B.Sc. in Industrial Engineering
         : Isfahan University of Technology
    2019 : 💼 Project Control Specialist
         : Jahanpars Group
         : Reporting, schedule tracking, and management analysis
    2020 : 💼 Continued project controls and coordination work
    2021 : ⚒️ Expanded practical software foundations through self-driven development
    2022 : ⚒️ Completed freeCodeCamp certifications
         : Responsive Web Design, JavaScript Algorithms and Data Structures
         : Front End Development Libraries, Data Visualization
         : Relational Database, Back End Development and APIs
    2023 : 🎓 Completed B.Sc. in Industrial Engineering
         : Started M.Sc. in Engineering Management
         : Iran University of Science and Technology
    2023 : 💼 Project Management Officer
         : IEIC
         : Led planning and coordination team
    2023 : ⚒️ Built Logistics Marketplace Heatmap Decision Support Tool
         : Combined analytics, automation, and business insight
    2024 : ⚒️ Built RAG4Konkur local LLM study assistant
         : Explored algorithmic trading systems
         : Deepened Python, backend, automation, and AI application skills
    2024 : ⚒️ Worked on Autonomous Assembling Robotic Arm simulation
         : Applied deep reinforcement learning to robotics control
    2025 : ⚒️ Developed Autonomous Budgeting AI Agent thesis project
         : Reinforcement learning for budgeting under uncertainty
    2026 : 🎓 Expected completion of M.Sc. in Engineering Management
```

## Option 1.4 — Refined timeline with icons and duration milestones

Legend: 🎓 Education | 💼 Work | 📜 Certifications | ⚒️ Projects

```mermaid
timeline
    title Career Timeline — Education, Work, Certifications, and Projects
    2017 : 🎓 Started B.Sc. in Industrial Engineering
         : Isfahan University of Technology
    2019 : 💼 Started as Project Control Specialist
         : Jahanpars Group
    2020 : 💼 Finished Project Control Specialist role
         : Strengthened reporting, schedule tracking, and management analysis
    2021 : ⚒️ Expanded software foundations through self-driven development
    2022 : 📜 Completed freeCodeCamp certifications
         : Responsive Web Design and JavaScript Algorithms
         : Front End Libraries, Data Visualization, Databases, and APIs
    2023 : 🎓 Finished B.Sc. in Industrial Engineering
    2023 : 🎓 Started M.Sc. in Engineering Management
         : Iran University of Science and Technology
    2023 : 💼 Joined IEIC as Project Management Officer
         : Led planning and coordination work
    2023 : ⚒️ Built logistics heatmap decision-support tool
    2024 : ⚒️ Built RAG4Konkur study assistant
         : Explored algorithmic trading systems
    2024 : ⚒️ Worked on robotic arm RL simulation
    2025 : ⚒️ Developed Autonomous Budgeting AI Agent thesis
         : Reinforcement learning for budgeting under uncertainty
    2026 : 🎓 Expected completion of M.Sc. in Engineering Management
```

## Option 2 — Career transition flowchart

```mermaid
flowchart TD
    A[Industrial Engineering Foundation<br/>B.Sc. 2017–2023<br/>Isfahan University of Technology] --> B[Project Controls and Operations<br/>Jahanpars Group 2019–2020]
    B --> C[Planning, KPIs, Stakeholder Coordination<br/>IEIC PMO 2023]
    C --> D[Engineering Management M.Sc.<br/>2023–2026<br/>Iran University of Science and Technology]

    A --> E[Self-taught Software Development]
    E --> F[freeCodeCamp Full Stack JavaScript Certifications]
    F --> G[Frontend + Backend + Databases + Data Visualization]

    G --> H[Python Backend and Automation]
    H --> I[Decision-support tools]
    I --> J[Logistics Marketplace Heatmap Tool]

    H --> K[Applied AI and ML]
    K --> L[RAG4Konkur<br/>Local LLM study assistant]
    K --> M[Algorithmic Trading Experiments]
    K --> N[Robotics RL Simulation]
    K --> O[Autonomous Budgeting AI Agent]

    D --> O
    C --> O
    A --> H
```

## Option 3 — Parallel life tracks timeline

```mermaid
flowchart LR
    subgraph EDU[Education]
        EDU1[2017–2023<br/>B.Sc. Industrial Engineering]
        EDU2[2023–2026<br/>M.Sc. Engineering Management]
    end

    subgraph WORK[Professional Experience]
        WORK1[2019–2020<br/>Project Control Specialist<br/>Jahanpars Group]
        WORK2[2023<br/>Project Management Officer<br/>IEIC]
    end

    subgraph CERTS[Certifications]
        CERT1[freeCodeCamp<br/>Responsive Web Design]
        CERT2[JavaScript Algorithms & Data Structures]
        CERT3[Front End Development Libraries]
        CERT4[Data Visualization]
        CERT5[Relational Database]
        CERT6[Back End Development & APIs]
    end

    subgraph PROJECTS[Projects and Passion Projects]
        PROJ1[Logistics Marketplace Heatmap Tool]
        PROJ2[RAG4Konkur]
        PROJ3[Algorithmic Trading Systems]
        PROJ4[Autonomous Robotic Arm RL Simulation]
        PROJ5[Autonomous Budgeting AI Agent]
    end

    EDU1 --> EDU2
    WORK1 --> WORK2
    CERT1 --> CERT2 --> CERT3 --> CERT4 --> CERT5 --> CERT6
    PROJ1 --> PROJ2 --> PROJ3 --> PROJ4 --> PROJ5

    EDU1 -.builds systems thinking.-> WORK1
    WORK1 -.sharpens analytics.-> WORK2
    CERT6 -.supports backend confidence.-> PROJ1
    EDU2 -.research depth.-> PROJ5
    WORK2 -.business planning context.-> PROJ5
    PROJ4 -.RL experience.-> PROJ5
```

## Option 4 — Story arc from operations to AI engineer

```mermaid
flowchart TB
    S1[Industrial Engineering Student] --> S2[Project Control Specialist]
    S2 --> S3[Planning and Reporting Professional]
    S3 --> S4[Project Management Officer]

    S1 --> T1[Web Development Learning]
    T1 --> T2[freeCodeCamp Certifications]
    T2 --> T3[Backend + Databases + APIs]

    S4 --> U1[Business and KPI Understanding]
    T3 --> U2[Python and Automation Systems]
    S1 --> U3[Analytical and Optimization Mindset]

    U1 --> V[Decision-support Software Builder]
    U2 --> V
    U3 --> V

    V --> W1[Heatmap Analytics Tool]
    V --> W2[Algorithmic Trading Experiments]
    V --> W3[RAG4Konkur]

    W2 --> X[AI and Reinforcement Learning Direction]
    W3 --> X
    V --> X

    X --> Y1[Robotic Arm RL Simulation]
    X --> Y2[Autonomous Budgeting AI Agent Thesis]

    Y2 --> Z[Target Profile:<br/>Python Developer / Backend Python / AI Application Engineer]
```

## Option 5 — Compact roadmap with grouped milestones

```mermaid
mindmap
  root((Mahriar Gharaghani))
    Education
      B.Sc. Industrial Engineering
      M.Sc. Engineering Management
        Thesis: Autonomous Budgeting AI Agent
    Professional Experience
      Jahanpars Group
        Project control reports
        Schedule monitoring
        Decision support analysis
      IEIC
        Led 5-person team
        KPI systems
        Contract support
        Debt deadline reduction
    Certifications
      Responsive Web Design
      JavaScript Algorithms and Data Structures
      Front End Development Libraries
      Data Visualization
      Relational Database
      Back End Development and APIs
    Technical Direction
      Python backend
      Automation workflows
      Data analysis and visualization
      AI and ML
      Reinforcement learning
      Local LLM workflows
    Projects
      Logistics heatmap decision tool
      RAG4Konkur
      Algorithmic trading systems
      Robotic arm RL simulation
      Autonomous budgeting AI agent
```

## Recommended picks

- **Best for resumes / portfolios:** Option 1
- **Best for showing career transitions:** Option 2
- **Best for showing everything at once:** Option 3
- **Best for personal-brand storytelling:** Option 4
- **Best for quick visual summary:** Option 5

## Notes

- Some projects in `PYDEV.md` were not tied to exact dates, so they are placed in a logical progression rather than a verified calendar year.
- If you want, I can next turn one of these into a **polished final version** with better styling, shorter labels, Persian year references, or a version optimized for GitHub Markdown rendering.
