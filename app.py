import os
from flask import Flask, render_template_string, request
from textblob import TextBlob

# Initialize the Flask application
app = Flask(__name__)

# ------------------------------------------------------------------
# HTML Template (Embedded for single-file convenience)
# In a larger production app, this would be in a 'templates' folder.
# ------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analyzer</title>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen flex flex-col items-center justify-center p-4">

    <div class="w-full max-w-2xl bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        
        <!-- Header -->
        <div class="bg-indigo-600 p-8 text-center">
            <h1 class="text-3xl font-bold text-white mb-2">
                <i class="fa-solid fa-brain mr-2"></i>Sentiment Analysis
            </h1>
            <p class="text-indigo-100">Powered by Flask & TextBlob</p>
        </div>

        <!-- Form Section -->
        <div class="p-8">
            <form action="/" method="POST" class="space-y-6">
                <div>
                    <label for="text" class="block text-sm font-semibold text-slate-700 mb-2">
                        Enter text to analyze:
                    </label>
                    <textarea 
                        name="text" 
                        id="text" 
                        rows="4" 
                        class="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition resize-none text-slate-700 placeholder-slate-400"
                        placeholder="e.g., I absolutely love this product! It's fantastic."
                        required
                    >{{ original_text if original_text else '' }}</textarea>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-xl transition duration-200 ease-in-out transform hover:-translate-y-1 shadow-md flex items-center justify-center gap-2">
                    <i class="fa-solid fa-magnifying-glass-chart"></i> Analyze Sentiment
                </button>
            </form>

            <!-- Results Section (Only shows if result exists) -->
            {% if result %}
            <div class="mt-8 animate-fade-in-up">
                <div class="relative">
                    <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="w-full border-t border-slate-200"></div>
                    </div>
                    <div class="relative flex justify-center">
                        <span class="bg-white px-3 text-sm font-medium text-slate-500">Analysis Result</span>
                    </div>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Sentiment Card -->
                    <div class="bg-{{ color }}-50 border border-{{ color }}-100 rounded-xl p-4 text-center">
                        <p class="text-sm text-{{ color }}-600 font-semibold uppercase tracking-wider mb-1">Sentiment</p>
                        <p class="text-2xl font-bold text-{{ color }}-700">{{ result }}</p>
                    </div>

                    <!-- Polarity Card -->
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
                        <p class="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">
                            Polarity
                            <span class="group relative inline-block cursor-help ml-1">
                                <i class="fa-regular fa-circle-question text-slate-400"></i>
                                <span class="invisible group-hover:visible absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 bg-slate-800 text-white text-xs rounded py-1 px-2 z-10">
                                    -1.0 (Negative) to 1.0 (Positive)
                                </span>
                            </span>
                        </p>
                        <p class="text-2xl font-bold text-slate-700">{{ polarity }}</p>
                    </div>

                    <!-- Subjectivity Card -->
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
                        <p class="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">
                            Subjectivity
                            <span class="group relative inline-block cursor-help ml-1">
                                <i class="fa-regular fa-circle-question text-slate-400"></i>
                                <span class="invisible group-hover:visible absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 bg-slate-800 text-white text-xs rounded py-1 px-2 z-10">
                                    0.0 (Objective) to 1.0 (Subjective)
                                </span>
                            </span>
                        </p>
                        <p class="text-2xl font-bold text-slate-700">{{ subjectivity }}</p>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
        
        <div class="bg-slate-50 p-4 text-center border-t border-slate-100">
            <p class="text-xs text-slate-400">&copy; Sentiment Analyzer Project</p>
        </div>
    </div>

</body>
</html>
"""

# ------------------------------------------------------------------
# Routes and Logic
# ------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    polarity = None
    subjectivity = None
    color = "slate"
    original_text = None

    if request.method == 'POST':
        original_text = request.form['text']
        
        # Perform Analysis
        blob = TextBlob(original_text)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # Logic to determine sentiment label and UI color
        if polarity > 0:
            result = "Positive"
            color = "green"
        elif polarity < 0:
            result = "Negative"
            color = "red"
        else:
            result = "Neutral"
            color = "yellow"

    return render_template_string(
        HTML_TEMPLATE, 
        result=result, 
        polarity=polarity, 
        subjectivity=subjectivity, 
        color=color,
        original_text=original_text
    )

if __name__ == "__main__":
    # Run the Flask app
    # debug=True allows the server to auto-reload if you change the code
    app.run(debug=True)