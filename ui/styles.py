import streamlit as st


def cargar_estilos():

    st.html(
        """
        <style>

        :root {

            --bg: #0B0F17;

            --sidebar: #0A0E16;

            --surface: #111827;

            --surface-2: #1A2234;

            --border: #1E293B;

            --border-active: #25334D;

            --primary: #3B82F6;

            --primary-hover: #2563EB;

            --success: #10B981;

            --warning: #F59E0B;

            --danger: #EF4444;

            --text: #F8FAFC;

            --text-secondary: #94A3B8;

            --text-muted: #64748B;
        }


        /* =====================================================
           BASE
           ===================================================== */

        .stApp {

            background: var(--bg);

            color: var(--text);
        }


        #MainMenu {

            visibility: hidden;
        }


        footer {

            visibility: hidden;
        }


        header[data-testid="stHeader"] {

            background: transparent;
        }


        .block-container {

            max-width: 1500px;

            padding-top: 2rem;

            padding-bottom: 4rem;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {

            background: var(--sidebar);

            border-right:
                1px solid var(--border);
        }


        .brand-title {

            color: var(--text);

            font-size: 1.45rem;

            font-weight: 750;
        }


        .brand-version {

            color: var(--primary);
        }


        .brand-subtitle {

            color: var(--text-muted);

            font-size: 0.70rem;

            font-weight: 600;

            letter-spacing: 0.10em;

            text-transform: uppercase;

            margin-bottom: 1.4rem;
        }


        /* =====================================================
           PAGE
           ===================================================== */

        .page-kicker {

            color: var(--primary);

            font-size: 0.70rem;

            font-weight: 700;

            letter-spacing: 0.12em;

            margin-bottom: 0.55rem;
        }


        .page-title {

            color: var(--text);

            font-size: 2.5rem;

            font-weight: 750;

            line-height: 1.1;
        }


        .page-subtitle {

            color: var(--text-secondary);

            max-width: 820px;

            line-height: 1.65;

            margin-top: 0.8rem;

            margin-bottom: 1.8rem;
        }


        /* =====================================================
           CARDS
           ===================================================== */

        .diag-card {

            background: var(--surface);

            border:
                1px solid var(--border);

            border-radius: 16px;

            padding: 1.25rem;

            margin-bottom: 1rem;
        }


        .card-title {

            color: var(--text);

            font-size: 1.05rem;

            font-weight: 650;
        }


        .card-caption {

            color: var(--text-secondary);

            font-size: 0.82rem;

            margin-top: 0.3rem;
        }


        /* =====================================================
           STATUS
           ===================================================== */

        .status-online {

            display: inline-flex;

            align-items: center;

            gap: 0.45rem;

            padding:
                0.35rem 0.65rem;

            border-radius: 999px;

            color: var(--success);

            background:
                rgba(
                    16,
                    185,
                    129,
                    0.10
                );

            border:
                1px solid
                rgba(
                    16,
                    185,
                    129,
                    0.30
                );

            font-size: 0.70rem;

            font-weight: 700;
        }


        .status-dot {

            width: 7px;

            height: 7px;

            border-radius: 50%;

            background:
                var(--success);
        }


        /* =====================================================
           AGENTS
           ===================================================== */

        .agent-card {

            min-height: 165px;

            background: var(--surface);

            border:
                1px solid var(--border);

            border-radius: 16px;

            padding: 1rem;
        }


        .agent-card.running {

            border-color:
                rgba(
                    59,
                    130,
                    246,
                    0.65
                );

            box-shadow:
                0 0 16px -2px
                rgba(
                    59,
                    130,
                    246,
                    0.30
                );
        }


        .agent-card.completed {

            border-color:
                rgba(
                    16,
                    185,
                    129,
                    0.45
                );
        }


        .agent-icon {

            font-size: 1.5rem;

            margin-bottom: 0.7rem;
        }


        .agent-name {

            color: var(--text);

            font-size: 0.88rem;

            font-weight: 650;

            margin-bottom: 0.35rem;
        }


        .agent-desc {

            color: var(--text-secondary);

            font-size: 0.75rem;

            min-height: 45px;
        }


        .agent-status {

            color: var(--text-muted);

            margin-top: 0.85rem;

            font-family:
                Consolas,
                monospace;

            font-size: 0.64rem;

            font-weight: 600;
        }


        .agent-status-running {

            color: var(--primary);
        }


        .agent-status-completed {

            color: var(--success);
        }


        /* =====================================================
           STRUCTURED DIAGNOSTIC
           ===================================================== */

        .diagnostic-hero {

            display: flex;

            justify-content:
                space-between;

            align-items: center;

            gap: 1rem;

            background:
                var(--surface);

            border:
                1px solid var(--border);

            border-radius: 16px;

            padding:
                1.3rem 1.4rem;

            margin-top: 1.8rem;

            margin-bottom: 1rem;
        }


        .diagnostic-label {

            color: var(--text-muted);

            font-family:
                Consolas,
                monospace;

            font-size: 0.68rem;

            font-weight: 700;

            letter-spacing: 0.10em;
        }


        .diagnostic-system {

            color: var(--text);

            font-size: 1.45rem;

            font-weight: 700;

            margin-top: 0.25rem;

            text-transform: capitalize;
        }


        /* =====================================================
           RISK
           ===================================================== */

        .risk-badge {

            display: inline-flex;

            align-items: center;

            gap: 0.4rem;

            padding:
                0.45rem 0.75rem;

            border-radius: 999px;

            font-size: 0.72rem;

            font-weight: 750;

            white-space: nowrap;
        }


        .risk-low {

            color: #10B981;

            background:
                rgba(
                    16,
                    185,
                    129,
                    0.12
                );

            border:
                1px solid
                rgba(
                    16,
                    185,
                    129,
                    0.40
                );
        }


        .risk-medium {

            color: #F59E0B;

            background:
                rgba(
                    245,
                    158,
                    11,
                    0.12
                );

            border:
                1px solid
                rgba(
                    245,
                    158,
                    11,
                    0.40
                );
        }


        .risk-high {

            color: #F8FAFC;

            background:
                rgba(
                    239,
                    68,
                    68,
                    0.18
                );

            border:
                1px solid #EF4444;

            box-shadow:
                0 0 18px -4px
                rgba(
                    239,
                    68,
                    68,
                    0.35
                );
        }


        /* =====================================================
           RESULT CARDS
           ===================================================== */

        .result-card {

            background:
                var(--surface);

            border:
                1px solid var(--border);

            border-radius: 16px;

            padding: 1.25rem;

            margin-bottom: 1rem;
        }


        .result-card-title {

            color: var(--text);

            font-size: 1rem;

            font-weight: 700;

            margin-bottom: 0.6rem;
        }


        .result-card-caption {

            color: var(--text-muted);

            font-size: 0.75rem;

            margin-bottom: 0.8rem;
        }


        .result-card-text {

            color: #C2C6D6;

            font-size: 0.88rem;

            line-height: 1.65;
        }


        /* =====================================================
           LISTS
           ===================================================== */

        .diagnostic-list {

            color: #C2C6D6;

            padding-left: 1.2rem;

            margin-bottom: 0;
        }


        .diagnostic-list li {

            margin-bottom: 0.5rem;

            line-height: 1.5;
        }


        /* =====================================================
           TECHNICAL KNOWLEDGE
           ===================================================== */

        .technical-card {

            border-color:
                rgba(
                    59,
                    130,
                    246,
                    0.35
                );
        }


        .technical-source {

            display: inline-block;

            color: var(--primary);

            font-family:
                Consolas,
                monospace;

            font-size: 0.65rem;

            font-weight: 700;

            letter-spacing: 0.06em;

            margin-bottom: 0.75rem;
        }


        /* =====================================================
           SAFETY
           ===================================================== */

        .safety-card {

            border-color:
                rgba(
                    245,
                    158,
                    11,
                    0.30
                );
        }


        .safety-driving {

            color: var(--text);

            font-size: 1.05rem;

            font-weight: 700;

            margin-bottom: 0.6rem;
        }


        .safety-meta {

            color: var(--text-secondary);

            font-size: 0.75rem;

            margin-top: 0.8rem;
        }


        /* =====================================================
           UNCERTAINTY
           ===================================================== */

        .uncertainty-card {

            color: var(--text-secondary);

            background:
                rgba(
                    59,
                    130,
                    246,
                    0.06
                );

            border:
                1px solid
                rgba(
                    59,
                    130,
                    246,
                    0.20
                );

            border-radius: 12px;

            padding: 1rem;

            font-size: 0.78rem;

            line-height: 1.55;

            margin-bottom: 1rem;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {

            background:
                var(--bg) !important;

            border-color:
                var(--border-active) !important;

            border-radius:
                8px !important;
        }


        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {

            color:
                var(--text) !important;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button,
        .stFormSubmitButton > button {

            min-height: 42px;

            border-radius: 8px;

            font-weight: 650;
        }


        .stFormSubmitButton > button {

            background:
                var(--primary);

            color: white;

            border:
                1px solid
                rgba(
                    96,
                    165,
                    250,
                    0.45
                );
        }


        .stFormSubmitButton > button:hover {

            background:
                var(--primary-hover);
        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (
            max-width: 768px
        ) {

            .page-title {

                font-size: 1.9rem;
            }


            .diagnostic-hero {

                flex-direction: column;

                align-items:
                    flex-start;
            }


            .agent-card {

                min-height: auto;
            }
        }

        </style>
        """
    )