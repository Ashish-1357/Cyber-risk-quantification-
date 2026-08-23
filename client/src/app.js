/**
 * Cyber Risk Quantification Platform - Frontend
 * Vanilla JS SPA with Plotly.js visualizations
 */

const API_BASE = window.location.origin.includes('localhost') 
    ? 'http://localhost:8000/api/v1' 
    : '/api/v1';

// State
let appData = {
    assets: [],
    vulnerabilities: [],
    riskScenarios: [],
    controls: [],
    optimization: null,
    dashboardSummary: null
};

// DOM Elements
const views = {
    dashboard: document.getElementById('dashboard-view'),
    assets: document.getElementById('assets-view'),
    vulnerabilities: document.getElementById('vulnerabilities-view'),
    risk: document.getElementById('risk-view'),
    optimize: document.getElementById('optimize-view'),
    controls: document.getElementById('controls-view')
};

const navItems = document.querySelectorAll('.nav-item');
const loading = document.getElementById('loading');

// Initialize
async function init() {
    showLoading();
    try {
        await Promise.all([
            fetchDashboardSummary(),
            fetchAssets(),
            fetchVulnerabilities(),
            fetchRiskScenarios(),
            fetchControls()
        ]);
        renderDashboard();
        renderAssetsTable();
        renderVulnsTable();
        renderRiskCharts();
        renderControlsTable();
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to load data. Is the server running?');
    } finally {
        hideLoading();
    }
}

// API Helpers
async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}

async function apiPost(endpoint, data) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}

// Data Fetching
async function fetchDashboardSummary() {
    appData.dashboardSummary = await apiGet('/dashboard/summary');
}

async function fetchAssets() {
    appData.assets = await apiGet('/assets?limit=500');
}

async function fetchVulnerabilities() {
    appData.vulnerabilities = await apiGet('/vulnerabilities?limit=500');
}

async function fetchRiskScenarios() {
    appData.riskScenarios = await apiGet('/risk/scenarios');
}

async function fetchControls() {
    appData.controls = await apiGet('/controls');
}

// Navigation
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const viewName = item.dataset.view;
        switchView(viewName);
        navItems.forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        document.getElementById('page-title').textContent = 
            viewName.charAt(0).toUpperCase() + viewName.slice(1);
    });
});

function switchView(viewName) {
    Object.values(views).forEach(v => v.classList.remove('active'));
    views[viewName].classList.add('active');
}

// Dashboard Rendering
function renderDashboard() {
    const summary = appData.dashboardSummary;
    if (!summary) return;

    document.getElementById('risk-score').textContent = summary.risk_score.toFixed(1);
    document.getElementById('baseline-ale').textContent = formatCurrency(summary.baseline_ale);
    document.getElementById('residual-risk').textContent = formatCurrency(summary.residual_risk);
    document.getElementById('total-assets').textContent = summary.total_assets.toLocaleString();
    document.getElementById('total-vulns').textContent = summary.total_vulnerabilities.toLocaleString();
    document.getElementById('portfolio-roi').textContent = summary.portfolio_roi.toFixed(0) + '%';

    // Risk Scenarios Chart
    const scenarios = appData.riskScenarios;
    const scenarioNames = scenarios.map(s => s.scenario_name);
    const scenarioAle = scenarios.map(s => s.ale_mean);
    const scenarioVar = scenarios.map(s => s.ale_var_95);

    Plotly.newPlot('risk-scenarios-chart', [
        { x: scenarioNames, y: scenarioAle, type: 'bar', name: 'Expected ALE', marker: { color: '#3498db' } },
        { x: scenarioNames, y: scenarioVar, type: 'bar', name: 'VaR 95%', marker: { color: '#e74c3c', opacity: 0.6 } }
    ], {
        barmode: 'group',
        margin: { t: 20, b: 80 },
        xaxis: { tickangle: -30 },
        yaxis: { title: 'Amount ($)' },
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    }, { responsive: true });

    // Asset Criticality Pie
    const criticalityCounts = {};
    appData.assets.forEach(a => {
        criticalityCounts[a.criticality] = (criticalityCounts[a.criticality] || 0) + 1;
    });

    Plotly.newPlot('asset-criticality-chart', [{
        values: Object.values(criticalityCounts),
        labels: Object.keys(criticalityCounts),
        type: 'pie',
        marker: {
            colors: ['#dc2626', '#ea580c', '#ca8a04', '#16a34a']
        },
        textinfo: 'label+percent',
        hole: 0.3
    }], {
        margin: { t: 10, b: 10 },
        showlegend: false
    }, { responsive: true });

    // Investment Breakdown (will be populated after optimization)
    renderInvestmentChart();

    // Scenario Analysis
    renderScenarioAnalysis();

    // Portfolio Chart
    renderPortfolioChart();
}

