// Spotify Unwrapped Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize visualizations when the page loads
    initializeCharts();
    
    // Add event listeners for form controls
    setupEventListeners();
    
    // Make sure the bottom player bar stays fixed while scrolling
    window.addEventListener('scroll', function() {
        const bottomPic = document.getElementById('bottom-pic');
        bottomPic.style.bottom = '60px'; // Keep it above the footer
    });
});

// Initialize all charts
function initializeCharts() {
    createChoroplethMap();
    createLineGraph();
    createGenreDistribution();
    createDanceEnergyChart();
    createScatterPlot();
}

// Setup event listeners for interactive controls
function setupEventListeners() {
    // Song/Artist dropdown
    const songArtistDropdown = document.querySelector('#song-artist-dropdown');
    if (songArtistDropdown) {
        songArtistDropdown.addEventListener('change', function() {
            updateAllCharts();
        });
    }
    
    // Date range pickers
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateAllCharts();
        });
    });
    
    // Radio buttons for type selection
    const radioButtons = document.querySelectorAll('input[type="radio"][name="type"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            updateAllCharts();
        });
    });
    
    // Audio feature dropdown
    const featureDropdown = document.querySelector('#audio-feature-dropdown');
    if (featureDropdown) {
        featureDropdown.addEventListener('change', function() {
            updateDanceEnergyChart();
        });
    }
    
    // Scatter plot axis dropdowns
    const xAxisDropdown = document.querySelector('#x-axis-dropdown');
    const yAxisDropdown = document.querySelector('#y-axis-dropdown');
    
    if (xAxisDropdown && yAxisDropdown) {
        xAxisDropdown.addEventListener('change', function() {
            updateScatterPlot();
        });
        
        yAxisDropdown.addEventListener('change', function() {
            updateScatterPlot();
        });
    }
}

// Update all charts based on current selections
function updateAllCharts() {
    // Get current selections
    const selection = document.querySelector('#song-artist-dropdown').value;
    const startDate = document.querySelector('input[type="date"]:first-of-type').value;
    const endDate = document.querySelector('input[type="date"]:last-of-type').value;
    const type = document.querySelector('input[type="radio"][name="type"]:checked').value;
    
    console.log(`Updating all charts with: ${selection}, ${startDate} to ${endDate}, type: ${type}`);
    
    // Update individual charts
    updateChoroplethMap(selection, startDate, endDate, type);
    updateLineGraph(selection, startDate, endDate, type);
    updateDanceEnergyChart();
    updateScatterPlot();
}

// Choropleth Map functions
function createChoroplethMap() {
    // This would typically use Plotly.js or another visualization library
    console.log('Creating choropleth map');
    
    // In a real implementation, this would be actual chart creation code
    // For this static HTML example, we'll just log the function call
    
    // Example Plotly.js code (commented out)
    /*
    const data = [{
        type: 'choropleth',
        locationmode: 'country names',
        locations: ['USA', 'Canada', 'Mexico', 'Brazil', 'UK', 'France', 'Germany', 'Japan', 'Australia', 'South Africa'],
        z: [65, 58, 72, 82, 59, 63, 61, 55, 57, 69],
        text: ['USA', 'Canada', 'Mexico', 'Brazil', 'UK', 'France', 'Germany', 'Japan', 'Australia', 'South Africa'],
        colorscale: 'Viridis',
        colorbar: {
            title: 'Popularity',
            thickness: 20
        },
    }];

    const layout = {
        title: 'Global Music Popularity by Region',
        geo: {
            showframe: false,
            showcoastlines: true,
            projection: {
                type: 'mercator'
            }
        },
        paper_bgcolor: '#282828',
        plot_bgcolor: '#282828',
        font: {
            color: 'white'
        },
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 50,
            pad: 4
        }
    };

    Plotly.newPlot('choropleth-map', data, layout);
    */
}

function updateChoroplethMap(selection, startDate, endDate, type) {
    console.log(`Updating choropleth map with: ${selection}, ${startDate} to ${endDate}, type: ${type}`);
    
    // In a real implementation, this would update the existing chart
    // For this static HTML example, we'll just log the function call
}

// Line Graph functions
function createLineGraph() {
    console.log('Creating line graph');
    
    // Example Plotly.js code (commented out)
    /*
    const dates = ['2000-01', '2002-01', '2004-01', '2006-01', '2008-01', 
                  '2010-01', '2012-01', '2014-01', '2016-01', '2018-01'];
    
    const trace1 = {
        x: dates,
        y: [0.65, 0.68, 0.72, 0.74, 0.76, 0.79, 0.82, 0.85, 0.87, 0.89],
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Danceability',
        line: {
            color: '#1DB954',
            width: 3
        },
        marker: {
            size: 8
        }
    };
    
    const trace2 = {
        x: dates,
        y: [0.72, 0.75, 0.73, 0.69, 0.71, 0.76, 0.79, 0.82, 0.85, 0.88],
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Energy',
        line: {
            color: '#F230AA',
            width: 3
        },
        marker: {
            size: 8
        }
    };
    
    const trace3 = {
        x: dates,
        y: [0.55, 0.54, 0.57, 0.62, 0.65, 0.61, 0.58, 0.52, 0.48, 0.44],
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Acousticness',
        line: {
            color: '#1E90FF',
            width: 3
        },
        marker: {
            size: 8
        }
    };
    
    const data = [trace1, trace2, trace3];
    
    const layout = {
        title: 'Trend of Audio Features (2000-2019)',
        xaxis: {
            title: 'Year',
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: 'Value',
            showgrid: true,
            gridcolor: '#444',
            zeroline: false
        },
        paper_bgcolor: '#282828',
        plot_bgcolor: '#282828',
        font: {
            color: 'white'
        },
        legend: {
            orientation: 'h',
            yanchor: 'bottom',
            y: 1.02,
            xanchor: 'right',
            x: 1
        },
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        }
    };
    
    Plotly.newPlot('line-graph', data, layout);
    */
}

function updateLineGraph(selection, startDate, endDate, type) {
    console.log(`Updating line graph with: ${selection}, ${startDate} to ${endDate}, type: ${type}`);
    
    // In a real implementation, this would update the existing chart
}

// Genre Distribution functions
function createGenreDistribution() {
    console.log('Creating genre distribution chart');
    
    // Example Plotly.js code (commented out)
    /*
    const data = [{
        x: ['Pop', 'Latin', 'Rock', 'Hip-Hop', 'EDM', 'R&B', 'Country', 'K-Pop', 'Alternative', 'Indie'],
        y: [458, 356, 325, 289, 215, 178, 134, 245, 167, 142],
        type: 'bar',
        marker: {
            color: [
                '#1DB954', '#1DB954', '#1DB954', '#1DB954', '#1DB954',
                '#1DB954', '#1DB954', '#1DB954', '#1DB954', '#1DB954'
            ],
            opacity: [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.65, 0.55, 0.45],
            line: {
                color: '#1ed760',
                width: 1.5
            }
        }
    }];
    
    const layout = {
        title: 'Top 10 Genre by Song Counts',
        xaxis: {
            title: 'Genre',
            tickangle: -45
        },
        yaxis: {
            title: 'Song Count',
            gridcolor: '#444'
        },
        paper_bgcolor: '#282828',
        plot_bgcolor: '#282828',
        font: {
            color: 'white'
        },
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 50,
            pad: 4
        }
    };
    
    Plotly.newPlot('genre-distribution', data, layout);
    */
}

// Dance and Energy Chart functions
function createDanceEnergyChart() {
    console.log('Creating dance and energy chart');
    
    // This would create a bar chart showing danceability and energy