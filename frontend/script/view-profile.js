/*************************************************
 * Handle charts on Profile                      *
 *************************************************/
const pathParts = window.location.pathname.split('/');
const username = pathParts[2];
const kcalCanvas = document.getElementById('viewKcalChart');
const timeCanvas = document.getElementById('viewBubbleChart');

fetch(`/main/charts?username=${username}`)
    .then(res => res.json())
    .then(data => {
        if (kcalCanvas) {
            const kcalChart = new Chart(kcalCanvas.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: data.p7d_labels,
                    datasets: [{
                    label: 'calories',
                    data: data.p7d_cal,
                    borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Calories"
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Calories Burned in the Last 7 Days (UTC Time)',
                            align: 'start',
                            padding: {
                                top: 10,
                                bottom: 30
                            },
                            font: {
                                size: 18
                            }
                        },
                        legend: {
                            display: false,
                            position: 'top'
                        }
                    }
                }
            });
        }
    });

// Exercise minutes in the last 7 days
fetch(`/main/charts?username=${username}`)
    .then(res => res.json())
    .then(data => {
        if (timeCanvas) {
            const timeChart = new Chart(timeCanvas.getContext('2d'), {
                type: 'bubble',
                data: {
                    datasets: [{
                        label: 'Exercise minutes',
                        data: data.bubble_data,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            displayColors: false,
                            callbacks: {
                                label: function (context) {
                                    const x = context.raw.x;
                                    const y = context.raw.y;
                                    return `Day ${x}: ${y} minutes`;
                                }
                            }
                        },
                        title: {
                            display: true,
                            text: 'Exercise minutes in the last 7 days (UTC Time)',
                            align: 'start',
                            padding: {
                                top: 10,
                                bottom: 30
                            },
                            font: {
                                size: 18
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Day'
                            },
                            min: 0,
                            max: 8,
                            ticks: {
                                stepSize: 1
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Minutes'
                            }
                        }
                    }
                }
            });
        }
    });