function renderInvestmentChart() {
    const categories = {};
    appData.controls.forEach(c => {
        categories[c.category] = (categories[c.category] || 0) + c.total_5year_cost;
    });

    Plotly.newPlot('investment-chart', [{
        values: Object.values(categories),
        labels: Object.keys(categories),
        type: 'pie',
        hole: 0.4,
        textinfo: 'label+percent'
    }], {
        margin: { t: 10, b: 10 },
        showlegend: false
    }, { responsive: true });
}

async function renderScenarioAnalysis() {
    try {
        const data = await apiGet('/optimize/scenario-analysis?min_budget=500000&max_budget=5000000&steps=20');

        Plotly.newPlot('scenario-analysis-chart', [
            {
                x: data.map(d => d.budget),
                y: data.map(d => d.risk_reduction),
                mode: 'lines+markers',
                name: 'Risk Reduction',
                line: { color: '#2ecc71', width: 3 },
                fill: 'tozeroy',
                fillcolor: 'rgba(46, 204, 113, 0.1)'
            },
            {
                x: data.map(d => d.budget),
                y: data.map(d => d.residual_risk),
                mode: 'lines+markers',
                name: 'Residual Risk',
                line: { color: '#e74c3c', width: 2 },
                yaxis: 'y2'
            }
        ], {
            margin: { t: 20, b: 50 },
            xaxis: { title: 'Budget ($)' },
            yaxis: { title: 'Risk Reduction ($)', side: 'left' },
            yaxis2: { title: 'Residual Risk ($)', side: 'right', overlaying: 'y' },
            showlegend: true,
            legend: { orientation: 'h', y: 1.1 }
        }, { responsive: true });
    } catch (e) {
        console.error('Scenario analysis error:', e);
    }
}

function renderPortfolioChart() {
    if (!appData.optimization) return;

    const selected = appData.optimization.selected_controls;
    const names = selected.map(c => c.name);
    const reductions = selected.map(c => c.risk_reduction || 0);
    const costs = selected.map(c => c.total_5year_cost);

    Plotly.newPlot('portfolio-chart', [
        {
            x: names,
            y: reductions,
            type: 'bar',
            name: 'Risk Reduction',
            marker: { color: '#3498db' }
        },
        {
            x: names,
            y: costs,
            type: 'bar',
            name: '5-Year Cost',
            marker: { color: '#e74c3c', opacity: 0.6 }
        }
    ], {
        barmode: 'group',
        margin: { t: 20, b: 120 },
        xaxis: { tickangle: -45 },
        yaxis: { title: 'Amount ($)' },
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    }, { responsive: true });
}

// Assets Table
function renderAssetsTable() {
    const tbody = document.querySelector('#assets-table tbody');
    tbody.innerHTML = appData.assets.map(asset => `
        <tr>
            <td>${asset.id}</td>
            <td>${asset.name}</td>
            <td>${asset.type}</td>
            <td><span class="badge-${asset.criticality}">${asset.criticality}</span></td>
            <td>${asset.business_unit}</td>
            <td>${formatCurrency(asset.annual_revenue_impact)}</td>
            <td>${asset.cloud_provider}</td>
        </tr>
    `).join('');
}

// Vulnerabilities Table
function renderVulnsTable() {
    const tbody = document.querySelector('#vulns-table tbody');
    tbody.innerHTML = appData.vulnerabilities.map(vuln => `
        <tr>
            <td>${vuln.id}</td>
            <td>${vuln.cve_id}</td>
            <td>${vuln.asset_name}</td>
            <td>${vuln.cvss_score}</td>
            <td><span class="badge-${vuln.asset_criticality}">${vuln.contextual_risk_score}</span></td>
            <td>${vuln.exploit_available ? '✅' : '❌'}</td>
            <td>${vuln.patch_available ? '✅' : '❌'}</td>
            <td>${formatCurrency(vuln.remediation_cost)}</td>
        </tr>
    `).join('');
}

