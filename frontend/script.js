// FinVerify AI Frontend JavaScript

// State
let currentVerification = null;
let chart = null;

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    loadExamples();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('claimInput').addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            verifyClaim();
        }
    });
}

async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();

        const container = document.getElementById('exampleButtons');
        container.innerHTML = '';

        data.examples.forEach(function (example) {
            const button = document.createElement('button');
            button.className = 'bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-full text-sm transition';
            button.textContent = example.length > 30 ? example.substring(0, 30) + '...' : example;
            button.onclick = function () { setExample(example); };
            container.appendChild(button);
        });
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

function setExample(text) {
    document.getElementById('claimInput').value = text;
    verifyClaim();
}

async function verifyClaim() {
    const claim = document.getElementById('claimInput').value.trim();
    if (!claim) {
        showError('Please enter a claim to verify');
        return;
    }

    // Show loading state
    const verifyBtn = document.getElementById('verifyBtn');
    const originalText = verifyBtn.innerHTML;
    verifyBtn.innerHTML = '<span class="loading-pulse">&#8987; Verifying...</span>';
    verifyBtn.disabled = true;

    // Show results container
    document.getElementById('results').classList.remove('hidden');

    // Reset displays
    document.getElementById('confidenceBar').style.width = '0%';
    document.getElementById('confidenceValue').textContent = '...';
    document.getElementById('confidenceReason').textContent = 'Analyzing claim...';
    document.getElementById('claimedDisplay').textContent = 'Analyzing...';
    document.getElementById('actualDisplay').textContent = 'Fetching data...';

    // Hide chart initially
    document.getElementById('chartContainer').classList.add('hidden');

    try {
        const response = await fetch('/api/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ claim: claim }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Verification failed');
        }

        if (data.error) {
            showError(data.error);
            return;
        }

        // Store current verification
        currentVerification = data;

        // Update UI with results
        updateResults(data);

        // Show debug info if in development
        if (window.location.hostname === 'localhost') {
            showDebugInfo(data);
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // Restore button
        verifyBtn.innerHTML = originalText;
        verifyBtn.disabled = false;
    }
}

function updateResults(data) {
    const confidence = data.confidence;

    // Update confidence bar
    document.getElementById('confidenceBar').style.width = confidence + '%';
    document.getElementById('confidenceValue').textContent = confidence + '%';
    document.getElementById('confidenceReason').textContent = data.reason || '';

    // Update confidence color
    const bar = document.getElementById('confidenceBar');
    bar.className = 'h-6 rounded-full transition-all duration-1000 ease-out';

    if (confidence >= 80) {
        bar.classList.add('bg-green-500');
        document.getElementById('confidenceBadge').className =
            'px-4 py-2 rounded-full text-sm font-semibold bg-green-100 text-green-800';
        document.getElementById('confidenceBadge').textContent = 'High Confidence';
    } else if (confidence >= 50) {
        bar.classList.add('bg-yellow-500');
        document.getElementById('confidenceBadge').className =
            'px-4 py-2 rounded-full text-sm font-semibold bg-yellow-100 text-yellow-800';
        document.getElementById('confidenceBadge').textContent = 'Medium Confidence';
    } else {
        bar.classList.add('bg-red-500');
        document.getElementById('confidenceBadge').className =
            'px-4 py-2 rounded-full text-sm font-semibold bg-red-100 text-red-800';
        document.getElementById('confidenceBadge').textContent = 'Low Confidence';
    }

    if (data.verification) {
        const v = data.verification;

        // Format values
        const claimedFormatted =
            v.additional_context?.claimed_formatted || v.metric + ': ' + v.claimed_value;
        const actualFormatted =
            v.additional_context?.actual_formatted || v.metric + ': ' + v.actual_value;

        // Update displays
        document.getElementById('claimedDisplay').textContent = claimedFormatted;
        document.getElementById('actualDisplay').textContent = actualFormatted;

        document.getElementById('claimedDetail').innerHTML =
            '<span class="font-medium">' + v.company + ' (' + v.ticker + ')</span><br>' +
            v.metric.replace('_', ' ').toUpperCase();

        document.getElementById('actualDetail').innerHTML =
            '<span class="font-medium">Verified via ' + v.source + '</span><br>' +
            (v.additional_context?.percent_difference || '');

        document.getElementById('sourceInfo').textContent = v.source;
        document.getElementById('timestamp').textContent = new Date(v.timestamp).toLocaleString();

        // Try to fetch and show historical data
        fetchHistoricalData(v.ticker);
    }
}

async function fetchHistoricalData(ticker) {
    try {
        const response = await fetch('/api/historical/' + ticker + '?days=30');
        if (response.ok) {
            const data = await response.json();
            if (data && data.length > 0) {
                displayPriceChart(data);
            }
        }
    } catch (error) {
        console.log('Historical data not available');
    }
}

function displayPriceChart(priceData) {
    var ctx = document.getElementById('priceChart').getContext('2d');

    // Destroy existing chart
    if (chart) {
        chart.destroy();
    }

    // Show chart container
    document.getElementById('chartContainer').classList.remove('hidden');

    // Create new chart
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: priceData.map(function (d) {
                return new Date(d.date).toLocaleDateString();
            }),
            datasets: [
                {
                    label: 'Stock Price',
                    data: priceData.map(function (d) {
                        return d.close;
                    }),
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.1,
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 2.5,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function (value) {
                            return '$' + value;
                        },
                    },
                },
            },
        },
    });
}

function showError(message) {
    var toast = document.createElement('div');
    toast.className =
        'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-xl shadow-lg z-50';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(function () {
        toast.remove();
    }, 3000);
}

function showDebugInfo(data) {
    document.getElementById('debugInfo').classList.remove('hidden');
    document.getElementById('debugJson').textContent = JSON.stringify(data, null, 2);
}

function clearInput() {
    document.getElementById('claimInput').value = '';
    document.getElementById('results').classList.add('hidden');
    document.getElementById('debugInfo').classList.add('hidden');
    document.getElementById('chartContainer').classList.add('hidden');
}
