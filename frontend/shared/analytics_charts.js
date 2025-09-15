/**
 * PACT Analytics Charts
 * =====================
 * 
 * Reusable chart components for engagement and performance visualization.
 * Provides real-time updating charts for both student and teacher interfaces.
 */

class PACTChartManager {
    constructor() {
        this.charts = new Map();
        this.defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        };
        
        this.colorScheme = {
            primary: '#3498db',
            secondary: '#2c3e50',
            success: '#27ae60',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#17a2b8',
            light: '#f8f9fa',
            dark: '#343a40'
        };
        
        this.log('📊 Chart Manager initialized');
    }
    
    // Engagement Charts
    createEngagementLineChart(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            this.log(`❌ Canvas element ${canvasId} not found`);
            return null;
        }
        
        const ctx = canvas.getContext('2d');
        const config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Engagement Level',
                    data: [],
                    borderColor: this.colorScheme.primary,
                    backgroundColor: this.colorScheme.primary + '20',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                ...this.defaultOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: (value) => Math.round(value * 100) + '%'
                        },
                        grid: {
                            color: '#e0e0e0'
                        }
                    },
                    x: {
                        grid: {
                            color: '#e0e0e0'
                        }
                    }
                },
                plugins: {
                    ...this.defaultOptions.plugins,
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `Engagement: ${Math.round(context.parsed.y * 100)}%`;
                            }
                        }
                    }
                },
                ...options
            }
        };
        
        const chart = new Chart(ctx, config);
        const chartWrapper = new EngagementChart(chart, canvasId);
        this.charts.set(canvasId, chartWrapper);
        
        this.log(`📈 Engagement chart created: ${canvasId}`);
        return chartWrapper;
    }
    
    createClassroomOverviewChart(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            this.log(`❌ Canvas element ${canvasId} not found`);
            return null;
        }
        
        const ctx = canvas.getContext('2d');
        const config = {
            type: 'doughnut',
            data: {
                labels: ['High Engagement', 'Medium Engagement', 'Low Engagement', 'Inactive'],
                datasets: [{
                    data: [0, 0, 0, 0],
                    backgroundColor: [
                        this.colorScheme.success,
                        this.colorScheme.warning,
                        this.colorScheme.danger,
                        '#cccccc'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                ...this.defaultOptions,
                cutout: '60%',
                plugins: {
                    ...this.defaultOptions.plugins,
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const label = context.label;
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${label}: ${value} students (${percentage}%)`;
                            }
                        }
                    }
                },
                ...options
            }
        };
        
        const chart = new Chart(ctx, config);
        const chartWrapper = new ClassroomOverviewChart(chart, canvasId);
        this.charts.set(canvasId, chartWrapper);
        
        this.log(`🍩 Classroom overview chart created: ${canvasId}`);
        return chartWrapper;
    }
    
    createProgressBarChart(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            this.log(`❌ Canvas element ${canvasId} not found`);
            return null;
        }
        
        const ctx = canvas.getContext('2d');
        const config = {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Progress',
                    data: [],
                    backgroundColor: this.colorScheme.success + '80',
                    borderColor: this.colorScheme.success,
                    borderWidth: 1
                }]
            },
            options: {
                ...this.defaultOptions,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: (value) => value + '%'
                        }
                    }
                },
                plugins: {
                    ...this.defaultOptions.plugins,
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `Progress: ${context.parsed.x}%`;
                            }
                        }
                    }
                },
                ...options
            }
        };
        
        const chart = new Chart(ctx, config);
        const chartWrapper = new ProgressChart(chart, canvasId);
        this.charts.set(canvasId, chartWrapper);
        
        this.log(`📊 Progress chart created: ${canvasId}`);
        return chartWrapper;
    }
    
    createAdaptationTimelineChart(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            this.log(`❌ Canvas element ${canvasId} not found`);
            return null;
        }
        
        const ctx = canvas.getContext('2d');
        const config = {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Engagement Drop',
                    data: [],
                    backgroundColor: this.colorScheme.danger,
                    borderColor: this.colorScheme.danger,
                    pointRadius: 6
                }, {
                    label: 'Confusion Detected',
                    data: [],
                    backgroundColor: this.colorScheme.warning,
                    borderColor: this.colorScheme.warning,
                    pointRadius: 6
                }, {
                    label: 'Mastery Achieved',
                    data: [],
                    backgroundColor: this.colorScheme.success,
                    borderColor: this.colorScheme.success,
                    pointRadius: 6
                }]
            },
            options: {
                ...this.defaultOptions,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'minute',
                            displayFormats: {
                                minute: 'HH:mm'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Engagement Level'
                        },
                        ticks: {
                            callback: (value) => Math.round(value * 100) + '%'
                        }
                    }
                },
                plugins: {
                    ...this.defaultOptions.plugins,
                    tooltip: {
                        callbacks: {
                            title: (context) => {
                                return new Date(context[0].parsed.x).toLocaleTimeString();
                            },
                            label: (context) => {
                                const adaptationType = context.dataset.label;
                                const engagement = Math.round(context.parsed.y * 100);
                                return `${adaptationType}: ${engagement}% engagement`;
                            }
                        }
                    }
                },
                ...options
            }
        };
        
        const chart = new Chart(ctx, config);
        const chartWrapper = new AdaptationTimelineChart(chart, canvasId);
        this.charts.set(canvasId, chartWrapper);
        
        this.log(`⚡ Adaptation timeline chart created: ${canvasId}`);
        return chartWrapper;
    }
    
    // Utility Methods
    getChart(canvasId) {
        return this.charts.get(canvasId);
    }
    
    destroyChart(canvasId) {
        const chartWrapper = this.charts.get(canvasId);
        if (chartWrapper) {
            chartWrapper.destroy();
            this.charts.delete(canvasId);
            this.log(`🗑️ Chart destroyed: ${canvasId}`);
        }
    }
    
    destroyAllCharts() {
        this.charts.forEach((chart, id) => {
            chart.destroy();
        });
        this.charts.clear();
        this.log('🗑️ All charts destroyed');
    }
    
    log(...args) {
        console.log('[PACT Charts]', ...args);
    }
}

// Individual Chart Classes
class EngagementChart {
    constructor(chartInstance, canvasId) {
        this.chart = chartInstance;
        this.canvasId = canvasId;
        this.maxDataPoints = 20;
        this.data = [];
    }
    
    addDataPoint(timestamp, engagement, label = null) {
        const timeLabel = label || new Date(timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        this.chart.data.labels.push(timeLabel);
        this.chart.data.datasets[0].data.push(engagement);
        
        // Keep only recent data points
        if (this.chart.data.labels.length > this.maxDataPoints) {
            this.chart.data.labels.shift();
            this.chart.data.datasets[0].data.shift();
        }
        
        this.chart.update('none');
        
        // Store for analysis
        this.data.push({ timestamp, engagement, label: timeLabel });
        if (this.data.length > this.maxDataPoints) {
            this.data.shift();
        }
    }
    
    updateLatestPoint(engagement) {
        if (this.chart.data.datasets[0].data.length > 0) {
            const lastIndex = this.chart.data.datasets[0].data.length - 1;
            this.chart.data.datasets[0].data[lastIndex] = engagement;
            this.chart.update('none');
        }
    }
    
    setThresholds(low = 0.3, high = 0.8) {
        // Add threshold lines
        this.chart.options.plugins.annotation = {
            annotations: {
                lowThreshold: {
                    type: 'line',
                    yMin: low,
                    yMax: low,
                    borderColor: '#e74c3c',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    label: {
                        content: 'Low Engagement',
                        enabled: true,
                        position: 'end'
                    }
                },
                highThreshold: {
                    type: 'line',
                    yMin: high,
                    yMax: high,
                    borderColor: '#27ae60',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    label: {
                        content: 'High Engagement',
                        enabled: true,
                        position: 'end'
                    }
                }
            }
        };
        this.chart.update();
    }
    
    getAverageEngagement() {
        const data = this.chart.data.datasets[0].data;
        if (data.length === 0) return 0;
        
        const sum = data.reduce((acc, val) => acc + val, 0);
        return sum / data.length;
    }
    
    getEngagementTrend() {
        const data = this.chart.data.datasets[0].data;
        if (data.length < 2) return 'stable';
        
        const recent = data.slice(-5); // Last 5 points
        const early = recent.slice(0, Math.floor(recent.length / 2));
        const late = recent.slice(Math.floor(recent.length / 2));
        
        const earlyAvg = early.reduce((acc, val) => acc + val, 0) / early.length;
        const lateAvg = late.reduce((acc, val) => acc + val, 0) / late.length;
        
        const diff = lateAvg - earlyAvg;
        
        if (diff > 0.1) return 'improving';
        if (diff < -0.1) return 'declining';
        return 'stable';
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

class ClassroomOverviewChart {
    constructor(chartInstance, canvasId) {
        this.chart = chartInstance;
        this.canvasId = canvasId;
    }
    
    updateStudentCounts(highEngagement, mediumEngagement, lowEngagement, inactive) {
        this.chart.data.datasets[0].data = [
            highEngagement,
            mediumEngagement, 
            lowEngagement,
            inactive
        ];
        this.chart.update();
    }
    
    updateFromStudentData(students) {
        let high = 0, medium = 0, low = 0, inactive = 0;
        
        students.forEach(student => {
            const engagement = student.engagementLevel || 0;
            
            if (engagement > 0.8) high++;
            else if (engagement > 0.5) medium++;
            else if (engagement > 0.2) low++;
            else inactive++;
        });
        
        this.updateStudentCounts(high, medium, low, inactive);
        
        return { high, medium, low, inactive, total: students.length };
    }
    
    getInsights() {
        const data = this.chart.data.datasets[0].data;
        const total = data.reduce((acc, val) => acc + val, 0);
        
        if (total === 0) return 'No students active';
        
        const percentages = data.map(val => (val / total) * 100);
        const [high, medium, low, inactive] = percentages;
        
        if (high > 60) return 'Excellent classroom engagement!';
        if (low + inactive > 50) return 'Many students need attention';
        if (medium > 50) return 'Good overall engagement';
        return 'Mixed engagement levels';
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

class ProgressChart {
    constructor(chartInstance, canvasId) {
        this.chart = chartInstance;
        this.canvasId = canvasId;
    }
    
    updateStudentProgress(studentData) {
        const labels = studentData.map(student => student.name);
        const progress = studentData.map(student => 
            Math.round((student.knowledgeLevel || 0) * 100)
        );
        
        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = progress;
        
        // Color code based on progress
        this.chart.data.datasets[0].backgroundColor = progress.map(value => {
            if (value >= 80) return '#27ae60'; // Green
            if (value >= 60) return '#f39c12'; // Orange
            if (value >= 40) return '#e67e22'; // Dark orange
            return '#e74c3c'; // Red
        });
        
        this.chart.update();
    }
    
    addStudent(studentName, progress) {
        this.chart.data.labels.push(studentName);
        this.chart.data.datasets[0].data.push(progress);
        
        // Update colors
        const progressValue = this.chart.data.datasets[0].data;
        this.chart.data.datasets[0].backgroundColor = progressValue.map(value => {
            if (value >= 80) return '#27ae60';
            if (value >= 60) return '#f39c12';
            if (value >= 40) return '#e67e22';
            return '#e74c3c';
        });
        
        this.chart.update();
    }
    
    updateStudentProgress(studentName, newProgress) {
        const index = this.chart.data.labels.indexOf(studentName);
        if (index !== -1) {
            this.chart.data.datasets[0].data[index] = newProgress;
            
            // Update color for this student
            const colors = this.chart.data.datasets[0].backgroundColor;
            if (newProgress >= 80) colors[index] = '#27ae60';
            else if (newProgress >= 60) colors[index] = '#f39c12';
            else if (newProgress >= 40) colors[index] = '#e67e22';
            else colors[index] = '#e74c3c';
            
            this.chart.update();
        }
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

class AdaptationTimelineChart {
    constructor(chartInstance, canvasId) {
        this.chart = chartInstance;
        this.canvasId = canvasId;
        this.adaptationTypes = {
            'engagement_drop': 0,
            'confusion_detected': 1,
            'mastery_achieved': 2
        };
    }
    
    addAdaptationEvent(timestamp, adaptationType, engagementLevel, studentName = '') {
        const datasetIndex = this.adaptationTypes[adaptationType];
        
        if (datasetIndex !== undefined) {
            this.chart.data.datasets[datasetIndex].data.push({
                x: timestamp,
                y: engagementLevel,
                studentName: studentName
            });
            
            this.chart.update();
        }
    }
    
    clearOldEvents(maxAge = 30 * 60 * 1000) { // 30 minutes
        const cutoffTime = Date.now() - maxAge;
        
        this.chart.data.datasets.forEach(dataset => {
            dataset.data = dataset.data.filter(point => point.x > cutoffTime);
        });
        
        this.chart.update();
    }
    
    getAdaptationStats() {
        const stats = {};
        
        this.chart.data.datasets.forEach((dataset, index) => {
            const adaptationType = Object.keys(this.adaptationTypes)[index];
            stats[adaptationType] = {
                count: dataset.data.length,
                label: dataset.label
            };
        });
        
        return stats;
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

// Real-time Chart Updater
class RealTimeChartUpdater {
    constructor(chartManager) {
        this.chartManager = chartManager;
        this.updateIntervals = new Map();
        this.dataSubscriptions = new Map();
    }
    
    startAutoUpdate(chartId, updateFunction, interval = 5000) {
        this.stopAutoUpdate(chartId); // Clear existing interval
        
        const intervalId = setInterval(() => {
            try {
                updateFunction();
            } catch (error) {
                console.error(`Chart update error for ${chartId}:`, error);
            }
        }, interval);
        
        this.updateIntervals.set(chartId, intervalId);
    }
    
    stopAutoUpdate(chartId) {
        const intervalId = this.updateIntervals.get(chartId);
        if (intervalId) {
            clearInterval(intervalId);
            this.updateIntervals.delete(chartId);
        }
    }
    
    subscribeToWebSocketData(chartId, websocketClient, eventType, updateFunction) {
        const unsubscribe = websocketClient.on(eventType, (data) => {
            try {
                updateFunction(data);
            } catch (error) {
                console.error(`WebSocket chart update error for ${chartId}:`, error);
            }
        });
        
        this.dataSubscriptions.set(chartId, unsubscribe);
    }
    
    unsubscribeFromWebSocketData(chartId) {
        const unsubscribe = this.dataSubscriptions.get(chartId);
        if (unsubscribe) {
            unsubscribe();
            this.dataSubscriptions.delete(chartId);
        }
    }
    
    destroy() {
        // Stop all auto updates
        this.updateIntervals.forEach(intervalId => clearInterval(intervalId));
        this.updateIntervals.clear();
        
        // Unsubscribe from all WebSocket data
        this.dataSubscriptions.forEach(unsubscribe => unsubscribe());
        this.dataSubscriptions.clear();
    }
}

// Chart Theme Manager
class ChartThemeManager {
    constructor() {
        this.themes = {
            light: {
                backgroundColor: '#ffffff',
                textColor: '#333333',
                gridColor: '#e0e0e0',
                primary: '#3498db',
                success: '#27ae60',
                warning: '#f39c12',
                danger: '#e74c3c'
            },
            dark: {
                backgroundColor: '#2c3e50',
                textColor: '#ecf0f1',
                gridColor: '#34495e',
                primary: '#5dade2',
                success: '#58d68d',
                warning: '#f7dc6f',
                danger: '#ec7063'
            },
            colorBlind: {
                backgroundColor: '#ffffff',
                textColor: '#333333',
                gridColor: '#e0e0e0',
                primary: '#1f77b4',
                success: '#2ca02c',
                warning: '#ff7f0e',
                danger: '#d62728'
            }
        };
        
        this.currentTheme = 'light';
    }
    
    applyTheme(chartManager, themeName) {
        if (!this.themes[themeName]) {
            console.warn(`Theme ${themeName} not found`);
            return;
        }
        
        this.currentTheme = themeName;
        const theme = this.themes[themeName];
        
        // Update chart manager's color scheme
        chartManager.colorScheme = {
            primary: theme.primary,
            success: theme.success,
            warning: theme.warning,
            danger: theme.danger,
            background: theme.backgroundColor,
            text: theme.textColor,
            grid: theme.gridColor
        };
        
        // Update all existing charts
        chartManager.charts.forEach(chartWrapper => {
            this.updateChartTheme(chartWrapper.chart, theme);
        });
    }
    
    updateChartTheme(chart, theme) {
        // Update dataset colors
        chart.data.datasets.forEach(dataset => {
            if (dataset.borderColor === chart.options.defaultColors?.primary) {
                dataset.borderColor = theme.primary;
            }
            if (dataset.backgroundColor?.includes(chart.options.defaultColors?.primary)) {
                dataset.backgroundColor = theme.primary + '20';
            }
        });
        
        // Update grid colors
        if (chart.options.scales) {
            Object.values(chart.options.scales).forEach(scale => {
                if (scale.grid) {
                    scale.grid.color = theme.gridColor;
                }
            });
        }
        
        chart.update();
    }
}

// Performance Monitor for Charts
class ChartPerformanceMonitor {
    constructor() {
        this.metrics = new Map();
        this.isMonitoring = false;
    }
    
    startMonitoring(chartId) {
        this.metrics.set(chartId, {
            updateCount: 0,
            totalUpdateTime: 0,
            lastUpdate: Date.now(),
            averageUpdateTime: 0
        });
    }
    
    recordUpdate(chartId, updateTime) {
        const metrics = this.metrics.get(chartId);
        if (metrics) {
            metrics.updateCount++;
            metrics.totalUpdateTime += updateTime;
            metrics.averageUpdateTime = metrics.totalUpdateTime / metrics.updateCount;
            metrics.lastUpdate = Date.now();
        }
    }
    
    getPerformanceReport() {
        const report = {};
        
        this.metrics.forEach((metrics, chartId) => {
            report[chartId] = {
                updateCount: metrics.updateCount,
                averageUpdateTime: Math.round(metrics.averageUpdateTime * 100) / 100,
                lastUpdate: new Date(metrics.lastUpdate).toLocaleTimeString(),
                performance: metrics.averageUpdateTime < 16 ? 'good' : 
                           metrics.averageUpdateTime < 33 ? 'fair' : 'poor'
            };
        });
        
        return report;
    }
}

// Factory Functions
function createStudentEngagementChart(canvasId, options = {}) {
    const chartManager = new PACTChartManager();
    return chartManager.createEngagementLineChart(canvasId, {
        plugins: {
            title: {
                display: true,
                text: 'Your Learning Engagement'
            }
        },
        ...options
    });
}

function createTeacherClassroomCharts(config = {}) {
    const chartManager = new PACTChartManager();
    const charts = {};
    
    if (config.engagementCanvasId) {
        charts.engagement = chartManager.createEngagementLineChart(config.engagementCanvasId, {
            plugins: {
                title: {
                    display: true,
                    text: 'Classroom Average Engagement'
                }
            }
        });
    }
    
    if (config.overviewCanvasId) {
        charts.overview = chartManager.createClassroomOverviewChart(config.overviewCanvasId);
    }
    
    if (config.progressCanvasId) {
        charts.progress = chartManager.createProgressBarChart(config.progressCanvasId, {
            plugins: {
                title: {
                    display: true,
                    text: 'Student Progress'
                }
            }
        });
    }
    
    if (config.timelineCanvasId) {
        charts.timeline = chartManager.createAdaptationTimelineChart(config.timelineCanvasId, {
            plugins: {
                title: {
                    display: true,
                    text: 'Adaptation Timeline'
                }
            }
        });
    }
    
    return { chartManager, charts };
}

// Global instances
const globalChartManager = new PACTChartManager();
const globalRealTimeUpdater = new RealTimeChartUpdater(globalChartManager);
const globalThemeManager = new ChartThemeManager();
const globalPerformanceMonitor = new ChartPerformanceMonitor();

// Export for different environments
if (typeof window !== 'undefined') {
    // Browser environment
    window.PACTChartManager = PACTChartManager;
    window.EngagementChart = EngagementChart;
    window.ClassroomOverviewChart = ClassroomOverviewChart;
    window.ProgressChart = ProgressChart;
    window.AdaptationTimelineChart = AdaptationTimelineChart;
    window.RealTimeChartUpdater = RealTimeChartUpdater;
    window.ChartThemeManager = ChartThemeManager;
    window.ChartPerformanceMonitor = ChartPerformanceMonitor;
    
    // Factory functions
    window.createStudentEngagementChart = createStudentEngagementChart;
    window.createTeacherClassroomCharts = createTeacherClassroomCharts;
    
    // Global instances
    window.globalChartManager = globalChartManager;
    window.globalRealTimeUpdater = globalRealTimeUpdater;
    window.globalThemeManager = globalThemeManager;
    window.globalPerformanceMonitor = globalPerformanceMonitor;
}

if (typeof module !== 'undefined' && module.exports) {
    // Node.js environment
    module.exports = {
        PACTChartManager,
        EngagementChart,
        ClassroomOverviewChart,
        ProgressChart,
        AdaptationTimelineChart,
        RealTimeChartUpdater,
        ChartThemeManager,
        ChartPerformanceMonitor,
        createStudentEngagementChart,
        createTeacherClassroomCharts
    };
}
