// Enhanced deployment.js - IMPROVED VISUALIZATION

let deploymentMapInstance = null;
let sensorMarkers = [];
let coverageCircles = [];

function initializeDeploymentMap(model) {
    console.log('🗺️ Enhanced initializeDeploymentMap called with', model.all_sensors?.length, 'sensors');
    
    const mapContainer = document.getElementById('deployment-map');
    if (!mapContainer) {
        console.error('❌ Map container not found');
        return null;
    }
    
    if (typeof L === 'undefined') {
        console.error('❌ Leaflet not loaded');
        mapContainer.innerHTML = '<p style="color: var(--text-secondary); padding: 2rem; text-align: center;">Map library not loaded</p>';
        return null;
    }
    
    // Remove existing map instance
    if (deploymentMapInstance) {
        console.log('🔄 Removing existing map...');
        try {
            deploymentMapInstance.remove();
        } catch (e) {
            console.warn('Map removal warning:', e);
        }
        deploymentMapInstance = null;
    }
    
    // Clear container
    mapContainer.innerHTML = '';
    mapContainer._leaflet_id = null;
    
    // Ensure container has dimensions
    mapContainer.style.height = '700px';
    mapContainer.style.width = '100%';
    mapContainer.style.position = 'relative';
    
    console.log('📏 Map container dimensions:', {
        width: mapContainer.offsetWidth,
        height: mapContainer.offsetHeight
    });
    
    if (mapContainer.offsetWidth === 0 || mapContainer.offsetHeight === 0) {
        console.error('❌ Map container has no dimensions!');
        return null;
    }
    
    try {
        // Create map with better settings
        console.log('🗺️ Creating enhanced Leaflet map...');
        const map = L.map('deployment-map', {
            center: [12.9716, 77.5946],
            zoom: 11,
            zoomControl: true,
            preferCanvas: false,
            renderer: L.svg()
        });
        
        deploymentMapInstance = map;
        window.debugMap = map;
        
        // Add better tile layer
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© OpenStreetMap contributors, © CARTO',
            maxZoom: 19,
            minZoom: 10
        }).addTo(map);
        
        console.log('✅ Map created successfully');
        
        // Get sensors
        const sensors = model.all_sensors || [];
        console.log(`📡 Processing ${sensors.length} sensors...`);
        
        if (sensors.length === 0) {
            console.warn('⚠️ No sensors to display');
            return map;
        }
        
        // Add legend control
        addEnhancedLegend(map, model);
        
        // Add statistics panel
        addStatisticsPanel(map, model);
        
        // Group sensors by type
        const referenceSensors = sensors.filter(s => s.type === 'reference');
        const monitoringSensors = sensors.filter(s => s.type === 'monitoring');
        
        console.log(`📊 Sensors: ${referenceSensors.length} Reference, ${monitoringSensors.length} Monitoring`);
        
        // Create layer groups for better control
        const referenceLayer = L.layerGroup().addTo(map);
        const monitoringLayer = L.layerGroup().addTo(map);
        
        let markersAdded = 0;
        let circlesAdded = 0;
        
        // Add reference sensors first (more prominent)
        referenceSensors.forEach((sensor, index) => {
            addEnhancedSensor(sensor, index, referenceLayer, map);
            markersAdded++;
            circlesAdded++;
        });
        
        // Add monitoring sensors
        monitoringSensors.forEach((sensor, index) => {
            addEnhancedSensor(sensor, referenceSensors.length + index, monitoringLayer, map);
            markersAdded++;
            circlesAdded++;
        });
        
        console.log(`✅ Added ${circlesAdded} coverage circles and ${markersAdded} markers`);
        
        // Add layer control
        const overlays = {
            "🔬 Reference Sensors (4km)": referenceLayer,
            "📊 Monitoring Sensors (3km)": monitoringLayer
        };
        L.control.layers(null, overlays, { collapsed: false, position: 'topright' }).addTo(map);
        
        // Add cluster visualization option
        addClusterView(map, sensors);
        
        // Force map update
        setTimeout(() => {
            map.invalidateSize(true);
            console.log('🔧 Map size invalidated');
            
            // Fix SVG positioning
            const svg = document.querySelector('.leaflet-overlay-pane svg');
            if (svg) {
                svg.style.transform = 'translate3d(0px, 0px, 0px)';
                svg.style.position = 'relative';
            }
        }, 100);
        
        return map;
        
    } catch (error) {
        console.error('❌ Error creating map:', error);
        mapContainer.innerHTML = `<p style="color: var(--danger); padding: 2rem; text-align: center;">Error creating map: ${error.message}</p>`;
        return null;
    }
}

