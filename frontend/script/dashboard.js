/*************************************************
 * Handle charts on Dashboard                    *
 *************************************************/
const kcalChart = document.getElementById('myChart').getContext('2d');
const weightChart = document.getElementById('weightChart').getContext('2d');
const timeChart = document.getElementById('bubbleChart').getContext('2d');

fetch('/charts')
.then(res => res.json())
.then(data => 
    new Chart(kcalChart, {
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
                    text: 'Calories Burned in the Last 7 Days',
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
    })
);

// Weight Changes Over the Past 12 Weeks
const myWeight = {
    labels: [
        "1", "2", "3", "4",
        "5", "6", "7", "8",
        "9", "10", "11", "12"
    ],
    datasets: [{
        label: "Weight (kg)",
        data: [70, 69.5, 69, 70, 70.5, 71.2, 68.8, 67.5, 67, 66.8, 66.5, 66],
        fill: false,
        borderColor: "blue",
        tension: 0.3,
        pointBackgroundColor: "blue",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "blue"
    }]
};
const myWeightChart = new Chart(weightChart, {
    type: 'line',
    data: myWeight,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: "Weight (kg)"
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Week"
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Weight Changes Over the Past 12 Weeks',
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
            },
            tooltip: {
                displayColors: false,
                callbacks: {
                    title: function () {
                        return '';
                    },
                    label: function (context) {
                        let week = context.label;
                        let weight = context.parsed.y;
                        return `Week ${week}: ${weight}kg`;
                    }
                }
            }
        }
    }
});

// Exercise minutes in the last 100 days
//const data = Array.from({length: 100}, (_, i) => {
  //  const minutes = Math.floor(Math.random() * 120) + 30; // 30-150 phút
    //return {
      //  x: i + 1,
        //y: minutes,
       // r: minutes / 15  // bán kính tỉ lệ theo số phút (15 phút ~ 1px)
    //};
//});
fetch('/charts')
  .then(res => res.json())
  .then(data => 
    new Chart(timeChart, {
    type: 'bubble',
    data: {
        datasets: [{
            label: 'Giờ tập luyện',
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
                text: 'Exercise minutes in the last 100 days',
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
                max: 101,
                ticks: {
                    stepSize: 10
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Minutes'
                },
                min: 0,
                max: 20000
            }
        }
    }
})
  );

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