/*************************************************
 * Handle charts on Dashboard                    *
 *************************************************/

// Global variables to store chart instances for updates
let kcalChart = null;
let timeChart = null;
let hourlyKcalChart = null;
let hourlyTimeChart = null;

// Initialize date selector and view toggle
function initChartControls() {
    const viewToggle = document.getElementById('viewToggle');
    const daySelector = document.getElementById('daySelector');
    const hourlyChartSection = document.getElementById('hourlyChartSection');
    const dailyChartSection = document.getElementById('dailyChartSection');
    
    // Hide hourly view by default
    hourlyChartSection.style.display = 'none';
    
    // Load date data
    fetch('/charts')
    .then(res => res.json())
    .then(data => {
        // Populate date selector
        if (data.days && data.days.length > 0) {
            daySelector.innerHTML = '';
            data.days.forEach((day, index) => {
                const option = document.createElement('option');
                option.value = day;
                // Format date for friendly display
                const date = new Date(day);
                option.text = `${date.toLocaleDateString()} (${data.p7d_labels[index]})`;
                daySelector.appendChild(option);
            });
            
            // Default to most recent date
            daySelector.value = data.days[data.days.length - 1];
        }
        
        // Load daily charts
        loadDailyCharts(data);
    });
    
    // View toggle event
    viewToggle.addEventListener('change', function() {
        if (this.value === 'daily') {
            dailyChartSection.style.display = 'block';
            hourlyChartSection.style.display = 'none';
        } else {
            dailyChartSection.style.display = 'none';
            hourlyChartSection.style.display = 'block';
            loadHourlyCharts(daySelector.value);
        }
    });
    
    // Date selection event
    daySelector.addEventListener('change', function() {
        if (viewToggle.value === 'hourly') {
            loadHourlyCharts(this.value);
        }
    });
}

// Load daily charts
function loadDailyCharts(data) {
    const kcalCtx = document.getElementById('myChart').getContext('2d');
    const timeCtx = document.getElementById('bubbleChart').getContext('2d');
    
    // Destroy existing charts if they exist
    if (kcalChart) kcalChart.destroy();
    if (timeChart) timeChart.destroy();
    
    // Create new charts
    kcalChart = new Chart(kcalCtx, {
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
    
    timeChart = new Chart(timeCtx, {
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
                        label: function(context) {
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
                },
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
                    },
                }
            }
        }
    });
}

// Load hourly charts
function loadHourlyCharts(selectedDay) {
    const hourlyKcalCtx = document.getElementById('hourlyKcalChart').getContext('2d');
    const hourlyTimeCtx = document.getElementById('hourlyTimeChart').getContext('2d');
    const noDataMsg = document.getElementById('noHourlyDataMessage');
    
    // Get hourly data for the selected date
    fetch(`/charts?view_type=hourly&selected_day=${selectedDay}`)
    .then(res => res.json())
    .then(data => {
        // Destroy existing charts if they exist
        if (hourlyKcalChart) hourlyKcalChart.destroy();
        if (hourlyTimeChart) hourlyTimeChart.destroy();
        
        // Update title with selected date
        document.getElementById('hourlyChartTitle').textContent = 
            `Hourly Data for ${data.hourly_data ? data.hourly_data.day_name : 'Selected Day'}`;
        
        // If hourly data exists
        if (data.hourly_data && data.hourly_data.hourly_cal_data.length > 0) {
            // Show charts and hide no data message
            document.getElementById('hourlyKcalChart').style.display = 'block';
            document.getElementById('hourlyTimeChart').style.display = 'block';
            noDataMsg.style.display = 'none';
            
            // Calories hourly chart
            hourlyKcalChart = new Chart(hourlyKcalCtx, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Calories by hour',
                        data: data.hourly_data.hourly_cal_data,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'category',
                            title: {
                                display: true,
                                text: "Hour (UTC)"
                            }
                        },
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
                            text: `Calories Burned by Hour on ${data.hourly_data.day_name}`,
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
                            display: false
                        }
                    }
                }
            });
            
            // Exercise duration hourly chart
            hourlyTimeChart = new Chart(hourlyTimeCtx, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Exercise minutes by hour',
                        data: data.hourly_data.hourly_duration_data,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'category',
                            title: {
                                display: true,
                                text: "Hour (UTC)"
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Minutes"
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: `Exercise Minutes by Hour on ${data.hourly_data.day_name}`,
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
                            display: false
                        }
                    }
                }
            });
        } else {
            // Show no data message and hide charts
            document.getElementById('hourlyKcalChart').style.display = 'none';
            document.getElementById('hourlyTimeChart').style.display = 'none';
            noDataMsg.style.display = 'block';
        }
    });
}