function addEnhancedSensor(sensor, globalIndex, layer, map) {
    const isReference = sensor.type === 'reference';
    const sensorRange = sensor.range_km || (isReference ? 4 : 3);
    
    // Enhanced colors
    const colors = {
        reference: {
            marker: '#EC4899',
            circle: '#F472B6',
            glow: 'rgba(236, 72, 153, 0.6)'
        },
        monitoring: {
            marker: '#6366F1',
            circle: '#818CF8',
            glow: 'rgba(99, 102, 241, 0.6)'
        }
    };
    
    const color = isReference ? colors.reference : colors.monitoring;
    
    // Add coverage circle with animation
    const circle = L.circle([sensor.lat, sensor.lon], {
        radius: sensorRange * 1000,
        color: color.circle,
        fillColor: color.circle,
        fillOpacity: 0.12,
        weight: 2,
        opacity: 0.5,
        className: 'sensor-coverage-circle'
    }).addTo(layer);
    
    coverageCircles.push(circle);
    
    // Enhanced hover effects
    circle.on('mouseover', function() {
        this.setStyle({ 
            fillOpacity: 0.25, 
            weight: 3,
            opacity: 0.8
        });
    });
    
    circle.on('mouseout', function() {
        this.setStyle({ 
            fillOpacity: 0.12, 
            weight: 2,
            opacity: 0.5
        });
    });
    
    // Enhanced popup with more details
    const aqiCategory = getAQICategory(sensor.pm25);
    circle.bindPopup(`
        <div style="font-family: 'JetBrains Mono', monospace; min-width: 260px; max-width: 300px;">
            <div style="background: linear-gradient(135deg, ${color.marker} 0%, ${color.circle} 100%); color: white; padding: 0.75rem; margin: -0.75rem -0.75rem 0.75rem -0.75rem; border-radius: 8px 8px 0 0;">
                <strong style="font-size: 1.15em; display: block; margin-bottom: 0.25rem;">${sensor.id}</strong>
                ${isReference ? '<span style="background: rgba(255,255,255,0.3); padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.7em; font-weight: 700;">REFERENCE STATION</span>' : '<span style="background: rgba(255,255,255,0.2); padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.7em;">MONITORING</span>'}
            </div>
            <div style="padding: 0.5rem 0;">
                <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.5rem; font-size: 0.85em;">
                    <span style="color: #94A3B8;">🏙️ Zone:</span>
                    <strong style="color: #E2E8F0;">${sensor.zone}</strong>
                    
                    <span style="color: #94A3B8;">📍 Location:</span>
                    <strong style="color: #E2E8F0;">${sensor.location}</strong>
                    
                    <span style="color: #94A3B8;">🗺️ Landmark:</span>
                    <span style="color: #CBD5E1;">${sensor.landmark}</span>
                    
                    <span style="color: #94A3B8;">📡 Range:</span>
                    <strong style="color: ${color.marker};">${sensorRange} km radius</strong>
                    
                    <span style="color: #94A3B8;">💰 Cost:</span>
                    <span style="color: #CBD5E1;">₹${(sensor.cost/100000).toFixed(1)}L</span>
                    
                    <span style="color: #94A3B8;">📍 GPS:</span>
                    <span style="color: #64748B; font-size: 0.75em;">${sensor.lat.toFixed(4)}°N, ${sensor.lon.toFixed(4)}°E</span>
                    
                    <span style="color: #94A3B8;">🌫️ PM2.5:</span>
                    <strong style="color: ${aqiCategory.color}; font-size: 1.1em;">${sensor.pm25} µg/m³</strong>
                    
                    <span style="color: #94A3B8;">🚦 Traffic:</span>
                    <span style="color: #CBD5E1;">${sensor.traffic}</span>
                </div>
                <div style="margin-top: 0.75rem; padding: 0.5rem; background: ${aqiCategory.color}15; border-left: 3px solid ${aqiCategory.color}; border-radius: 4px;">
                    <strong style="color: ${aqiCategory.color}; font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.5px;">${aqiCategory.text}</strong>
                    <p style="margin: 0.25rem 0 0 0; font-size: 0.7em; color: #94A3B8; line-height: 1.4;">${aqiCategory.advice}</p>
                </div>
            </div>
        </div>
    `, {
        maxWidth: 320,
        className: 'enhanced-sensor-popup'
    });
    
    // Enhanced marker with pulsing animation
    const markerSize = isReference ? 14 : 10;
    const pulseSize = isReference ? 24 : 18;
    
    const marker = L.marker([sensor.lat, sensor.lon], {
        icon: L.divIcon({
            className: 'enhanced-sensor-marker',
            html: `
                <div style="position: relative; width: ${pulseSize}px; height: ${pulseSize}px;">
                    <!-- Pulse animation -->
                    <div style="
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        width: ${pulseSize}px;
                        height: ${pulseSize}px;
                        background: ${color.glow};
                        border-radius: 50%;
                        animation: sensor-pulse 2s ease-out infinite;
                        opacity: 0;
                    "></div>
                    <!-- Main marker -->
                    <div style="
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        width: ${markerSize}px;
                        height: ${markerSize}px;
                        background: ${color.marker};
                        border: 3px solid white;
                        border-radius: 50%;
                        box-shadow: 0 4px 12px ${color.glow}, 0 0 20px ${color.glow};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 900;
                        font-size: ${isReference ? '9px' : '7px'};
                        color: white;
                        transition: all 0.3s ease;
                        cursor: pointer;
                    " class="marker-core">${globalIndex + 1}</div>
                </div>
                <style>
                    @keyframes sensor-pulse {
                        0% {
                            transform: translate(-50%, -50%) scale(0.5);
                            opacity: 1;
                        }
                        100% {
                            transform: translate(-50%, -50%) scale(1.5);
                            opacity: 0;
                        }
                    }
                    .marker-core:hover {
                        transform: translate(-50%, -50%) scale(1.3) !important;
                        box-shadow: 0 6px 20px ${color.glow}, 0 0 30px ${color.glow} !important;
                    }
                </style>
            `,
            iconSize: [pulseSize, pulseSize],
            iconAnchor: [pulseSize/2, pulseSize/2]
        }),
        zIndexOffset: isReference ? 2000 : 1000,
        riseOnHover: true
    }).addTo(layer);
    
    sensorMarkers.push(marker);
    
    // Share same popup
    marker.bindPopup(circle.getPopup());
    
    // Sync interactions
    marker.on('click', () => {
        circle.openPopup();
    });
}

