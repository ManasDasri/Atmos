// Enhanced app.js - IMPROVED MAIN DASHBOARD

// API base URL
const API_BASE = '';

// Utility: Fetch JSON data
async function fetchJSON(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Utility: Get AQI category with advice
function getAQICategory(pm25) {
    if (pm25 <= 50) return { 
        class: 'aqi-good', 
        text: 'Good',
        color: '#10B981',
        advice: 'Air quality is satisfactory. Perfect for outdoor activities!'
    };
    if (pm25 <= 100) return { 
        class: 'aqi-moderate', 
        text: 'Moderate',
        color: '#F59E0B',
        advice: 'Acceptable for most. Sensitive individuals should limit prolonged outdoor exertion.'
    };
    if (pm25 <= 150) return { 
        class: 'aqi-unhealthy', 
        text: 'Unhealthy',
        color: '#F97316',
        advice: 'Reduce outdoor activities. Wear masks if necessary.'
    };
    if (pm25 <= 200) return { 
        class: 'aqi-very-unhealthy', 
        text: 'Very Unhealthy',
        color: '#EF4444',
        advice: 'Avoid prolonged outdoor activities. Wear N95 masks.'
    };
    return { 
        class: 'aqi-hazardous', 
        text: 'Hazardous',
        color: '#9333EA',
        advice: 'Stay indoors. Use air purifiers. Health alert!'
    };
}

// Utility: Format currency
function formatCurrency(amount) {
    if (amount >= 10000000) {
        return `₹${(amount / 10000000).toFixed(1)}Cr`;
    } else if (amount >= 100000) {
        return `₹${(amount / 100000).toFixed(1)}L`;
    } else {
        return `₹${(amount / 1000).toFixed(0)}k`;
    }
}

// Load model data
async function loadModelData() {
    try {
        const data = await fetchJSON(`${API_BASE}/api/model`);
        return data;
    } catch (error) {
        console.error('Error loading model data:', error);
        showError('Failed to load model data. Please refresh the page.');
        return null;
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const stats = await fetchJSON(`${API_BASE}/api/stats`);
        return stats;
    } catch (error) {
        console.error('Error loading statistics:', error);
        return null;
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        z-index: 3000;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
        animation: slideInRight 0.3s ease-out;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Update stats display
function updateStatsDisplay(stats) {
    if (!stats) return;
    
    const elements = {
        totalSensors: document.getElementById('total-sensors'),
        referenceSensors: document.getElementById('reference-sensors'),
        monitoringSensors: document.getElementById('monitoring-sensors'),
        totalZones: document.getElementById('total-zones'),
        avgAQI: document.getElementById('avg-aqi'),
        worstZone: document.getElementById('worst-zone'),
        bestZone: document.getElementById('best-zone'),
        totalCost: document.getElementById('total-cost'),
        coverageArea: document.getElementById('coverage-area'),
        coveragePercentage: document.getElementById('coverage-percentage'),
        theoreticalCoverage: document.getElementById('theoretical-coverage'),
        overlapPercentage: document.getElementById('overlap-percentage'),
        effectiveCoverage: document.getElementById('effective-coverage')
    };
    
    if (elements.totalSensors) {
        animateValue(elements.totalSensors, 0, stats.total_sensors, 1500);
    }
    if (elements.referenceSensors) {
        elements.referenceSensors.textContent = stats.reference_sensors || 4;
    }
    if (elements.monitoringSensors) {
        elements.monitoringSensors.textContent = stats.monitoring_sensors || (stats.total_sensors - 4);
    }
    if (elements.totalZones) {
        elements.totalZones.textContent = stats.total_zones;
    }
    if (elements.avgAQI) {
        animateValue(elements.avgAQI, 0, stats.average_aqi, 1500, (val) => val.toFixed(1));
    }
    if (elements.worstZone) {
        elements.worstZone.textContent = `${stats.worst_zone.name} (${stats.worst_zone.aqi})`;
    }
    if (elements.bestZone) {
        elements.bestZone.textContent = `${stats.best_zone.name} (${stats.best_zone.aqi})`;
    }
    if (elements.totalCost) {
        elements.totalCost.textContent = formatCurrency(stats.total_cost);
    }
    if (elements.coverageArea) {
        const coverageValue = stats.coverage_area_km2 || 0;
        elements.coverageArea.textContent = `${coverageValue.toFixed(1)} km²`;
    }
    if (elements.coveragePercentage) {
        animateValue(elements.coveragePercentage, 0, stats.coverage_percentage || 0, 1500, (val) => val.toFixed(1));
    }
    if (elements.theoreticalCoverage) {
        const theoreticalValue = stats.theoretical_coverage_km2 || 0;
        elements.theoreticalCoverage.textContent = `${theoreticalValue.toFixed(1)} km²`;
    }
    if (elements.overlapPercentage) {
        const overlapValue = stats.overlap_percentage || 0;
        elements.overlapPercentage.textContent = `${overlapValue.toFixed(1)}%`;
    }
    if (elements.effectiveCoverage) {
        const effectiveValue = stats.coverage_area_km2 || 0;
        elements.effectiveCoverage.textContent = `${effectiveValue.toFixed(1)} km²`;
    }
}

// Animate number counter
function animateValue(element, start, end, duration, formatter = (val) => Math.round(val)) {
    if (!element) return;
    
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeProgress;
        
        element.textContent = formatter(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Render zones table
function renderZonesTable(zones, containerId = 'zones-table') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const sortedZones = [...zones].sort((a, b) => b.pm25 - a.pm25);
    
    let html = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Zone</th>
                        <th>PM2.5 (µg/m³)</th>
                        <th>Traffic</th>
                        <th>Sensors</th>
                        <th>Type & Range</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    sortedZones.forEach(zone => {
        const category = getAQICategory(zone.pm25);
        
        let sensorType;
        if (zone.has_reference_sensor) {
            sensorType = `<span style="color: #EC4899; font-weight: 700;">REF (4km)</span> + ${zone.monitoring_sensors} <span style="color: #4F46E5;">MON (3km)</span>`;
        } else {
            sensorType = `${zone.sensors || zone.total_sensors} <span style="color: #4F46E5;">MON (3km)</span>`;
        }
        
        html += `
            <tr>
                <td>
                    <strong>${zone.name}</strong>
                    ${zone.has_reference_sensor ? '<span style="color: #EC4899; font-size: 0.75rem; margin-left: 0.5rem;">● REF STATION</span>' : ''}
                </td>
                <td><strong style="color: var(--accent-primary);">${zone.pm25}</strong></td>
                <td><span class="traffic-${zone.traffic.toLowerCase()}">${zone.traffic}</span></td>
                <td><strong>${zone.total_sensors || zone.sensors}</strong></td>
                <td style="font-size: 0.813rem;">${sensorType}</td>
                <td><span class="aqi-badge ${category.class}">${category.text}</span></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// ENHANCED: Better map initialization with individual sensor markers and improved visuals
function initializeMap(modelData, mapId = 'map') {
    const mapContainer = document.getElementById(mapId);
    if (!mapContainer) {
        console.error('❌ Map container not found:', mapId);
        return;
    }
    
    if (typeof L === 'undefined') {
        mapContainer.innerHTML = '<p style="color: var(--text-secondary);">Map library not loaded</p>';
        return;
    }
    
    const map = L.map(mapId, {
        zoomControl: true,
        attributionControl: false
    }).setView([12.9716, 77.5946], 11);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors, © CARTO',
        maxZoom: 19
    }).addTo(map);

    // Fetch and draw the Bangalore Outline
    fetch('/static/bangalore.geojson')
        .then(res => res.json())
        .then(geojsonData => {
            L.geoJSON(geojsonData, {
                style: {
                    color: '#4F46E5',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: '#4F46E5',
                    fillOpacity: 0.05,
                    dashArray: '5, 10'
                }
            }).addTo(map);
            // Optionally, we could map.fitBounds() here if we want to zoom perfectly to the outline
        })
        .catch(err => console.error("Could not load Bangalore outline:", err));
        
    const sensors = modelData.all_sensors || [];
    const zones = modelData.zones || modelData;
    
    console.log(`🗺️ Map data:`, {
        sensors: sensors.length,
        zones: Array.isArray(zones) ? zones.length : 'N/A',
        hasSensors: sensors.length > 0
    });
    
    if (sensors.length > 0) {
        console.log(`✅ Rendering ${sensors.length} individual sensors on map`);
        
        // Create layer groups
        const referenceLayer = L.layerGroup().addTo(map);
        const monitoringLayer = L.layerGroup().addTo(map);
        
        sensors.forEach((sensor, index) => {
            const category = getAQICategory(sensor.pm25);
            const isReference = sensor.type === 'reference';
            const layer = isReference ? referenceLayer : monitoringLayer;
            
            const markerColor = isReference ? '#EC4899' : '#6366F1';
            const sensorRange = sensor.range_km || (isReference ? 4 : 3);
            
            // Coverage circle
            const circle = L.circle([sensor.lat, sensor.lon], {
                radius: sensorRange * 1000,
                fillColor: markerColor,
                color: markerColor,
                weight: 2,
                opacity: 0.4,
                fillOpacity: 0.1
            }).addTo(layer);
            
            circle.on('mouseover', function() {
                this.setStyle({ fillOpacity: 0.25, weight: 3, opacity: 0.7 });
            });
            
            circle.on('mouseout', function() {
                this.setStyle({ fillOpacity: 0.1, weight: 2, opacity: 0.4 });
            });
            
            circle.bindPopup(`
                <div style="font-family: monospace; min-width: 220px;">
                    <strong style="color: ${markerColor}; font-size: 1.1em;">${sensor.id}</strong><br>
                    ${isReference ? '<span style="background: rgba(236, 72, 153, 0.2); color: #EC4899; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7em; font-weight: 700;">REFERENCE</span><br>' : ''}
                    <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #ddd;">
                    <strong>Zone:</strong> ${sensor.zone}<br>
                    <strong>Location:</strong> ${sensor.location}<br>
                    <strong>Type:</strong> ${isReference ? 'Reference (4km)' : 'Monitoring (3km)'}<br>
                    <strong>PM2.5:</strong> <span style="color: ${category.color}; font-weight: 700;">${sensor.pm25} µg/m³</span><br>
                    <strong>Status:</strong> <span style="color: ${category.color};">${category.text}</span><br>
                    <strong>Traffic:</strong> ${sensor.traffic}
                </div>
            `);
            
            // Enhanced marker
            const markerSize = isReference ? 12 : 9;
            const pulseSize = isReference ? 22 : 18;
            
            const marker = L.marker([sensor.lat, sensor.lon], {
                icon: L.divIcon({
                    className: 'custom-sensor-marker-enhanced',
                    html: `
                        <div style="position: relative; width: ${pulseSize}px; height: ${pulseSize}px;">
                            <div style="
                                position: absolute;
                                top: 50%;
                                left: 50%;
                                transform: translate(-50%, -50%);
                                width: ${pulseSize}px;
                                height: ${pulseSize}px;
                                background: ${markerColor}40;
                                border-radius: 50%;
                                animation: marker-pulse 2s ease-out infinite;
                            "></div>
                            <div style="
                                position: absolute;
                                top: 50%;
                                left: 50%;
                                transform: translate(-50%, -50%);
                                width: ${markerSize}px;
                                height: ${markerSize}px;
                                background: ${markerColor};
                                border: 3px solid white;
                                border-radius: 50%;
                                box-shadow: 0 4px 12px ${markerColor}80;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 900;
                                font-size: ${isReference ? '8px' : '7px'};
                                color: white;
                                cursor: pointer;
                            " class="marker-core-enhanced">${index + 1}</div>
                        </div>
                        <style>
                            @keyframes marker-pulse {
                                0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.8; }
                                100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
                            }
                            .marker-core-enhanced:hover {
                                transform: translate(-50%, -50%) scale(1.2) !important;
                            }
                        </style>
                    `,
                    iconSize: [pulseSize, pulseSize],
                    iconAnchor: [pulseSize/2, pulseSize/2]
                }),
                zIndexOffset: isReference ? 2000 : 1000
            }).addTo(layer);
            
            marker.bindPopup(circle.getPopup());
            
            marker.on('mouseover', function() {
                circle.fire('mouseover');
            });
            
            marker.on('mouseout', function() {
                circle.fire('mouseout');
            });
        });
        
        // Add layer control
        const overlays = {
            "🔬 Reference Sensors": referenceLayer,
            "📊 Monitoring Sensors": monitoringLayer
        };
        L.control.layers(null, overlays, { collapsed: false }).addTo(map);
        
        console.log(`✅ Successfully rendered ${sensors.length} sensors with layer control`);
    } else {
        console.log('⚠️ all_sensors not found, using zone-level markers');
        
        const zoneArray = Array.isArray(zones) ? zones : [];
        
        if (zoneArray.length === 0) {
            console.error('❌ No zones available for rendering');
            mapContainer.innerHTML = '<p style="color: var(--danger); padding: 2rem; text-align: center;">No zone data available</p>';
            return;
        }
        
        zoneArray.forEach(zone => {
            const category = getAQICategory(zone.pm25);
            const hasReference = zone.has_reference_sensor || false;
            
            const markerColor = hasReference ? '#EC4899' : category.color;
            const markerSize = 8 + ((zone.total_sensors || zone.sensors || 0) * 1.5);
            
            const marker = L.circleMarker(zone.center, {
                radius: markerSize,
                fillColor: markerColor,
                color: '#fff',
                weight: hasReference ? 3 : 2,
                opacity: 1,
                fillOpacity: hasReference ? 0.9 : 0.8
            }).addTo(map);
            
            const sensorInfo = hasReference ? 
                `1 Reference (4km) + ${zone.monitoring_sensors || 0} Monitoring (3km)` : 
                `${zone.total_sensors || zone.sensors || 0} Monitoring (3km)`;
            
            marker.bindPopup(`
                <div style="font-family: 'JetBrains Mono', monospace; min-width: 200px;">
                    <strong style="font-size: 1.1em; color: ${markerColor};">${zone.name}</strong>
                    ${hasReference ? '<br><span style="background: rgba(236, 72, 153, 0.2); color: #EC4899; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">REFERENCE STATION</span>' : ''}
                    <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid rgba(167, 139, 250, 0.2);">
                    <strong>PM2.5:</strong> ${zone.pm25} µg/m³<br>
                    <strong>Traffic:</strong> ${zone.traffic}<br>
                    <strong>Sensors:</strong> ${sensorInfo}<br>
                    <span class="aqi-badge ${category.class}" style="margin-top: 0.5rem; display: inline-block; font-size: 0.75rem;">${category.text}</span>
                </div>
            `);
        });
    }
    
    setTimeout(() => {
        map.invalidateSize();
    }, 100);
    
    return map;
}

// Initialize chart with better styling
function initializeChart(zones, chartId = 'aqi-chart') {
    const ctx = document.getElementById(chartId);
    if (!ctx) return;
    
    if (typeof Chart === 'undefined') {
        ctx.parentElement.innerHTML = '<p style="color: var(--text-secondary);">Chart library not loaded</p>';
        return;
    }
    
    const sortedZones = [...zones].sort((a, b) => b.pm25 - a.pm25).slice(0, 10);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedZones.map(z => z.name),
            datasets: [{
                label: 'PM2.5 (µg/m³)',
                data: sortedZones.map(z => z.pm25),
                backgroundColor: sortedZones.map(z => {
                    if (z.pm25 <= 50) return 'rgba(16, 185, 129, 0.8)';
                    if (z.pm25 <= 100) return 'rgba(245, 158, 11, 0.8)';
                    if (z.pm25 <= 150) return 'rgba(249, 115, 22, 0.8)';
                    if (z.pm25 <= 200) return 'rgba(239, 68, 68, 0.8)';
                    return 'rgba(147, 51, 234, 0.8)';
                }),
                borderColor: sortedZones.map(z => {
                    if (z.pm25 <= 50) return '#10B981';
                    if (z.pm25 <= 100) return '#F59E0B';
                    if (z.pm25 <= 150) return '#F97316';
                    if (z.pm25 <= 200) return '#EF4444';
                    return '#9333EA';
                }),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(26, 27, 46, 0.95)',
                    titleColor: '#A78BFA',
                    bodyColor: '#FFFFFF',
                    borderColor: '#A78BFA',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: {
                        family: 'JetBrains Mono',
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        family: 'JetBrains Mono',
                        size: 12
                    },
                    callbacks: {
                        label: (context) => {
                            const zone = sortedZones[context.dataIndex];
                            const lines = [`PM2.5: ${context.parsed.y} µg/m³`];
                            if (zone.has_reference_sensor) {
                                lines.push('Reference Station');
                            }
                            lines.push(`Sensors: ${zone.total_sensors || zone.sensors}`);
                            return lines;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(167, 139, 250, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94A3B8',
                        font: {
                            family: 'JetBrains Mono',
                            size: 11
                        }
                    },
                    title: {
                        display: true,
                        text: 'PM2.5 (µg/m³)',
                        color: '#A78BFA',
                        font: {
                            family: 'JetBrains Mono',
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94A3B8',
                        maxRotation: 45,
                        minRotation: 45,
                        font: {
                            family: 'JetBrains Mono',
                            size: 10
                        }
                    }
                }
            }
        }
    });
}

// Search zone
async function searchZone(zoneName) {
    try {
        const zone = await fetchJSON(`${API_BASE}/api/zone/${encodeURIComponent(zoneName)}`);
        return zone;
    } catch (error) {
        console.error('Zone search error:', error);
        return null;
    }
}

// Display search result
function displaySearchResult(zone) {
    const container = document.getElementById('search-result');
    if (!container) return;
    
    if (!zone) {
        container.innerHTML = `
            <div class="card">
                <p style="color: var(--danger);">❌ Zone not found. Please try another name.</p>
            </div>
        `;
        return;
    }
    
    const category = getAQICategory(zone.pm25);
    const hasReference = zone.has_reference_sensor;
    
    const sensorType = hasReference ? 
        `${zone.monitoring_sensors} Monitoring (3km) + 1 Reference (4km)` : 
        `${zone.total_sensors || zone.sensors} Monitoring (3km range)`;
    
    container.innerHTML = `
        <div class="card fade-in">
            <h2 style="margin-bottom: 1.5rem; color: var(--accent-primary);">
                ${zone.name}
                ${hasReference ? '<span style="background: rgba(236, 72, 153, 0.2); color: #EC4899; padding: 0.25rem 0.75rem; border-radius: 8px; font-size: 0.813rem; font-weight: 700; margin-left: 1rem;">REFERENCE STATION</span>' : ''}
            </h2>
            <div class="stats-grid">
                <div class="stat-card ${category.class.replace('aqi-', '')}">
                    <div class="stat-label">PM2.5 Level</div>
                    <div class="stat-value">${zone.pm25}</div>
                    <div class="stat-subtitle">µg/m³</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Air Quality</div>
                    <div class="stat-value" style="font-size: 1.5rem;">${category.text}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Traffic Level</div>
                    <div class="stat-value" style="font-size: 1.5rem;">${zone.traffic}</div>
                    <div class="stat-subtitle">${zone.congestion?.toFixed(0) || 'N/A'}% congestion</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Sensors Deployed</div>
                    <div class="stat-value">${zone.total_sensors || zone.sensors}</div>
                    <div class="stat-subtitle">${sensorType}</div>
                </div>
            </div>
        </div>
    `;
}

// Trigger optimization
async function triggerOptimization() {
    const btn = document.getElementById('optimize-btn');
    if (!btn) return;
    
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> Optimizing...';
    
    try {
        await fetch(`${API_BASE}/api/optimize`, { method: 'POST' });
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        showError('Optimization failed. Please try again.');
        btn.disabled = false;
        btn.innerHTML = '🔄 Re-Optimize';
    }
}

// Check API status
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/waqi/live`);
        const data = await response.json();
        
        const notificationBar = document.getElementById('notification-bar');
        const notificationText = document.getElementById('notification-text');
        const notificationTimestamp = document.getElementById('notification-timestamp');
        
        if (!notificationBar) return;
        
        if (data.source === 'waqi_api') {
            notificationBar.className = 'notification-bar live';
            notificationText.textContent = '🌐 Live WAQI API Data';
            notificationTimestamp.textContent = `Updated: ${data.timestamp || 'now'}`;
        } else if (data.source === 'fallback') {
            notificationBar.className = 'notification-bar fallback';
            notificationText.textContent = '⚠️ Using Simulated Data';
            notificationTimestamp.textContent = 'WAQI API unavailable';
        }
        
        notificationBar.style.display = 'flex';
        document.body.classList.add('has-notification');
    } catch (error) {
        console.error('API status check failed:', error);
    }
}

// Initialize on page load
checkAPIStatus();
setInterval(checkAPIStatus, 5 * 60 * 1000);

// Global initialization
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Enhanced App.js loaded - Better Sensor Network Visualization v3.0');
});

// Export for global use
window.getAQICategory = getAQICategory;