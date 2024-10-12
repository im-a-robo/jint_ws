import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data from a CSV file
df = pd.read_csv('jint_ws/server/emotion_data.csv')

# Ensure 'timestamp' is parsed as datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define colors for each emotion
colors = {
    'sad': 'blue',
    'angry': 'red',
    'surprise': 'orange',
    'fear': 'purple',
    'happy': 'yellow',
    'disgust': 'green',
    'neutral': 'grey',
}

# Create a line plot
plt.figure(figsize=(12, 6))

# Plot each emotion with different colors
for emotion, color in colors.items():
    plt.plot(df['timestamp'], df[emotion], 
             color=color, label=emotion, linewidth=2)

# Formatting the plot
plt.title('Emotion Detection Over Time')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Emotion Percentage (%)')
plt.yticks(range(0, 101, 10))  # Set y-ticks from 0 to 100%
plt.xticks(rotation=45)

# Set x-axis major formatter to show HH:MM:SS
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Add legend
plt.legend(title='Emotions')

# Show grid
plt.grid()

# Adjust the x-axis limits to fit the data dynamically
plt.xlim(df['timestamp'].min(), df['timestamp'].max())

# Show the plot
plt.tight_layout()
plt.show()