// Risk Charts
function renderRiskCharts() {
    // Monte Carlo Distribution
    const scenarios = appData.riskScenarios;
    const traces = scenarios.map((s, i) => ({
        x: Array.from({length: 1000}, () => 
            s.ale_mean + (Math.random() - 0.5) * s.ale_std * 4
        ),
        type: 'histogram',
        name: s.scenario_name,
        opacity: 0.6,
        nbinsx: 50
    }));

    Plotly.newPlot('monte-carlo-chart', traces, {
        margin: { t: 20, b: 50 },
        xaxis: { title: 'Annualized Loss Expectancy ($)' },
        yaxis: { title: 'Frequency' },
        barmode: 'overlay',
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    }, { responsive: true });

    // VaR Chart
    const varData = [];
    scenarios.forEach(s => {
        varData.push({ scenario: s.scenario_name, metric: 'VaR 90%', value: s.ale_mean + s.ale_std * 1.28 });
        varData.push({ scenario: s.scenario_name, metric: 'VaR 95%', value: s.ale_var_95 });
        varData.push({ scenario: s.scenario_name, metric: 'VaR 99%', value: s.ale_var_99 });
        varData.push({ scenario: s.scenario_name, metric: 'CVaR 95%', value: s.ale_cvar_95 });
    });

    const metrics = ['VaR 90%', 'VaR 95%', 'VaR 99%', 'CVaR 95%'];
    const colors = ['#3498db', '#f39c12', '#e74c3c', '#9b59b6'];

    Plotly.newPlot('var-chart', metrics.map((m, i) => ({
        x: scenarios.map(s => s.scenario_name),
        y: varData.filter(d => d.metric === m).map(d => d.value),
        type: 'bar',
        name: m,
        marker: { color: colors[i] }
    })), {
        barmode: 'group',
        margin: { t: 20, b: 80 },
        xaxis: { tickangle: -30 },
        yaxis: { title: 'Amount ($)' },
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    }, { responsive: true });

    // Vulnerability Heatmap
    const heatmapData = {};
    appData.vulnerabilities.forEach(v => {
        const key = v.asset_criticality + '|' + (v.exploit_available ? 'yes' : 'no');
        if (!heatmapData[key]) heatmapData[key] = [];
        heatmapData[key].push(v.contextual_risk_score);
    });

    const criticalities = ['critical', 'high', 'medium', 'low'];
    const exploitStatus = ['No Exploit', 'Exploit Available'];
    const z = criticalities.map(c => 
        exploitStatus.map((e, i) => {
            const key = c + '|' + (i === 1 ? 'yes' : 'no');
            const values = heatmapData[key] || [0];
            return values.reduce((a, b) => a + b, 0) / values.length;
        })
    );

    Plotly.newPlot('vuln-heatmap', [{
        z: z,
        x: exploitStatus,
        y: criticalities,
        type: 'heatmap',
        colorscale: 'RdYlGn_r',
        showscale: true
    }], {
        margin: { t: 20, b: 50 },
        xaxis: { title: 'Exploit Status' },
        yaxis: { title: 'Asset Criticality' }
    }, { responsive: true });
}

// Controls Table
function renderControlsTable() {
    const tbody = document.querySelector('#controls-table tbody');
    tbody.innerHTML = appData.controls.map(ctrl => `
        <tr>
            <td>${ctrl.id}</td>
            <td>${ctrl.name}</td>
            <td>${ctrl.category}</td>
            <td>${(ctrl.effectiveness * 100).toFixed(0)}%</td>
            <td>${formatCurrency(ctrl.implementation_cost)}</td>
            <td>${formatCurrency(ctrl.annual_cost)}</td>
            <td>${formatCurrency(ctrl.total_5year_cost)}</td>
            <td>${ctrl.coverage.length} scenarios</td>
        </tr>
    `).join('');
}