function getAQICategory(pm25) {
    if (pm25 <= 50) return { 
        color: '#10B981', 
        text: 'Good', 
        advice: 'Air quality is satisfactory. Perfect for outdoor activities!' 
    };
    if (pm25 <= 100) return { 
        color: '#F59E0B', 
        text: 'Moderate', 
        advice: 'Acceptable for most. Sensitive individuals should limit prolonged outdoor exertion.' 
    };
    if (pm25 <= 150) return { 
        color: '#F97316', 
        text: 'Unhealthy', 
        advice: 'Reduce outdoor activities. Wear masks if necessary.' 
    };
    if (pm25 <= 200) return { 
        color: '#EF4444', 
        text: 'Very Unhealthy', 
        advice: 'Avoid prolonged outdoor activities. Wear N95 masks.' 
    };
    return { 
        color: '#9333EA', 
        text: 'Hazardous', 
        advice: 'Stay indoors. Use air purifiers. Health alert!' 
    };
}

function addEnhancedLegend(map, model) {
    const legend = L.control({ position: 'bottomleft' });
    
    legend.onAdd = function() {
        const div = L.DomUtil.create('div', 'map-legend');
        div.innerHTML = `
            <div style="background: rgba(26, 27, 46, 0.95); padding: 1rem; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.6); border: 1px solid rgba(167, 139, 250, 0.3); min-width: 200px;">
                <h4 style="margin: 0 0 0.75rem 0; color: #A78BFA; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Sensor Legend</h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.813rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="width: 16px; height: 16px; background: #EC4899; border: 2px solid white; border-radius: 50%; box-shadow: 0 0 12px rgba(236, 72, 153, 0.6);"></div>
                        <span style="color: #E2E8F0;">Reference (4km) - ${model.reference_sensors || 4}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="width: 14px; height: 14px; background: #6366F1; border: 2px solid white; border-radius: 50%; box-shadow: 0 0 12px rgba(99, 102, 241, 0.6);"></div>
                        <span style="color: #E2E8F0;">Monitoring (3km) - ${model.monitoring_sensors || 63}</span>
                    </div>
                    <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(167, 139, 250, 0.2);">
                        <div style="color: #94A3B8; font-size: 0.75rem;">Total Coverage</div>
                        <div style="color: #A78BFA; font-weight: 700; font-size: 1rem;">${(model.effective_coverage_km2 || 0).toFixed(1)} km²</div>
                        <div style="color: #64748B; font-size: 0.7rem;">${(model.coverage_percentage || 0).toFixed(1)}% of city</div>
                    </div>
                </div>
            </div>
        `;
        return div;
    };
    
    legend.addTo(map);
}