/*************************************************
 * Handle chart with GPT                         *
 *************************************************/
/* global MathJax */
// Detect the time of day and set a greeting
function detectTimeOfDay() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) {
        return "morning";
    } else if (hour >= 12 && hour < 18) {
        return "afternoon";
    } else {
        return "evening";
    }
}

// Greetings based on the time of day
const greetingsByTime = {
    morning: "Good morning! Ready to kickstart your day with a healthy plan?",
    afternoon: "Good afternoon! Need a quick workout idea or meal tip?",
    evening: "Good evening! Want to reflect on today’s progress or plan for tomorrow?"
};

// Additional random greetings
const greetings = [
    "Hi there! Are you working on weight loss, muscle gain, or just living healthier?",
    "Hey! I’m your virtual workout buddy 💪 Ask me anything about training or healthy eating.",
    "Welcome! Tell me your fitness or nutrition goal, and I’ll help you get started with a solid plan."
];
const timeOfDay = detectTimeOfDay();
greetings.push(greetingsByTime[timeOfDay]);
const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
const greetingMessage = randomGreeting;

// Prompt to tell the model to act as a personal trainer
let messageHistory = [
    {
        role: "system",
        content:
            "You are a professional personal trainer and nutritionist. Only answer health, fitness, or nutrition-related questions. If asked about anything else, politely say you're only able to assist with fitness or nutrition topics."
    }
];
messageHistory.push({ role: "assistant", content: greetingMessage });

// Load the conversation history in sessionStorage
if (sessionStorage.getItem("chatHistory")) {
    messageHistory = JSON.parse(sessionStorage.getItem("chatHistory"));
}
renderChatFromHistory(messageHistory);

// Send a message
$('#send-btn').on('click', function () {
    const $input = $('#user-input');
    const message = $input.val().toString().trim();
    if (!message) return;

    const $chat = $('#chat-window');
    $chat.append(`<div class="chat-message user">${message}</div>`);
    $chat.scrollTop($chat[0].scrollHeight);
    $input.val('');

    messageHistory.push({ role: 'user', content: message });
    sessionStorage.setItem('chatHistory', JSON.stringify(messageHistory));

    // Calling a proxy server deployed on Render
    $.ajax({
        url: 'https://exercise-assistant.onrender.com/chat',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: messageHistory
        }),
        success: function (response) {
            const reply = response.choices[0].message.content;
            $chat.append(`<div class="chat-message gpt">${reply}</div>`);
            MathJax.typeset(); // Activate MathJax for rendering LaTeX
            $chat.scrollTop($chat[0].scrollHeight);

            messageHistory.push({ role: 'assistant', content: reply });
            sessionStorage.setItem('chatHistory', JSON.stringify(messageHistory));
        },
        error: function (xhr) {
            console.error(xhr.responseText);
            $chat.append(`<div class="chat-message gpt text-danger">Error occurred.</div>`);
        }
    });
});

// User can press Enter to send
$('#user-input').on('keypress', function (e) {
    if (e.which === 13) $('#send-btn').click();
});

// Render chat history from sessionStorage
function renderChatFromHistory(history) {
    const $chat = $('#chat-window');
    history.forEach(msg => {
        if (msg.role === "system") return;
        const cssClass = msg.role === 'user' ? 'user' : 'gpt';
        $chat.append(`<div class="chat-message ${cssClass}">${msg.content}</div>`);
    });
    $chat.scrollTop($chat[0].scrollHeight);
}

// Initialize chart controls when document is ready
document.addEventListener('DOMContentLoaded', initChartControls);

// Update the selected day text when day selector changes
$('#daySelector').on('change', function() {
    const selectedDay = $(this).find('option:selected').text();
    $('#selectedDayText').text(selectedDay);
    loadHourlyData();
});

// Also update the text when view toggle changes to hourly
$('#viewToggle').on('change', function() {
    if ($(this).val() === 'hourly') {
        const selectedDay = $('#daySelector').find('option:selected').text();
        $('#selectedDayText').text(selectedDay);
    }
});