// Optimization
document.getElementById('run-optimization').addEventListener('click', async () => {
    showLoading();
    try {
        const request = {
            budget: parseFloat(document.getElementById('opt-budget').value),
            staff_capacity: parseInt(document.getElementById('opt-staff').value),
            risk_appetite: parseFloat(document.getElementById('opt-appetite').value),
            method: document.getElementById('opt-method').value
        };

        const result = await apiPost('/optimize', request);
        appData.optimization = result;

        // Update results panel
        document.getElementById('res-controls').textContent = result.num_controls;
        document.getElementById('res-investment').textContent = formatCurrency(result.total_investment);
        document.getElementById('res-reduction').textContent = formatCurrency(result.total_risk_reduction);
        document.getElementById('res-residual').textContent = formatCurrency(result.residual_risk);
        document.getElementById('res-roi').textContent = result.portfolio_roi.toFixed(0) + '%';
        document.getElementById('res-npv').textContent = formatCurrency(result.npv);

        // Update selected controls list
        const listEl = document.getElementById('selected-controls-list');
        listEl.innerHTML = result.selected_controls.map(c => `
            <div class="control-item">
                <span class="control-name">${c.name}</span>
                <span class="control-cost">${formatCurrency(c.total_5year_cost)}</span>
            </div>
        `).join('');

        // Update charts
        renderPortfolioChart();
        renderParetoChart();

    } catch (error) {
        console.error('Optimization error:', error);
        showError('Optimization failed: ' + error.message);
    } finally {
        hideLoading();
    }
});

async function renderParetoChart() {
    try {
        const data = await apiGet('/optimize/scenario-analysis?min_budget=500000&max_budget=5000000&steps=20');

        Plotly.newPlot('pareto-chart', [
            {
                x: data.map(d => d.investment),
                y: data.map(d => d.residual_risk),
                mode: 'lines+markers',
                name: 'Pareto Frontier',
                line: { color: '#9b59b6', width: 3 },
                marker: { size: 8 }
            }
        ], {
            margin: { t: 20, b: 50 },
            xaxis: { title: 'Investment ($)' },
            yaxis: { title: 'Residual Risk ($)' },
            shapes: [{
                type: 'line',
                x0: 0, x1: 1, xref: 'paper',
                y0: parseFloat(document.getElementById('opt-appetite').value),
                y1: parseFloat(document.getElementById('opt-appetite').value),
                line: { color: 'red', dash: 'dash', width: 2 }
            }],
            annotations: [{
                x: 0.95, y: parseFloat(document.getElementById('opt-appetite').value),
                xref: 'paper', text: 'Risk Appetite',
                showarrow: false, font: { color: 'red' }
            }]
        }, { responsive: true });
    } catch (e) {
        console.error('Pareto chart error:', e);
    }
}

// Filters
document.getElementById('asset-search').addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#assets-table tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
});

document.getElementById('asset-criticality-filter').addEventListener('change', (e) => {
    const value = e.target.value;
    const rows = document.querySelectorAll('#assets-table tbody tr');
    rows.forEach(row => {
        if (!value) { row.style.display = ''; return; }
        const criticality = row.querySelector('td:nth-child(4)').textContent.trim().toLowerCase();
        row.style.display = criticality === value ? '' : 'none';
    });
});

document.getElementById('vuln-search').addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#vulns-table tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
});

document.getElementById('critical-only').addEventListener('change', (e) => {
    const checked = e.target.checked;
    const rows = document.querySelectorAll('#vulns-table tbody tr');
    rows.forEach(row => {
        if (!checked) { row.style.display = ''; return; }
        const score = parseFloat(row.querySelector('td:nth-child(5)').textContent);
        row.style.display = score >= 7 ? '' : 'none';
    });
});

// Refresh
document.getElementById('refresh-btn').addEventListener('click', init);

// Export
document.getElementById('export-btn').addEventListener('click', () => {
    const data = {
        timestamp: new Date().toISOString(),
        summary: appData.dashboardSummary,
        scenarios: appData.riskScenarios,
        optimization: appData.optimization
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cyber-risk-report-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
});

// Utilities
function formatCurrency(value) {
    if (value === undefined || value === null) return '--';
    if (value >= 1e9) return '$' + (value / 1e9).toFixed(1) + 'B';
    if (value >= 1e6) return '$' + (value / 1e6).toFixed(1) + 'M';
    if (value >= 1e3) return '$' + (value / 1e3).toFixed(1) + 'K';
    return '$' + value.toFixed(0);
}

function showLoading() { loading.classList.remove('hidden'); }
function hideLoading() { loading.classList.add('hidden'); }

function showError(message) {
    alert('Error: ' + message);
}

// Start
init();