function addStatisticsPanel(map, model) {
    const stats = L.control({ position: 'topright' });
    
    stats.onAdd = function() {
        const div = L.DomUtil.create('div', 'map-stats');
        div.innerHTML = `
            <div style="background: rgba(26, 27, 46, 0.95); padding: 1rem; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.6); border: 1px solid rgba(167, 139, 250, 0.3); min-width: 180px;">
                <h4 style="margin: 0 0 0.75rem 0; color: #A78BFA; font-size: 0.813rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">📊 Quick Stats</h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; color: #E2E8F0;">
                        <span style="color: #94A3B8;">Total Sensors:</span>
                        <strong style="color: #A78BFA;">${model.total_sensors || 67}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #E2E8F0;">
                        <span style="color: #94A3B8;">Zones Covered:</span>
                        <strong style="color: #A78BFA;">${model.zones?.length || 0}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #E2E8F0;">
                        <span style="color: #94A3B8;">Total Cost:</span>
                        <strong style="color: #10B981;">₹${((model.total_cost || 2490000)/100000).toFixed(1)}L</strong>
                    </div>
                    <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(167, 139, 250, 0.2);">
                        <div style="color: #94A3B8; font-size: 0.7rem;">Overlap Analysis</div>
                        <div style="color: #F59E0B; font-weight: 600;">${(model.overlap_percentage || 0).toFixed(1)}% overlap</div>
                        <div style="color: #64748B; font-size: 0.65rem; margin-top: 0.25rem;">Scientifically calculated</div>
                    </div>
                </div>
            </div>
        `;
        return div;
    };
    
    stats.addTo(map);
}

function addClusterView(map, sensors) {
    // Add button to toggle cluster view
    const clusterControl = L.control({ position: 'topleft' });
    
    clusterControl.onAdd = function() {
        const div = L.DomUtil.create('div', 'cluster-control');
        div.innerHTML = `
            <button id="toggle-clusters" style="
                background: rgba(26, 27, 46, 0.95);
                color: #A78BFA;
                border: 1px solid rgba(167, 139, 250, 0.3);
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.813rem;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                transition: all 0.3s ease;
            " onmouseover="this.style.background='rgba(167, 139, 250, 0.2)'" onmouseout="this.style.background='rgba(26, 27, 46, 0.95)'">
                🎯 Toggle Coverage View
            </button>
        `;
        
        L.DomEvent.disableClickPropagation(div);
        
        return div;
    };
    
    clusterControl.addTo(map);
    
    // Toggle coverage circles visibility
    setTimeout(() => {
        const btn = document.getElementById('toggle-clusters');
        let showCoverage = true;
        
        if (btn) {
            btn.addEventListener('click', () => {
                showCoverage = !showCoverage;
                coverageCircles.forEach(circle => {
                    if (showCoverage) {
                        circle.setStyle({ opacity: 0.5, fillOpacity: 0.12 });
                    } else {
                        circle.setStyle({ opacity: 0, fillOpacity: 0 });
                    }
                });
                btn.textContent = showCoverage ? '🎯 Hide Coverage' : '🎯 Show Coverage';
            });
        }
    }, 500);
}

