"""
🌍 EcoBrain - AI Environmental Command System
A modern, real-time air quality monitoring dashboard with AI insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
import hashlib
from datetime import datetime
import plotly.graph_objects as go
from prophet import Prophet
from air_quality_map import show_india_map
import json
import os
import random
import time
import threading

# ═══════════════════════════════════════════════════════════════
# ⚙️ PAGE CONFIGURATION & THEMING
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EcoBrain",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# 🎨 MODERN & ATTRACTIVE UI STYLING
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* Import Modern Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Vibrant Modern Color Palette */
:root {
    /* Primary Colors - Modern Blue Gradient */
    --primary: #667eea;
    --primary-light: #764ba2;
    --primary-dark: #4c63d2;
    --primary-glow: rgba(102, 126, 234, 0.4);

    /* Secondary Colors - Warm Purple */
    --secondary: #f093fb;
    --secondary-light: #f5576c;
    --secondary-dark: #c44569;

    /* Accent Colors - Electric Green */
    --accent: #00d4ff;
    --accent-light: #00ff88;
    --accent-dark: #00b4d8;
    --accent-glow: rgba(0, 212, 255, 0.6);

    /* Success Colors - Bright Green */
    --success: #00ff88;
    --success-light: #7cffcb;
    --success-dark: #00cc6a;

    /* Warning Colors - Orange */
    --warning: #ffa500;
    --warning-light: #ffb347;
    --warning-dark: #ff8c00;

    /* Danger Colors - Red */
    --danger: #ff4757;
    --danger-light: #ff6b81;
    --danger-dark: #ff3838;

    /* Neutral Colors - Modern Grays */
    --gray-50: #f8fafc;
    --gray-100: #f1f5f9;
    --gray-200: #e2e8f0;
    --gray-300: #cbd5e1;
    --gray-400: #94a3b8;
    --gray-500: #64748b;
    --gray-600: #475569;
    --gray-700: #334155;
    --gray-800: #1e293b;
    --gray-900: #0f172a;

    /* Backgrounds - Dynamic Gradient */
    --bg-primary: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #0c0c0c 100%);
    --bg-secondary: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
    --bg-tertiary: linear-gradient(135deg, #16213e 0%, #0f0f23 100%);
    --bg-card: linear-gradient(135deg, rgba(22, 33, 62, 0.95) 0%, rgba(15, 15, 35, 0.95) 100%);
    --bg-glass: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.05) 100%);
    --bg-overlay: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(245, 143, 251, 0.1) 100%);

    /* Text Colors */
    --text-primary: #ffffff;
    --text-secondary: #e2e8f0;
    --text-muted: #94a3b8;
    --text-accent: #00d4ff;

    /* Shadows - Enhanced */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.15);
    --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.2), 0 4px 12px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.25), 0 8px 20px rgba(0, 0, 0, 0.2);
    --shadow-xl: 0 24px 60px rgba(0, 0, 0, 0.3), 0 12px 30px rgba(0, 0, 0, 0.25);
    --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.4), 0 0 60px rgba(102, 126, 234, 0.2);
    --shadow-neon: 0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(0, 212, 255, 0.3);
}

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Application Background - Dynamic */
.stApp {
    background: var(--bg-primary);
    background-attachment: fixed;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    overflow-x: hidden;
}

/* Animated Background Particles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.05) 0%, transparent 50%);
    animation: float 20s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-10px) rotate(1deg); }
    66% { transform: translateY(10px) rotate(-1deg); }
}

/* Modern Card Design */
.modern-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 32px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 24px;
}

.modern-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
    background-size: 200% 100%;
    animation: gradient-shift 3s ease-in-out infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.modern-card:hover::before {
    opacity: 1;
}

.modern-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--shadow-xl), var(--shadow-glow);
    border-color: rgba(0, 212, 255, 0.3);
}

.modern-card:hover {
    animation: card-pulse 2s ease-in-out infinite;
}

@keyframes card-pulse {
    0%, 100% { box-shadow: var(--shadow-xl), var(--shadow-glow); }
    50% { box-shadow: var(--shadow-xl), var(--shadow-neon); }
}

@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Glass Panel Alternative */
.glass-panel {
    background: var(--bg-glass);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    padding: 32px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: var(--shadow-lg);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.glass-panel::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.03), transparent);
    animation: shimmer 4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.glass-panel:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: var(--shadow-xl), 0 0 40px rgba(0, 212, 255, 0.2);
    border-color: rgba(0, 212, 255, 0.2);
}

/* Typography - Modern & Bold */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em;
    line-height: 1.2;
    margin-bottom: 1.5rem !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

h1 {
    font-size: 3rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, var(--accent), var(--primary-light), var(--secondary));
    background-size: 200% 200%;
    animation: gradient-text 3s ease-in-out infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2rem !important;
}

@keyframes gradient-text {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

h2 {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, var(--accent), var(--secondary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h3 {
    font-size: 1.875rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
}

h4 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

p {
    color: var(--text-secondary) !important;
    line-height: 1.8 !important;
    margin-bottom: 1.5rem !important;
    font-size: 1.1rem !important;
}

/* Modern Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, var(--secondary) 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 16px 32px !important;
    border: none !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    position: relative;
    overflow: hidden;
    font-family: 'Poppins', sans-serif !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.6s ease;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: var(--shadow-xl), 0 0 30px var(--primary-glow) !important;
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary) 50%, var(--accent) 100%) !important;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:active {
    transform: translateY(-2px) scale(1.02) !important;
}

/* Modern Form Elements */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input {
    background: var(--bg-glass) !important;
    color: var(--text-primary) !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-sm) !important;
    backdrop-filter: blur(10px) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.2) !important;
    outline: none !important;
    transform: scale(1.02);
    background: rgba(0, 212, 255, 0.05) !important;
}

/* Modern Metric Cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 24px;
    box-shadow: var(--shadow-md);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    text-align: center;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(245, 143, 251, 0.05));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: var(--shadow-xl), 0 0 30px rgba(0, 212, 255, 0.2);
    border-color: rgba(0, 212, 255, 0.3);
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-value {
    color: var(--accent);
    font-size: 3.5rem;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1rem;
    display: block;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    animation: value-glow 2s ease-in-out infinite alternate;
}

@keyframes value-glow {
    from { text-shadow: 0 0 20px rgba(0, 212, 255, 0.5); }
    to { text-shadow: 0 0 30px rgba(0, 212, 255, 0.8), 0 0 40px rgba(0, 212, 255, 0.4); }
}

.metric-label {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'Poppins', sans-serif;
}

/* Modern Status Badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 12px 24px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.status-badge::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.status-badge:hover::before {
    left: 100%;
}

.status-good {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 106, 0.2));
    color: #00ff88;
    border-color: rgba(0, 255, 136, 0.3);
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
}

.status-moderate {
    background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 140, 0, 0.2));
    color: #ffa500;
    border-color: rgba(255, 165, 0, 0.3);
    box-shadow: 0 0 20px rgba(255, 165, 0, 0.2);
}

.status-poor {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.2), rgba(255, 56, 56, 0.2));
    color: #ff4757;
    border-color: rgba(255, 71, 87, 0.3);
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.2);
}

.status-hazardous {
    background: linear-gradient(135deg, rgba(139, 69, 19, 0.2), rgba(153, 27, 27, 0.2));
    color: #8b4513;
    border-color: rgba(139, 69, 19, 0.3);
    box-shadow: 0 0 20px rgba(139, 69, 19, 0.2);
}

/* Modern Alert Boxes */
.alert-box {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.15), rgba(255, 56, 56, 0.15));
    border: 2px solid rgba(255, 71, 87, 0.3);
    border-left: 6px solid var(--danger);
    padding: 24px 32px;
    border-radius: 20px;
    color: #ff6b81;
    font-weight: 600;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    animation: alert-pulse 2s ease-in-out infinite;
    box-shadow: 0 0 30px rgba(255, 71, 87, 0.2);
}

.alert-box::before {
    content: '🚨';
    position: absolute;
    right: 24px;
    top: 24px;
    font-size: 2rem;
    opacity: 0.8;
    animation: icon-bounce 1s ease-in-out infinite;
}

@keyframes alert-pulse {
    0%, 100% { box-shadow: 0 0 30px rgba(255, 71, 87, 0.2); }
    50% { box-shadow: 0 0 40px rgba(255, 71, 87, 0.4), 0 0 60px rgba(255, 71, 87, 0.2); }
}

@keyframes icon-bounce {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
}

/* Modern Chat Interface */
.stChatMessage {
    background: var(--bg-card) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: var(--shadow-md) !important;
    margin-bottom: 1.5rem !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
}

.stChatMessage:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg) !important;
}

.stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(245, 143, 251, 0.1)) !important;
    border-color: rgba(0, 212, 255, 0.3) !important;
}

/* Modern Sidebar */
.stSidebar {
    background: var(--bg-secondary) !important;
    border-right: 2px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) !important;
}

.stSidebar > div {
    background: transparent !important;
}

/* Modern Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: var(--bg-glass);
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    padding: 16px;
    border-radius: 16px 16px 0 0;
    backdrop-filter: blur(10px);
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 12px 24px;
    font-family: 'Poppins', sans-serif;
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(245, 143, 251, 0.2));
    color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--secondary));
    color: var(--bg-primary);
    font-weight: 700;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    transform: translateY(-2px);
}

/* Modern DataFrames */
.stDataFrame {
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-lg) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.stDataFrame > div > div > div > div {
    background: var(--bg-card) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Modern Charts */
.plotly .main-svg {
    background: transparent !important;
}

.plotly .modebar {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow-md) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Modern Progress Bars */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
    border-radius: 8px !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
}

/* Modern Scrollbars */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg-tertiary);
    border-radius: 8px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--accent), var(--secondary));
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

/* Modern Loading Animation */
@keyframes modern-pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.7;
        transform: scale(1.05);
    }
}

.modern-loading {
    animation: modern-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Modern Focus States */
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    transform: scale(1.02);
    animation: input-glow 2s ease-in-out infinite alternate;
}

@keyframes input-glow {
    from { box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.2); }
    to { box-shadow: 0 0 0 6px rgba(0, 212, 255, 0.4), 0 0 20px rgba(0, 212, 255, 0.2); }
}

/* Modern Responsive Design */
@media (max-width: 768px) {
    .modern-card, .glass-panel {
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 16px;
    }

    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    h2 {
        font-size: 2rem !important;
    }

    h3 {
        font-size: 1.75rem !important;
    }

    .metric-value {
        font-size: 3rem !important;
    }

    .status-badge {
        padding: 10px 20px;
        font-size: 0.8rem;
    }
}

/* Modern Animations */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(40px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.animate-slide-in {
    animation: slideInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.animate-fade-in {
    animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Modern Grid Layouts */
.modern-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.modern-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.modern-grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}

.modern-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
}

/* Modern Spacing Utilities */
.modern-spacing-sm { margin-bottom: 0.75rem; }
.modern-spacing-md { margin-bottom: 1.5rem; }
.modern-spacing-lg { margin-bottom: 2.5rem; }
.modern-spacing-xl { margin-bottom: 3.5rem; }

/* Modern Text Utilities */
.modern-text-sm { font-size: 0.875rem; }
.modern-text-base { font-size: 1rem; }
.modern-text-lg { font-size: 1.25rem; }
.modern-text-xl { font-size: 1.5rem; }

.modern-text-muted { color: var(--text-muted); }
.modern-text-secondary { color: var(--text-secondary); }
.modern-text-accent { color: var(--accent); }

/* Modern Status Indicators */
.status-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 12px;
    box-shadow: 0 0 10px currentColor;
}

.status-indicator.online { color: var(--success); }
.status-indicator.offline { color: var(--danger); }
.status-indicator.warning { color: var(--warning); }

/* Modern Notification Badge */
.notification-badge {
    position: relative;
    display: inline-block;
}

.notification-badge::after {
    content: attr(data-count);
    position: absolute;
    top: -10px;
    right: -10px;
    background: linear-gradient(135deg, var(--danger), var(--warning));
    color: white;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--bg-primary);
    box-shadow: 0 0 15px rgba(255, 71, 87, 0.4);
    animation: badge-pulse 2s ease-in-out infinite;
}

@keyframes badge-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Modern Divider */
.modern-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
    margin: 3rem 0;
    border: none;
    position: relative;
}

.modern-divider::before {
    content: '';
    position: absolute;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 8px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
}

/* Modern Code Blocks */
.stCodeBlock {
    background: var(--bg-glass) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-md) !important;
    backdrop-filter: blur(10px) !important;
}

.stCodeBlock > div > pre {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 12px !important;
}

/* Modern Expander */
.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-sm) !important;
    backdrop-filter: blur(10px) !important;
}

.stExpander > div > div {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* Modern Slider */
.stSlider > div > div > div {
    background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
}

.stSlider > div > div > div > div {
    background: var(--primary) !important;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.4) !important;
}

/* Modern Radio */
.stRadio > div {
    background: var(--bg-glass) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    backdrop-filter: blur(10px) !important;
}

/* Modern Checkbox */
.stCheckbox > div > div > div > div {
    background: var(--bg-glass) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(10px) !important;
}

/* Modern Success/Error Messages */
.stSuccess, .stError, .stWarning, .stInfo {
    background: var(--bg-card) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-md) !important;
    backdrop-filter: blur(10px) !important;
}

.stSuccess {
    border-left-color: var(--success) !important;
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 204, 106, 0.1)) !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
}

.stError {
    border-left-color: var(--danger) !important;
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.1), rgba(255, 56, 56, 0.1)) !important;
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.2) !important;
}

.stWarning {
    border-left-color: var(--warning) !important;
    background: linear-gradient(135deg, rgba(255, 165, 0, 0.1), rgba(255, 140, 0, 0.1)) !important;
    box-shadow: 0 0 20px rgba(255, 165, 0, 0.2) !important;
}

.stInfo {
    border-left-color: var(--info) !important;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.2) !important;
}

/* Modern Container Padding */
.block-container {
    padding-top: 3rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* Modern Full Width Elements */
.full-width {
    width: 100% !important;
}

/* Modern Centered Content */
.centered-content {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
}

/* Modern Hero Section */
.hero-section {
    text-align: center;
    padding: 5rem 3rem;
    background: var(--bg-overlay);
    border-radius: 24px;
    margin-bottom: 3rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: var(--shadow-lg);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(0, 212, 255, 0.05), rgba(245, 143, 251, 0.05));
    animation: hero-shimmer 4s ease-in-out infinite;
}

@keyframes hero-shimmer {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

/* Modern Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.stat-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: var(--shadow-md);
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-8px) scale(1.05);
    box-shadow: var(--shadow-xl), 0 0 30px rgba(0, 212, 255, 0.3);
    border-color: rgba(0, 212, 255, 0.3);
}

.stat-card:hover::before {
    opacity: 1;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1rem;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

.stat-label {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'Poppins', sans-serif;
}

/* Modern Loading States */
.loading-skeleton {
    background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(255, 255, 255, 0.1) 50%, var(--bg-tertiary) 75%);
    background-size: 200% 100%;
    animation: modern-loading 1.5s infinite;
    border-radius: 16px;
}

@keyframes modern-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* Modern Accessibility */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Modern Content Grid */
.content-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 3rem;
    margin: 3rem 0;
}

.dashboard-top {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.dashboard-summary-card {
    position: relative;
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(30, 41, 59, 0.95));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    padding: 2rem;
    box-shadow: var(--shadow-xl);
    overflow: hidden;
}

.dashboard-summary-card::before {
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 180px;
    height: 180px;
    background: rgba(0, 212, 255, 0.12);
    border-radius: 50%;
}

.dashboard-summary-card h2 {
    margin: 0;
    font-size: 4rem;
    letter-spacing: -0.04em;
}

.dashboard-summary-card .summary-label {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
}

.dashboard-summary-card .summary-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
}

.dashboard-summary-card .summary-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--text-secondary);
    font-weight: 600;
}

.dashboard-summary-card .summary-chip strong {
    color: var(--text-primary);
}

.dashboard-small-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}

.small-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    color: var(--text-secondary);
}

.small-card h4 {
    margin: 0 0 0.5rem 0;
    color: var(--text-primary);
}

.small-card .small-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}

.pollutant-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.pollutant-block {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 1rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow-sm);
}

.pollutant-block span {
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.pollutant-block strong {
    color: var(--accent);
    font-size: 1.2rem;
}

.top-panel {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1rem 2rem;
    margin-bottom: 2rem;
}

.top-panel .chip {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.75rem 1rem;
    border-radius: 999px;
    font-size: 0.95rem;
    font-weight: 600;
}

@media (max-width: 992px) {
    .dashboard-top {
        grid-template-columns: 1fr;
    }

    .dashboard-small-grid {
        grid-template-columns: 1fr;
    }
}

.content-section {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.section-title {
    color: var(--text-primary);
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Poppins', sans-serif;
}

.section-title::before {
    content: '';
    width: 6px;
    height: 24px;
    background: linear-gradient(135deg, var(--accent), var(--secondary));
    border-radius: 3px;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

/* Modern Chat Messages */
.chat-message {
    padding: 1.5rem;
    border-radius: 20px;
    margin: 0.75rem 0;
    max-width: 85%;
    line-height: 1.6;
    font-size: 1rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.chat-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.chat-message:hover::before {
    opacity: 1;
}

.user-message {
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 6px;
    box-shadow: var(--shadow-lg);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.ai-message {
    background: var(--bg-card);
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom-left-radius: 6px;
    box-shadow: var(--shadow-md);
    backdrop-filter: blur(10px);
}

/* Modern Pollutant Items */
.pollutant-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
    border-radius: 8px;
    margin: 0.25rem 0;
}

.pollutant-item:hover {
    background: rgba(0, 212, 255, 0.05);
    border-radius: 12px;
    padding-left: 1rem;
    margin: 0.25rem -1rem;
    border-bottom-color: rgba(0, 212, 255, 0.3);
    transform: translateX(4px);
}

.pollutant-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 1.1rem;
}

.pollutant-value {
    font-weight: 700;
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

/* Modern Alert Box */
.alert-box {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.15), rgba(255, 56, 56, 0.15));
    border: 2px solid rgba(255, 71, 87, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    color: #ff6b81;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    animation: modern-alert-pulse 2s infinite;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.alert-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 71, 87, 0.1), transparent);
    animation: alert-shimmer 3s ease-in-out infinite;
}

@keyframes modern-alert-pulse {
    0%, 100% {
        box-shadow: var(--shadow-lg), 0 0 20px rgba(255, 71, 87, 0.2);
        transform: scale(1);
    }
    50% {
        box-shadow: var(--shadow-xl), 0 0 40px rgba(255, 71, 87, 0.4);
        transform: scale(1.01);
    }
}

@keyframes alert-shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

/* Modern Metric Value */
.metric-value {
    font-size: 4rem;
    font-weight: 900;
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    margin: 1.5rem 0;
    text-align: center;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    animation: metric-glow 3s ease-in-out infinite alternate;
}

@keyframes metric-glow {
    from {
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transform: scale(1);
    }
    to {
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.8), 0 0 40px rgba(0, 212, 255, 0.4);
        transform: scale(1.02);
    }
}

/* Modern Status Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}

.status-badge::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.status-badge:hover::before {
    left: 100%;
}

.status-good {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 106, 0.2));
    color: #00ff88;
    border-color: rgba(0, 255, 136, 0.3);
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}

.status-moderate {
    background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 140, 0, 0.2));
    color: #ffa500;
    border-color: rgba(255, 165, 0, 0.3);
    box-shadow: 0 0 20px rgba(255, 165, 0, 0.3);
}

.status-unhealthy {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.2), rgba(255, 56, 56, 0.2));
    color: #ff4757;
    border-color: rgba(255, 71, 87, 0.3);
    box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
}

.status-hazardous {
    background: linear-gradient(135deg, rgba(139, 69, 19, 0.2), rgba(153, 27, 27, 0.2));
    color: #8b4513;
    border-color: rgba(139, 69, 19, 0.3);
    box-shadow: 0 0 20px rgba(139, 69, 19, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 📊 SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "logged_in": False,
        "user": "",
        "has_anomaly": False,
        "latest_aqi": 0,
        "chat_history": [],
        "selected_city": "Mumbai",
        "selected_pollutant": "PM2.5",
        "language": "en",
        "notifications_enabled": False,
        "theme": "dark",
        "auto_refresh": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═══════════════════════════════════════════════════════════════
# 🌐 MULTI-LANGUAGE SUPPORT
# ═══════════════════════════════════════════════════════════════
class LanguageManager:
    """Handle multi-language support for the application"""
    
    LANGUAGES = {
        "en": {
            "name": "English",
            "flag": "🇺🇸",
            "dashboard": "Dashboard",
            "analytics": "Analytics", 
            "ai_assistant": "AI Assistant",
            "login": "Login",
            "signup": "Sign Up",
            "logout": "Logout",
            "username": "Username",
            "password": "Password",
            "confirm_password": "Confirm Password",
            "create_account": "Create Account",
            "invalid_credentials": "Invalid credentials",
            "user_exists": "User exists",
            "account_created": "Account created!",
            "welcome_back": "Welcome Back",
            "choose_username": "Choose Username",
            "create_password": "Create Password",
            "ecobrain_command": "EcoBrain Command Center",
            "real_time_intelligence": "Real-time Environmental Intelligence Dashboard",
            "select_city": "Select City",
            "select_pollutant": "Select Pollutant",
            "live_status": "Live Environmental Status",
            "ai_insight": "AI Insight",
            "risk_score": "Risk Score",
            "alert": "ALERT",
            "pollution_spike": "Sudden Pollution Spike Detected",
            "live_monitoring": "Live Monitoring",
            "day_trend": "7-Day Trend",
            "ai_forecast": "AI Forecast (Prophet Model)",
            "ask_about_quality": "Ask about air quality...",
            "ecobrain_assistant": "EcoBrain AI Assistant",
            "ask_me_about": "Ask me anything about air quality, pollution, and health impacts",
            "live_city_comparison": "Live City Comparison",
            "navigation": "Navigation",
            "auto_refresh": "Auto-refresh (30s)",
            "toggle_theme": "Toggle Theme",
            "language": "Language",
            "notifications": "Notifications",
            "enable_notifications": "Enable Notifications",
            "notification_enabled": "Notifications enabled! You'll receive alerts for high AQI levels.",
            "notification_denied": "Notifications denied. You won't receive alerts.",
            "install_app": "Install App",
            "install_description": "Install EcoBrain as a PWA for offline access and better experience",
            "offline_mode": "Offline Mode",
            "data_cached": "Data cached for offline use",
            "good": "GOOD",
            "moderate": "MODERATE", 
            "unhealthy": "UNHEALTHY",
            "hazardous": "HAZARDOUS",
            "safe": "Safe",
            "caution": "Moderate caution required",
            "avoid": "High pollution risk. Avoid outdoor exposure",
            "air_quality": "Air Quality",
            "pollution": "Pollution",
            "health": "Health",
            "recommendations": "Recommendations",
            "check_aqi": "Check AQI before exercising outdoors",
            "use_masks": "Use N95 masks on high AQI days",
            "close_windows": "Keep windows closed during pollution peaks",
            "air_purifiers": "Use air purifiers indoors",
            "monitor_updates": "Monitor daily AQI updates"
        },
        "hi": {
            "name": "हिंदी",
            "flag": "🇮🇳",
            "dashboard": "डैशबोर्ड",
            "analytics": "विश्लेषण",
            "ai_assistant": "एआई सहायक",
            "login": "लॉगिन",
            "signup": "साइन अप",
            "logout": "लॉग आउट",
            "username": "उपयोगकर्ता नाम",
            "password": "पासवर्ड",
            "confirm_password": "पासवर्ड की पुष्टि करें",
            "create_account": "खाता बनाएं",
            "invalid_credentials": "अमान्य क्रेडेंशियल्स",
            "user_exists": "उपयोगकर्ता मौजूद है",
            "account_created": "खाता बनाया गया!",
            "welcome_back": "वापसी पर स्वागत है",
            "choose_username": "उपयोगकर्ता नाम चुनें",
            "create_password": "पासवर्ड बनाएं",
            "ecobrain_command": "एकोब्रेन कमांड सेंटर",
            "real_time_intelligence": "रियल-टाइम पर्यावरणीय इंटेलिजेंस डैशबोर्ड",
            "select_city": "शहर चुनें",
            "select_pollutant": "प्रदूषक चुनें",
            "live_status": "लाइव पर्यावरणीय स्थिति",
            "ai_insight": "एआई अंतर्दृष्टि",
            "risk_score": "जोखिम स्कोर",
            "alert": "अलर्ट",
            "pollution_spike": "अचानक प्रदूषण स्पाइक का पता चला",
            "live_monitoring": "लाइव मॉनिटरिंग",
            "day_trend": "7-दिन का रुझान",
            "ai_forecast": "एआई पूर्वानुमान (प्रॉफेट मॉडल)",
            "ask_about_quality": "वायु गुणवत्ता के बारे में पूछें...",
            "ecobrain_assistant": "एकोब्रेन एआई सहायक",
            "ask_me_about": "वायु गुणवत्ता, प्रदूषण और स्वास्थ्य प्रभावों के बारे में कुछ भी पूछें",
            "live_city_comparison": "लाइव शहर तुलना",
            "navigation": "नेविगेशन",
            "auto_refresh": "ऑटो-रिफ्रेश (30सेकंड)",
            "toggle_theme": "थीम टॉगल करें",
            "language": "भाषा",
            "notifications": "सूचनाएं",
            "enable_notifications": "सूचनाएं सक्षम करें",
            "notification_enabled": "सूचनाएं सक्षम! आपको उच्च AQI स्तर के लिए अलर्ट मिलेंगे।",
            "notification_denied": "सूचनाएं अस्वीकृत। आपको अलर्ट नहीं मिलेंगे।",
            "install_app": "ऐप इंस्टॉल करें",
            "install_description": "ऑफलाइन एक्सेस और बेहतर अनुभव के लिए EcoBrain को PWA के रूप में इंस्टॉल करें",
            "offline_mode": "ऑफलाइन मोड",
            "data_cached": "ऑफलाइन उपयोग के लिए डेटा कैश किया गया",
            "good": "अच्छा",
            "moderate": "मध्यम",
            "unhealthy": "अस्वास्थ्यकर",
            "hazardous": "खतरनाक",
            "safe": "सुरक्षित",
            "caution": "मध्यम सावधानी आवश्यक",
            "avoid": "उच्च प्रदूषण जोखिम। बाहर निकलने से बचें",
            "air_quality": "वायु गुणवत्ता",
            "pollution": "प्रदूषण",
            "health": "स्वास्थ्य",
            "recommendations": "सिफारिशें",
            "check_aqi": "बाहर व्यायाम करने से पहले AQI जांचें",
            "use_masks": "उच्च AQI दिनों में N95 मास्क का उपयोग करें",
            "close_windows": "प्रदूषण के चरम समय में खिड़कियां बंद रखें",
            "air_purifiers": "अंदर एयर प्यूरिफायर का उपयोग करें",
            "monitor_updates": "दैनिक AQI अपडेट की निगरानी करें"
        },
        "es": {
            "name": "Español",
            "flag": "🇪🇸",
            "dashboard": "Panel",
            "analytics": "Análisis",
            "ai_assistant": "Asistente IA",
            "login": "Iniciar Sesión",
            "signup": "Registrarse",
            "logout": "Cerrar Sesión",
            "username": "Usuario",
            "password": "Contraseña",
            "confirm_password": "Confirmar Contraseña",
            "create_account": "Crear Cuenta",
            "invalid_credentials": "Credenciales inválidas",
            "user_exists": "Usuario existe",
            "account_created": "¡Cuenta creada!",
            "welcome_back": "Bienvenido de vuelta",
            "choose_username": "Elegir Usuario",
            "create_password": "Crear Contraseña",
            "ecobrain_command": "Centro de Comando EcoBrain",
            "real_time_intelligence": "Panel de Inteligencia Ambiental en Tiempo Real",
            "select_city": "Seleccionar Ciudad",
            "select_pollutant": "Seleccionar Contaminante",
            "live_status": "Estado Ambiental en Vivo",
            "ai_insight": "Perspectiva IA",
            "risk_score": "Puntuación de Riesgo",
            "alert": "ALERTA",
            "pollution_spike": "Pico de Contaminación Súbito Detectado",
            "live_monitoring": "Monitoreo en Vivo",
            "day_trend": "Tendencia de 7 Días",
            "ai_forecast": "Pronóstico IA (Modelo Prophet)",
            "ask_about_quality": "Preguntar sobre calidad del aire...",
            "ecobrain_assistant": "Asistente IA EcoBrain",
            "ask_me_about": "Pregúntame cualquier cosa sobre calidad del aire, contaminación e impactos en la salud",
            "live_city_comparison": "Comparación de Ciudades en Vivo",
            "navigation": "Navegación",
            "auto_refresh": "Auto-refresco (30s)",
            "toggle_theme": "Cambiar Tema",
            "language": "Idioma",
            "notifications": "Notificaciones",
            "enable_notifications": "Habilitar Notificaciones",
            "notification_enabled": "¡Notificaciones habilitadas! Recibirás alertas para niveles altos de AQI.",
            "notification_denied": "Notificaciones denegadas. No recibirás alertas.",
            "install_app": "Instalar App",
            "install_description": "Instala EcoBrain como PWA para acceso offline y mejor experiencia",
            "offline_mode": "Modo Offline",
            "data_cached": "Datos almacenados en caché para uso offline",
            "good": "BUENO",
            "moderate": "MODERADO",
            "unhealthy": "INSALUBRE",
            "hazardous": "PELIGROSO",
            "safe": "Seguro",
            "caution": "Precaución moderada requerida",
            "avoid": "Alto riesgo de contaminación. Evitar exposición al aire libre",
            "air_quality": "Calidad del Aire",
            "pollution": "Contaminación",
            "health": "Salud",
            "recommendations": "Recomendaciones",
            "check_aqi": "Verificar AQI antes de hacer ejercicio al aire libre",
            "use_masks": "Usar máscaras N95 en días de AQI alto",
            "close_windows": "Mantener ventanas cerradas durante picos de contaminación",
            "air_purifiers": "Usar purificadores de aire en interiores",
            "monitor_updates": "Monitorear actualizaciones diarias de AQI"
        }
    }
    
    @staticmethod
    def get_text(key, lang="en"):
        """Get translated text for given key and language"""
        return LanguageManager.LANGUAGES.get(lang, LanguageManager.LANGUAGES["en"]).get(key, key)
    
    @staticmethod
    def get_available_languages():
        """Get list of available languages"""
        return [(code, lang["name"], lang["flag"]) for code, lang in LanguageManager.LANGUAGES.items()]

# ═══════════════════════════════════════════════════════════════
# 🔔 REAL-TIME NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════
class NotificationManager:
    """Handle browser notifications and alerts"""
    
    @staticmethod
    def request_permission():
        """Request notification permission from browser"""
        permission_js = """
        <script>
        if ('Notification' in window) {
            if (Notification.permission === 'default') {
                Notification.requestPermission().then(function(permission) {
                    console.log('Notification permission:', permission);
                });
            }
        }
        </script>
        """
        st.markdown(permission_js, unsafe_allow_html=True)
    
    @staticmethod
    def show_notification(title, body, icon="🌍"):
        """Show browser notification"""
        notification_js = f"""
        <script>
        if ('Notification' in window && Notification.permission === 'granted') {{
            new Notification('{title}', {{
                body: '{body}',
                icon: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9Ijk2IiBmaWxsPSIjMGYxNzJhIi8+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9IjgwIiBmaWxsPSIjM0I4MkY2Ii8+Cjx0ZXh0IHg9Ijk2IiB5PSI5OCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEwNCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuMzVlbSI+{icon}</dGV4dD4KPC9zdmc+',
                badge: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9Ijk2IiBmaWxsPSIjMGYxNzJhIi8+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9IjgwIiBmaWxsPSIjM0I4MkY2Ii8+Cjx0ZXh0IHg9Ijk2IiB5PSI5OCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEwNCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuMzVlbSI+{icon}</dGV4dD4KPC9zdmc+',
                vibrate: [100, 50, 100],
                requireInteraction: false,
                silent: false
            }});
        }}
        </script>
        """
        st.markdown(notification_js, unsafe_allow_html=True)
    
    @staticmethod
    def check_aqi_alerts(aqi_value, city, lang="en"):
        """Check if AQI warrants an alert and show notification"""
        if aqi_value >= 150:  # High pollution alert
            title = LanguageManager.get_text("alert", lang)
            body = f"{LanguageManager.get_text('pollution_spike', lang)} in {city} (AQI: {aqi_value})"
            NotificationManager.show_notification(title, body, "🚨")
        elif aqi_value >= 100:  # Moderate alert
            title = "EcoBrain Alert"
            body = f"Moderate air quality in {city} (AQI: {aqi_value})"
            NotificationManager.show_notification(title, body, "⚠️")

# ═══════════════════════════════════════════════════════════════
# 📱 PWA FEATURES
# ═══════════════════════════════════════════════════════════════
class PWAManager:
    """Handle Progressive Web App functionality"""
    
    @staticmethod
    def register_service_worker():
        """Register service worker for PWA functionality"""
        sw_js = """
        <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/sw.js')
                    .then(function(registration) {
                        console.log('Service Worker registered successfully:', registration.scope);
                        
                        // Check for updates
                        registration.addEventListener('updatefound', function() {
                            const newWorker = registration.installing;
                            newWorker.addEventListener('statechange', function() {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    // New version available
                                    console.log('New version available!');
                                }
                            });
                        });
                    })
                    .catch(function(error) {
                        console.log('Service Worker registration failed:', error);
                    });
            });
        }
        </script>
        """
        st.markdown(sw_js, unsafe_allow_html=True)
    
    @staticmethod
    def add_manifest_link():
        """Add manifest link to head"""
        manifest_link = """
        <link rel="manifest" href="/manifest.json">
        <meta name="theme-color" content="#3B82F6">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="EcoBrain">
        <link rel="apple-touch-icon" href="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9Ijk2IiBmaWxsPSIjMGYxNzJhIi8+CjxjaXJjbGUgY3g9Ijk2IiBjeT0iOTYiIHI9IjgwIiBmaWxsPSIjM0I4MkY2Ii8+Cjx0ZXh0IHg9Ijk2IiB5PSI5OCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEwNCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuMzVlbSI+🌍PC90ZXh0Pgo8L3N2Zz4=">
        """
        st.markdown(manifest_link, unsafe_allow_html=True)
    
    @staticmethod
    def show_install_prompt():
        """Show PWA install prompt"""
        install_js = """
        <script>
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button
            const installButton = document.createElement('button');
            installButton.innerHTML = '📱 Install App';
            installButton.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #3B82F6, #00ffaa);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
                z-index: 1000;
            `;
            
            installButton.addEventListener('click', () => {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    }
                    deferredPrompt = null;
                    installButton.remove();
                });
            });
            
            document.body.appendChild(installButton);
            
            // Auto-hide after 10 seconds
            setTimeout(() => {
                if (installButton.parentNode) {
                    installButton.remove();
                }
            }, 10000);
        });
        </script>
        """
        st.markdown(install_js, unsafe_allow_html=True)
    
    @staticmethod
    def check_online_status():
        """Check and display online/offline status"""
        status_js = """
        <script>
        function updateOnlineStatus() {
            const statusDiv = document.getElementById('online-status');
            if (statusDiv) {
                if (navigator.onLine) {
                    statusDiv.innerHTML = '🟢 Online';
                    statusDiv.style.color = '#00ffaa';
                } else {
                    statusDiv.innerHTML = '🔴 Offline';
                    statusDiv.style.color = '#ff4d4d';
                }
            }
        }
        
        window.addEventListener('online', updateOnlineStatus);
        window.addEventListener('offline', updateOnlineStatus);
        updateOnlineStatus();
        </script>
        """
        st.markdown(status_js, unsafe_allow_html=True)
        
        # Display status in sidebar
        online_status = "🟢 Online" if True else "🔴 Offline"  # Simplified for demo
        st.sidebar.markdown(f"<div id='online-status'>{online_status}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🔐 DATABASE FUNCTIONS
# ═══════════════════════════════════════════════════════════════
class UserDB:
    """Handle user authentication and database operations"""
    
    DB_PATH = "users.db"
    
    @staticmethod
    def init():
        """Initialize database"""
        try:
            conn = sqlite3.connect(UserDB.DB_PATH)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Database error: {e}")
    
    @staticmethod
    def hash_password(password):
        """Hash password with SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def register(username, password):
        """Register new user"""
        try:
            conn = sqlite3.connect(UserDB.DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, UserDB.hash_password(password))
            )
            conn.commit()
            conn.close()
            return True, "Account created successfully! ✨"
        except sqlite3.IntegrityError:
            return False, "Username already exists!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user"""
        try:
            conn = sqlite3.connect(UserDB.DB_PATH)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, UserDB.hash_password(password))
            )
            user = c.fetchone()
            conn.close()
            return user is not None
        except Exception as e:
            st.error(f"Auth error: {e}")
            return False

# Initialize database
UserDB.init()

# ═══════════════════════════════════════════════════════════════
# 🌐 API FUNCTIONS
# ═══════════════════════════════════════════════════════════════
class AQIProvider:
    """Handle AQI data fetching from WAQI API"""
    
    CITIES = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Nagpur"]
    POLLUTANTS = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
    POLLUTANT_KEYS = {
        "PM2.5": "pm25",
        "PM10": "pm10",
        "NO2": "no2",
        "CO": "co",
        "SO2": "so2",
        "O3": "o3"
    }
    
    @staticmethod
    def fetch_city_data(city):
        """Fetch AQI data for a specific city"""
        try:
            token = st.secrets.get("WAQI_TOKEN", "")
            if not token:
                return None, None
            
            url = f"https://api.waqi.info/feed/{city}/?token={token}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("status") == "ok":
                city_data = data.get("data", {})
                forecast = city_data.get("forecast", {}).get("daily", {}).get("pm25", [])
                return city_data, forecast
        except Exception as e:
            st.warning(f"Could not fetch data for {city}")
        
        return None, None
    
    @staticmethod
    def fetch_all_cities():
        """Fetch AQI for all major cities"""
        aqi_values = []
        
        for city in AQIProvider.CITIES:
            try:
                data, _ = AQIProvider.fetch_city_data(city)
                if data:
                    aqi_values.append(data.get("aqi", 0))
                else:
                    aqi_values.append(0)
            except:
                aqi_values.append(0)
        
        return pd.DataFrame({
            "City": AQIProvider.CITIES,
            "AQI": aqi_values
        })

# ═══════════════════════════════════════════════════════════════
# 🤖 AI ASSISTANT
# ═══════════════════════════════════════════════════════════════
class AIAssistant:
    """Simple but effective AI assistant for AQI queries"""
    
    @staticmethod
    def get_health_advice(aqi_value, lang="en"):
        """Get practical health advice based on AQI"""
        if aqi_value < 50:
            return f"🟢 **{LanguageManager.get_text('good', lang)}**\n\nThe air is clean and comfortable; enjoy outdoor time while staying hydrated."
        elif aqi_value < 100:
            return f"🟡 **{LanguageManager.get_text('moderate', lang)}**\n\nAir quality is moderate, so sensitive individuals should take light precautions outdoors."
        elif aqi_value < 150:
            return f"🟠 **{LanguageManager.get_text('unhealthy', lang)}**\n\nLimit prolonged outdoor activity and use protection if you need to be outside."
        else:
            return f"⚫ **{LanguageManager.get_text('hazardous', lang)}**\n\nConditions are hazardous. Stay indoors, avoid heavy exertion, and keep air filters running."
    
    @staticmethod
    def get_ai_insight(aqi_value, lang="en"):
        """Get AI insight sentence based on AQI"""
        if aqi_value < 50:
            return "The current air quality is excellent and the environment is healthy for most activities."
        elif aqi_value < 100:
            return "Air quality is acceptable for most people, but some may feel mild discomfort outdoors."
        elif aqi_value < 150:
            return "The air quality is unhealthy for sensitive groups, so consider reducing time outside."
        else:
            return "Air quality is hazardous right now; it’s best to stay indoors and limit exposure."
    
    @staticmethod
    def respond_to_query(prompt, city, aqi_value, lang="en"):
        """Generate AI response to user query"""
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ["aqi", "index", "level"]):
            return f"{LanguageManager.get_text('air_quality', lang)} {LanguageManager.get_text('aqi', lang)}: **{aqi_value}**\n\n{AIAssistant.get_health_advice(aqi_value, lang)}"

        elif any(word in prompt_lower for word in ["safe", "health", "good", "outdoor", "exercise"]):
            return AIAssistant.get_health_advice(aqi_value, lang)

        elif any(word in prompt_lower for word in ["pollution", "pollutant", "particulate"]):
            return f"**{LanguageManager.get_text('pollution', lang)} {LanguageManager.get_text('status', lang)} {city}:**\n\nAQI {LanguageManager.get_text('level', lang)}: {aqi_value}\n\n{AIAssistant.get_health_advice(aqi_value, lang)}"

        elif any(word in prompt_lower for word in ["recommend", "advice", "suggestion"]):
            recommendations = [
                f"🏃 {LanguageManager.get_text('check_aqi', lang)}",
                f"😷 {LanguageManager.get_text('use_masks', lang)}",
                f"🏠 {LanguageManager.get_text('close_windows', lang)}",
                f"💨 {LanguageManager.get_text('air_purifiers', lang)}",
                f"📱 {LanguageManager.get_text('monitor_updates', lang)}"
            ]
            return f"**{LanguageManager.get_text('recommendations', lang)}:**\n\n" + "\n".join(recommendations)

        else:
            return f"{LanguageManager.get_text('ask_me_about', lang)}"
def get_ai_response(prompt, lang="en"):
    """Get AI response for user query"""
    city = st.session_state.get("selected_city", "Mumbai")
    aqi_value = st.session_state.get("latest_aqi", 50)
    return AIAssistant.respond_to_query(prompt, city, aqi_value, lang)

def show_india_map(pollutant):
    """Display India air quality map"""
    try:
        from air_quality_map import show_india_map as render_map
        render_map(pollutant)
    except ImportError:
        st.info("Map module not available. Please ensure air_quality_map.py is present.")
    except Exception as e:
        st.error(f"Error loading map: {str(e)}")

# ═══════════════════════════════════════════════════════════════
def render_aqi_badge(aqi_value, lang="en"):
    """Render AQI status badge with color coding"""
    if aqi_value < 50:
        status_text = LanguageManager.get_text('good', lang)
        status_badge = f"🟢 {status_text}"
    elif aqi_value < 100:
        status_text = LanguageManager.get_text('moderate', lang)
        status_badge = f"🟡 {status_text}"
    elif aqi_value < 150:
        status_text = LanguageManager.get_text('unhealthy', lang)
        status_badge = f"🟠 {status_text}"
    elif aqi_value < 200:
        status_text = LanguageManager.get_text('unhealthy', lang)
        status_badge = f"🔴 {status_text}"
    else:
        status_text = LanguageManager.get_text('hazardous', lang)
        status_badge = f"⚫ {status_text}"
    
    return status_text, status_badge

def create_forecast_chart(forecast_data):
    """Create interactive forecast chart"""
    if not forecast_data:
        st.info("No forecast data available")
        return
    
    try:
        df = pd.DataFrame(forecast_data)
        df["day"] = pd.to_datetime(df["day"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["day"],
            y=df["avg"],
            mode="lines+markers",
            name="Avg PM2.5",
            line=dict(color="#00ffaa", width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating chart: {e}")

def create_prophet_forecast(forecast_data):
    """Create Prophet AI forecast"""
    try:
        df = pd.DataFrame(forecast_data)
        if len(df) < 3:
            st.warning("Insufficient data for forecasting")
            return
        
        df["day"] = pd.to_datetime(df["day"])
        df_prophet = df[["day", "avg"]].copy()
        df_prophet.columns = ["ds", "y"]
        
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        model.fit(df_prophet)
        
        future = model.make_future_dataframe(periods=5)
        forecast = model.predict(future)
        
        fig = go.Figure()
        
        # Actual data
        fig.add_trace(go.Scatter(
            x=df_prophet["ds"],
            y=df_prophet["y"],
            name="Actual",
            line=dict(color="#1b6fce", width=3),
            mode="lines+markers"
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            name="Forecast",
            line=dict(color="#00ffaa", width=3, dash="dash"),
            mode="lines"
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast["ds"].tolist() + forecast["ds"].tolist()[::-1],
            y=forecast["yhat_upper"].tolist() + forecast["yhat_lower"].tolist()[::-1],
            fill="toself",
            name="Confidence Range",
            fillcolor="rgba(0,255,170,0.1)",
            line=dict(width=0),
            showlegend=True
        ))
        
        fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Forecast error: {e}")

# ═══════════════════════════════════════════════════════════════
# 🔐 LOGIN & REGISTRATION PAGE
# ═══════════════════════════════════════════════════════════════
def show_login_page():
    """Render login/registration interface"""
    lang = st.session_state.get("language", "en")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="modern-card" style="margin-top: 60px; text-align: center;">
            <h1>🌍 EcoBrain</h1>
            <p style="color: var(--text-muted); font-size: 1.1rem;">
                AI Environmental Command System
            </p>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 10px;">
                {LanguageManager.get_text('real_time_intelligence', lang)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([f" {LanguageManager.get_text('login', lang)}", f" {LanguageManager.get_text('signup', lang)}"])
        
        with tab1:
            st.subheader(LanguageManager.get_text("welcome_back", lang))
            username = st.text_input(LanguageManager.get_text("username", lang), key="login_user")
            password = st.text_input(LanguageManager.get_text("password", lang), type="password", key="login_pass")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(f"{LanguageManager.get_text('login', lang)}", use_container_width=True):
                    if username and password:
                        if UserDB.authenticate(username, password):
                            st.session_state.logged_in = True
                            st.session_state.user = username
                            st.success("Login successful! ")
                            st.rerun()
                        else:
                            st.error(f"{LanguageManager.get_text('invalid_credentials', lang)}")
                    else:
                        st.warning("Please enter both username and password")
        
        with tab2:
            st.subheader(LanguageManager.get_text("choose_username", lang))
            new_username = st.text_input(LanguageManager.get_text("choose_username", lang), key="signup_user")
            new_password = st.text_input(LanguageManager.get_text("create_password", lang), type="password", key="signup_pass")
            confirm_password = st.text_input(LanguageManager.get_text("confirm_password", lang), type="password", key="signup_confirm")
            
            if st.button(f"✨ {LanguageManager.get_text('create_account', lang)}", use_container_width=True):
                if not new_username or not new_password:
                    st.warning("Please fill all fields")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 6:
                    st.warning("Password must be at least 6 characters")
                else:
                    success, message = UserDB.register(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# ═══════════════════════════════════════════════════════════════
# 📊 DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════
def show_dashboard_page():
    """Render main dashboard"""
    lang = st.session_state.get("language", "en")
    
    # Header
    st.markdown(f"""
    <div class="hero-section animate-slide-in">
        <h1>🌍 {LanguageManager.get_text('ecobrain_command', lang)}</h1>
        <p class="professional-text-lg professional-text-secondary">
            {LanguageManager.get_text('real_time_intelligence', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # City & Pollutant Selection
    col1, col2, col3 = st.columns([1.5, 1.5, 3])
    
    with col1:
        city = st.selectbox(
            f" {LanguageManager.get_text('select_city', lang)}",
            AQIProvider.CITIES,
            key="city_select"
        )
    
    with col2:
        pollutant = st.selectbox(
            f" {LanguageManager.get_text('select_pollutant', lang)}",
            AQIProvider.POLLUTANTS,
            key="pollutant_select"
        )
    
    # Fetch data
    data, forecast = AQIProvider.fetch_city_data(city)
    
    if data:
        # Update session state
        st.session_state.latest_aqi = data.get("aqi", 0)
        
        # Check for notifications
        if st.session_state.notifications_enabled:
            NotificationManager.check_aqi_alerts(st.session_state.latest_aqi, city, lang)
        
        # Main metrics
        iaqi = data.get("iaqi", {})
        pollutant_key = AQIProvider.POLLUTANT_KEYS.get(pollutant, "pm25")
        value = iaqi.get(pollutant_key, {}).get("v", data.get("aqi", 0))
        status_text, status_badge = render_aqi_badge(int(value), lang)
        risk_score = min(100, int(value * 0.8))

        pollutant_items = [
            (name.upper(), int(details.get("v", 0)))
            for name, details in iaqi.items()
            if isinstance(details, dict) and details.get("v") is not None
        ]
        pollutant_html = "".join(
            f'<div class="pollutant-block"><span>{name}</span><strong>{val}</strong></div>'
            for name, val in pollutant_items[:6]
        )

        st.markdown(f"""
        <div class="dashboard-top">
            <div class="dashboard-summary-card animate-fade-in">
                <div class="summary-label">{LanguageManager.get_text('live_status', lang)}</div>
                <h2>{city} • AQI {int(value)}</h2>
                <div class="summary-meta">
                    <span class="summary-chip">{LanguageManager.get_text('pollutant', lang)}: <strong>{pollutant}</strong></span>
                    <span class="summary-chip">{LanguageManager.get_text('status', lang)}: <strong>{status_text}</strong></span>
                    <span class="summary-chip">{LanguageManager.get_text('last_updated', lang)}: <strong>{datetime.now().strftime('%I:%M %p')}</strong></span>
                </div>
            </div>
            <div class="dashboard-summary-card" style="padding: 2rem 1.75rem;">
                <div class="summary-label">{LanguageManager.get_text('health_index', lang)}</div>
                <h2 class="aqi-score">{status_badge}</h2>
                <div class="summary-meta">
                    <span class="summary-chip">{LanguageManager.get_text('risk_score', lang)}: <strong>{risk_score}/100</strong></span>
                    <span class="summary-chip">{LanguageManager.get_text('mode', lang)}: <strong>Live</strong></span>
                </div>
            </div>
        </div>
        <div class="dashboard-small-grid">
            <div class="small-card">
                <h4>{LanguageManager.get_text('current_aqi', lang)}</h4>
                <div class="small-value">{int(value)}</div>
                <p>{LanguageManager.get_text('aqi_explanation', lang)}</p>
            </div>
            <div class="small-card">
                <h4>{LanguageManager.get_text('top_pollutant', lang)}</h4>
                <div class="small-value">{pollutant}</div>
                <p>{LanguageManager.get_text('pollutant_details', lang)}</p>
            </div>
            <div class="small-card">
                <h4>{LanguageManager.get_text('health_advice', lang)}</h4>
                <p>{AIAssistant.get_health_advice(value, lang)}</p>
            </div>
        </div>
        <div class="pollutant-grid">{pollutant_html}</div>
        """, unsafe_allow_html=True)

        st.session_state.has_anomaly = int(value) > 150
        if st.session_state.has_anomaly:
            st.markdown(f"""
            <div class="alert-box">
                🚨 <strong>{LanguageManager.get_text('alert', lang)}:</strong> {LanguageManager.get_text('pollution_spike', lang)} - AQI > 150
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="modern-card">
            <h4>🧠 {LanguageManager.get_text('ai_insight', lang)} {city}</h4>
            <p>{AIAssistant.get_ai_insight(value, lang)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Content Area
        st.markdown('<div class="content-grid">', unsafe_allow_html=True)
        
        # Left Column - Map and Details
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        
        # Map Section
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="section-title"> {pollutant} Distribution Map</h3>', unsafe_allow_html=True)
        try:
            show_india_map(pollutant)
        except Exception as e:
            st.info("Map visualization not available")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # City Comparison
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="section-title">📊 {LanguageManager.get_text("live_city_comparison", lang)}</h3>', unsafe_allow_html=True)
        
        comparison_df = AQIProvider.fetch_all_cities()
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Bar Chart")
            st.bar_chart(comparison_df.set_index("City")["AQI"])
        
        with col_chart2:
            st.subheader("Status Overview")
            # Color-code cities
            comparison_df["Status"] = comparison_df["AQI"].apply(
                lambda x: "🟢 Good" if x < 50 else "🟡 Moderate" if x < 100 else "🟠 Poor"
            )
            st.dataframe(comparison_df[["City", "AQI", "Status"]], use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Right Column - Analytics and AI
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        
        # Analytics Section
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="section-title">📈 {LanguageManager.get_text("analytics", lang)}</h3>', unsafe_allow_html=True)
        
        # Time range selector
        time_range = st.selectbox(
            LanguageManager.get_text("time_range", lang),
            ["24 Hours", "7 Days", "30 Days", "90 Days"],
            key="analytics_time"
        )
        
        # Sample analytics chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(24)),
            y=[random.randint(20, 150) for _ in range(24)],
            mode='lines+markers',
            name='AQI Trend',
            line=dict(color='#2563eb', width=2),
            marker=dict(size=6, color='#2563eb')
        ))
        
        fig.update_layout(
            title="AQI Trend (Last 24 Hours)",
            xaxis_title="Time (Hours)",
            yaxis_title="AQI Value",
            template="plotly_white",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI Assistant Section
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="section-title">🤖 {LanguageManager.get_text("ai_assistant", lang)}</h3>', unsafe_allow_html=True)
        
        # AI Chat Interface
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.ai_messages[-5:]:  # Show last 5 messages
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message ai-message">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        chat_input = st.text_input(
            LanguageManager.get_text("ask_ai", lang),
            key="ai_input",
            placeholder=LanguageManager.get_text("type_message", lang)
        )
        
        if st.button("Send", key="send_ai"):
            if chat_input.strip():
                # Add user message
                st.session_state.ai_messages.append({"role": "user", "content": chat_input})
                
                # Get AI response
                ai_response = get_ai_response(chat_input, lang)
                st.session_state.ai_messages.append({"role": "ai", "content": ai_response})
                
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.error("Unable to fetch data. Please check API connection.")
    
    # Auto-refresh functionality
    if st.session_state.auto_refresh:
        time.sleep(30)
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# 📈 ANALYTICS PAGE
# ═══════════════════════════════════════════════════════════════
def show_analytics_page():
    """Render analytics with forecasting"""
    lang = st.session_state.get("language", "en")
    
    st.markdown(f"### 📈 {LanguageManager.get_text('analytics', lang)}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        city = st.selectbox(
            f"🏙️ {LanguageManager.get_text('select_city', lang)}",
            AQIProvider.CITIES,
            key="analytics_city"
        )
    
    data, forecast = AQIProvider.fetch_city_data(city)
    
    if forecast:
        df_forecast = pd.DataFrame(forecast)
        df_forecast["day"] = pd.to_datetime(df_forecast["day"])
        
        # Anomaly Detection
        if len(df_forecast) > 2:
            df_forecast["z_score"] = (df_forecast["avg"] - df_forecast["avg"].mean()) / df_forecast["avg"].std()
            df_forecast["anomaly"] = df_forecast["z_score"].abs() > 2
            st.session_state.has_anomaly = df_forecast["anomaly"].any()
        
        # Two-column layout
        col1_trend, col2_forecast = st.columns(2)
        
        with col1_trend:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.subheader(f"📊 {LanguageManager.get_text('day_trend', lang)}")
            st.line_chart(df_forecast.set_index("day")["avg"])
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2_forecast:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.subheader(f"🤖 {LanguageManager.get_text('ai_forecast', lang)}")
            create_prophet_forecast(forecast)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Anomaly Information
        if st.session_state.has_anomaly:
            anomalies = df_forecast[df_forecast["anomaly"]]["day"].tolist()
            st.markdown(f"""
            <div class="alert-box">
                ⚠️ Anomalies detected on: {', '.join([d.strftime('%Y-%m-%d') for d in anomalies])}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No forecast data available for this city")

# ═══════════════════════════════════════════════════════════════
# 🤖 AI ASSISTANT PAGE
# ═══════════════════════════════════════════════════════════════
def show_assistant_page():
    """Render AI assistant chat interface"""
    lang = st.session_state.get("language", "en")
    
    st.markdown(f"""
    <div class="modern-card">
        <h3>🧠 {LanguageManager.get_text('ecobrain_assistant', lang)}</h3>
        <p style="color: var(--text-muted);">
            {LanguageManager.get_text('ask_me_about', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # User input
    user_input = st.chat_input(LanguageManager.get_text("ask_about_quality", lang))
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate AI response
        try:
            ai_response = AIAssistant.respond_to_query(
                user_input,
                st.session_state.selected_city,
                st.session_state.latest_aqi,
                lang
            )
        except Exception as e:
            ai_response = f"⚠️ Error generating response: {str(e)}"
        
        # Add assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        with st.chat_message("assistant"):
            st.markdown(ai_response)

# ═══════════════════════════════════════════════════════════════
# 🎯 MAIN APPLICATION LOGIC
# ═══════════════════════════════════════════════════════════════
def main():
    """Main application entry point"""
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Sidebar Navigation
        with st.sidebar:
            st.markdown(f"""
            <div class="modern-card" style="text-align: center;">
                <h3> {st.session_state.user}</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    {datetime.now().strftime('%B %d, %Y')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Language Selection
            st.markdown("---")
            lang_options = LanguageManager.get_available_languages()
            lang_display = [f"{flag} {name}" for code, name, flag in lang_options]
            lang_codes = [code for code, name, flag in lang_options]
            
            current_lang_idx = lang_codes.index(st.session_state.language) if st.session_state.language in lang_codes else 0
            
            selected_lang_display = st.selectbox(
                f"{LanguageManager.get_text('language', st.session_state.language)} 🌐",
                lang_display,
                index=current_lang_idx,
                key="lang_selector"
            )
            
            # Update language based on selection
            selected_lang_idx = lang_display.index(selected_lang_display)
            st.session_state.language = lang_codes[selected_lang_idx]
            lang = st.session_state.language
            
            # Notifications Toggle
            st.markdown("---")
            if st.checkbox(LanguageManager.get_text("enable_notifications", lang), 
                          value=st.session_state.notifications_enabled, key="notif_toggle"):
                st.session_state.notifications_enabled = True
                NotificationManager.request_permission()
                st.success(LanguageManager.get_text("notification_enabled", lang))
            else:
                st.session_state.notifications_enabled = False
            
            # PWA Status
            st.markdown("---")
            PWAManager.check_online_status()
            
            # Auto-refresh toggle
            st.markdown("---")
            st.session_state.auto_refresh = st.checkbox(
                LanguageManager.get_text("auto_refresh", lang), 
                value=st.session_state.auto_refresh,
                key="auto_refresh_toggle"
            )
            
            st.markdown("---")
            
            page_options = [
                LanguageManager.get_text("dashboard", lang),
                LanguageManager.get_text("analytics", lang), 
                LanguageManager.get_text("ai_assistant", lang)
            ]
            
            page = st.radio(
                LanguageManager.get_text("navigation", lang),
                page_options,
                key="nav_radio"
            )
            
            # Map page names back to English for routing
            page_map = {
                LanguageManager.get_text("dashboard", lang): "Dashboard",
                LanguageManager.get_text("analytics", lang): "Analytics",
                LanguageManager.get_text("ai_assistant", lang): "AI Assistant"
            }
            page = page_map.get(page, page)
            
            st.markdown("---")
            
            if st.button(f" {LanguageManager.get_text('logout', lang)}", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.chat_history = []
                st.rerun()
        
        # Page Router
        if page == "Dashboard":
            show_dashboard_page()
        elif page == "Analytics":
            show_analytics_page()
        elif page == "AI Assistant":
            show_assistant_page()

# ═══════════════════════════════════════════════════════════════
# 🚀 RUN APPLICATION
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Initialize PWA features
    PWAManager.add_manifest_link()
    PWAManager.register_service_worker()
    PWAManager.show_install_prompt()
    
    main()