function renderDeploymentDetails(zones) {
    const container = document.getElementById('deployment-details');
    if (!container) {
        console.error('Deployment details container not found');
        return;
    }
    
    if (!zones || zones.length === 0) {
        container.innerHTML = '<p style="color: var(--danger);">No zones data available</p>';
        return;
    }
    
    const sortedZones = [...zones].sort((a, b) => (b.total_sensors || b.sensors || 0) - (a.total_sensors || a.sensors || 0));
    
    let html = '';
    
    sortedZones.forEach(zone => {
        const zoneName = zone.name || 'Unknown Zone';
        const zonePm25 = zone.pm25 || 0;
        const zoneTraffic = zone.traffic || 'Unknown';
        const zoneSensors = zone.total_sensors || zone.sensors || 0;
        const hasReference = zone.has_reference_sensor || false;
        const monitoringSensors = zone.monitoring_sensors || zoneSensors;
        const zoneCongestion = zone.congestion || 0;
        const sensorPlacements = zone.sensor_placements || [];
        
        const aqiCategory = getAQICategory(zonePm25);
        const aqiClass = aqiCategory.text.toLowerCase().replace(/ /g, '-');
        const trafficClass = `traffic-${zoneTraffic.toLowerCase()}`;
        
        html += `
            <div class="zone-deployment">
                <div class="zone-header">
                    <h3>
                        ${zoneName}
                        ${hasReference ? '<span class="reference-badge">Reference Station</span>' : ''}
                        <span class="traffic-badge ${trafficClass}">${zoneTraffic}</span>
                        <span class="aqi-badge aqi-${aqiClass}">${aqiCategory.text}</span>
                    </h3>
                    <div class="zone-meta">
                        <span>📡 <strong>${zoneSensors}</strong> sensors</span>
                        ${hasReference ? 
                            `<span>🔬 <strong>1</strong> Reference + <strong>${monitoringSensors}</strong> Monitoring</span>` : 
                            `<span>📊 <strong>${zoneSensors}</strong> Monitoring</span>`
                        }
                        <span>🌫️ PM2.5: <strong>${zonePm25.toFixed(1)}</strong></span>
                        <span>🚦 Congestion: <strong>${zoneCongestion.toFixed(0)}%</strong></span>
                    </div>
                </div>
                <div class="sensor-list">
        `;
        
        sensorPlacements.forEach((sensor, index) => {
            const isReference = sensor.type === 'reference';
            const coords = [sensor.lat || 0, sensor.lon || 0];
            const sensorName = sensor.location || sensor.name || `Sensor ${index + 1}`;
            const sensorLandmark = sensor.landmark || 'N/A';
            const sensorRange = sensor.range_km || (isReference ? 4 : 3);
            
            html += `
                <div class="sensor-item">
                    <div class="sensor-number ${isReference ? 'reference' : ''}">${index + 1}</div>
                    <div class="sensor-details">
                        <h4>
                            ${sensorName} 
                            ${isReference ? '<span class="reference-badge">REF 4km</span>' : `<span style="font-size: 0.75rem; color: var(--text-secondary); background: rgba(79, 70, 229, 0.1); padding: 0.25rem 0.5rem; border-radius: 6px;">MON ${sensorRange}km</span>`}
                        </h4>
                        <div class="sensor-landmark">📍 ${sensorLandmark}</div>
                    </div>
                    <div class="sensor-coords">
                        ${coords[0].toFixed(4)}°N, ${coords[1].toFixed(4)}°E
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    console.log('✅ Deployment details rendered with enhanced styling');
}

// Export functions
if (typeof window !== 'undefined') {
    window.initializeDeploymentMap = initializeDeploymentMap;
    window.renderDeploymentDetails = renderDeploymentDetails;
    window.getAQICategory = getAQICategory;
    console.log('✅ Enhanced Deployment.js loaded with improved visualizations');
}